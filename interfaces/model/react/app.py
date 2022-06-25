import season
import os
import base64
import json
import datetime
import markupsafe
import re
import subprocess
from abc import *
import pypugjs

class Model(metaclass=ABCMeta):
    def __init__(self, wiz):
        self.wiz = wiz
        self.branch = wiz.branch

    @abstractmethod
    def basepath(self):
        pass

    @abstractmethod
    def cachepath(self):
        pass

    def list(self):
        fs = season.util.os.FileSystem(self.basepath())
        routes = fs.files()
        res = []
        for id in routes:
            if fs.isfile(f"{id}/app.json"):
                pkg = self(id)
                res.append(pkg.data(code=False))
        res.sort(key=lambda x: x['package']['id'])
        return res

    def cachefs(self):
        path = self.cachepath()
        fs = season.util.os.FileSystem(path)
        return fs

    def clean(self):
        fs = self.cachefs()
        fs.delete()
    
    def load(self, id):
        if id is None: return None
        return self.Package(self, id)

    def __call__(self, id):
        return self.load(id)

    class Package:
        def __init__(self, manager, id):
            self.manager = manager
            self.fs = season.util.os.FileSystem(os.path.join(manager.basepath(), id))
            self.id = id
            self.memory_id = f'app.{id}'

        def data(self, code=True):
            wiz = self.manager.wiz
            # if self.memory_id in wiz.memory and code is True:
            #     return wiz.memory[self.memory_id]

            fs = self.fs
            pkg = dict()
            pkg["package"] = fs.read.json(f"app.json")
            pkg["package"]['id'] = self.id

            if 'theme' not in pkg['package']: pkg['package']['theme'] = ''

            def readfile(key, filename, default=""):
                try: pkg[key] = fs.read(filename)
                except: pkg[key] = default
                return pkg

            if code:
                pkg = readfile("api", "api.py")
                pkg = readfile("socketio", "socketio.py")
                
                if fs.isfile(f"view.jsx"):
                    pkg["view"] = fs.read(f"view.jsx")
                else:
                    pkg["view"] = ""

                if fs.isfile(f"component.jsx"):
                    pkg["jsx"] = fs.read(f"component.jsx")
                else:
                    pkg["jsx"] = ""

                if fs.isfile(f"view.scss"):
                    pkg["scss"] = fs.read(f"view.scss")
                else:
                    pkg["scss"] = ""

                try:
                    pkg['dic'] = fs.read.json("dic.json")
                except:
                    pkg['dic'] = dict()

                wiz.memory[self.memory_id] = pkg
            return pkg

        def dic(self):
            class dicClass:
                def __init__(self, wiz, dicdata):
                    self.wiz = wiz
                    self.dicdata = dicdata

                def __call__(self, key=None):
                    dicdata = self.dicdata
                    language = self.wiz.request.language()
                    language = language.lower()
                    
                    if language in dicdata: dicdata = dicdata[language]
                    elif "default" in dicdata: dicdata = dicdata["default"]
                    
                    if key is None: return dicdata

                    key = key.split(".")
                    tmp = dicdata
                    for k in key:
                        if k not in tmp:
                            return ""
                        tmp = tmp[k]
                    return tmp

            fs = self.fs
            wiz = self.manager.wiz
            try:
                dicdata = fs.read.json("dic.json")
            except:
                dicdata = dict()
            return dicClass(wiz, dicdata)

        def cmd(self, args):
            try:
                script = " ".join(args)
                stdout = subprocess.Popen(script, shell=True, stdout=subprocess.PIPE).stdout
                return stdout.read().decode().strip()
            except Exception as e:
                print(e)

        def api(self):
            wiz = self.manager.wiz
            app = self.data()
            if app is None or 'api' not in app:
                return None

            app_id = app['package']['id']
            view_api = app['api']
            if len(view_api) == 0:
                return None
            
            tag = wiz.tag()
            logger = wiz.logger(f"[{tag}/app/{app_id}/api]", 94)
            name = os.path.join(wiz.basepath(), 'apps', app_id, 'api.py')
            apifn = season.util.os.compiler(view_api, name=name, logger=logger, wiz=wiz)

            return apifn

        def update(self, data):
            # check structure
            required = ['package', 'dic', 'api', 'socketio', 'view', 'jsx', 'scss']
            for key in required:
                if key not in data: 
                    raise Exception(f"'`{key}`' not defined")

            required = ['id']
            for key in required:
                if key not in data['package']: 
                    raise Exception(f"'`package.{key}`' not defined")

            package = data['package']

            # check id format
            id = package['id']
            if len(id) < 3:
                raise Exception(f"id length at least 3")

            allowed = "qwertyuiopasdfghjklzxcvbnm.1234567890"
            for c in id:
                if c not in allowed:
                    raise Exception(f"only small alphabet and number and . in package id")

            # update timestamp
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if 'created' not in package:
                package['created'] = timestamp
            package['updated'] = timestamp
            data['package'] = package

            # extensions
            wiz = self.manager.wiz
            # react build
            
            ## get Component Name
            p = re.compile('export[\s]+default[\s]+([A-Z]+[a-zA-Z]+[0-9]?);?')
            _search = p.search(data['jsx'])
            component = _search[1]

            ## react import check
            import_regex = re.compile('import[\s]+.+[\s]+from[\s]+[\'\"]{1}(.+)[\'\"]{1};?')
            import_list = import_regex.findall(data['jsx'])
            view_component = data['jsx']
            if "react" not in import_list:
                view_component = 'import React from "react";\n' + view_component
            view_component = 'import { useRecoilState as wizState, useRecoilValue as wizValue } from "recoil";\n' + view_component
            view_component = 'import Directive from "./ReactDirective";\n' + view_component

            ## WizComponent replace
            view_component = view_component.replace("WizComponent", package['title'])

            ## WizView replace
            is_pug = True
            try:
                is_pug = package['properties']['html'] == "pug"
            except:
                pass
            def compile(code):
                pugconfig = season.stdClass()
                pugconfig.variable_start_string = '{$'
                pugconfig.variable_end_string = '$}'

                pug = pypugjs.Parser(code)
                pug = pug.parse()
                html = pypugjs.ext.jinja.Compiler(pug, **pugconfig).compile()
                return html.replace('"{', "{").replace('}"', "}")
            wizview = data['view']
            if is_pug:
                wizview = compile(wizview)
            wizview_regex = re.compile('return[\s]+WizView;?')
            res_wizview = wizview_regex.findall(view_component)
            if res_wizview is not None and len(res_wizview) > 0:
                view = 'return (<Directive>\n' + wizview + '\n</Directive>);'
                view_component = view_component.replace(res_wizview[-1], view)

            ## save replaced code
            self.fs.write("ViewComponent.jsx", view_component)

            ## index.jsx
            js = f'''import React from "react";
import ReactDOM from "react-dom/client";
import {{ RecoilRoot }} from "recoil";
import {component} from "./ViewComponent.jsx";
const App = () => {{
    return (
        <RecoilRoot>
            <{component} />
        </RecoilRoot>
    );
}}
ReactDOM.createRoot(document.querySelector("#root")).render(<App />);'''
            self.fs.write("index.jsx", js)

            # save file
            self.fs.write.json("app.json", data['package'])
            self.fs.write.json("dic.json", data['dic'])
            self.fs.write("api.py", data['api'])
            self.fs.write("socketio.py", data['socketio'])
            self.fs.write(f"view.jsx", data['view'])
            self.fs.write(f"component.jsx", data['jsx'])
            self.fs.write(f"view.scss", data['scss'])

            root = os.path.join(season.path.project, "branch", wiz.branch())
            target_path = os.path.join(self.fs.abspath(), "index.jsx")
            build_path = os.path.join(root, "build", f"{self.id}.js")
            output = self.cmd(["cd", root, "&&", "yarn", "run", "build", target_path, build_path])
            theme_name = package['theme']
            tmp = theme_name.split("/")
            theme = tmp[0]
            layout = tmp[1]
            html = wiz.server.wiz.theme(theme).layout(layout).view('layout.html')
            html = str(html).replace("</body>", f"<script type='text/javascript' src='/build/{self.id}.js'></script>\n</body>")
            buildfs = season.util.os.FileSystem(os.path.join(root, "build"))
            buildfs.write(f"{self.id}.html", html)

            # update cache
            wiz.server.socket.bind()
            return self

        def delete(self):
            self.fs.delete()

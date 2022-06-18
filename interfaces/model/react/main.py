import datetime
import os
import season
import re

class Model(wiz.model("react/app")):
    def __init__(self, module):
        self.component = None
        self.module = module
        super().__init__(wiz)

    # override
    def basepath(self):
        return os.path.join(season.path.project, "branch", wiz.branch(), self.module)

    # override
    def cachepath(self):
        return os.path.join(season.path.project, "cache", "branch", wiz.branch(), self.module)

    def __error__(self, msg = ""):
        msg = str(msg)
        raise Exception(f"WIZ-REACT App [model][storage]: {msg}")

    # def fs(self, path=None):
    #     if path is None:
    #         return season.util.os.FileSystem(self.basepath())
    #     return season.util.os.FileSystem(self.basepath()).use(path)  

    def yarn(self):
        return wiz.model("react/yarn")(self)

    ## API METHOD

    # component rebuild
    def refresh(self, component, path=""):
        yarn = self.yarn()

        # app cache delete
        # yarn.clean_build()

        # rebuild
        yarn.build(component, path=path)

    # app load
    def __load__(self, component, code=True):
        # load app package data
        app = dict()
        app["package"] = self.read.json(f"{component}.json")
        try: app["dic"] = self.read.json(f"{component}.dic.json")
        except: app["dic"] = {}

        # if require code data
        if code:
            def readfile(key, filename, default=""):
                try:
                    app[key] = self.read.text(filename)
                except:
                    app[key] = default

            readfile("api", f"{component}.py")
            readfile("react", f"{component}.jsx")
            readfile("scss", f"{component}.scss")
        return app

    # app create
    def __template__(self, component):
        c = component.split("/")[-1]
        WIZ_REACT = f"""const {{ useState, useEffect }} = React;
import "./{c}.scss";
import dic from "./{c}.dic.json";
//import other component : ./[exported component name]
//import SubComponent from './SubComponent';

// change to component name
const {c} = () => {{
    const [value, setValue] = useState("");

    useEffect(() => {{
        /*
        wiz.API 함수
        const API = async (apiName, options = {{}}, json = true, errorDefault = null, onError = __onError__) => {{
            const opts = {{
                ...defaultOptions,
                ...options,
            }};
            try {{
                let res = await fetch(URI(apiName), opts);
                if (!json) return res;
                const {{ code, data }} = await res.json();
                if(!/^20[0124]$/.test(code)) {{
                    throw new Error(data);
                }}
                return data;
            }}
            catch(err) {{
                onError(err);
                return errorDefault;
            }}
        }}
        */
        console.log(wiz);
    }}, []);

    return (
        <div>
            this is test app.
        </div>
    );
}};

export default {c};\n"""
        WIZ_API = "def __startup__(wiz):\n    # TODO: Setup Access Level, etc.\n    pass\n\ndef status(wiz):\n    # build response\n    wiz.response.status(200, 'hello')\n    # wiz.response.status(200, hello='hello', world='world')\n"
        return {
            "package": {
                "path": "/".join(component.split("/")[:-1]),
                "component": c,
                "view": component,
            },
            "api": WIZ_API,
            "react": WIZ_REACT,
            "scss": "",
            "dic": {
                "default": {},
                "ko": {},
            },
        }

    def __path__(self, component, path=""):
        return os.path.join(path, component)

    # app save
    def __update__(self, data):
        # check required attributes
        required = ['package']
        for key in required:
            if key not in data: 
                self.__error__(f"'`{key}`' not defined")

        # check required package attributes
        required = ['path', 'component', 'view']
        for key in required:
            if key not in data['package']: 
                self.__error__(f"'`package.{key}`' not defined")

        # set timestamp created, updated
        package = data['package']
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if 'created' not in package:
            package['created'] = timestamp
        package['updated'] = timestamp
        data['package'] = package

        component = package['component']
        component_path = package['path']
        # if component name changed
        p = re.compile('export[\s]+default[\s]+([a-zA-Z]+[0-9]?);?')
        # scss_path = re.compile('\@import[\s]+[\'\"]{1}(\@root.+)[\'\"]{1};')
        # scss_list = scss_path.findall(data['scss'])
        # for __scss in scss_list:
        #     _list = [season.path.project, "react", "src"]
        #     _to = os.path.join(*_list)
        #     data['scss'] = data['scss'].replace(__scss, __scss.replace('@root', _to))
        try:
            _search = p.search(data['react'])
            component_name = _search[1]
        except Exception as e:
            self.__error__("must include `export default [component name]`")
        # print("component: ", component, component_name)
        prev_comp = self.__path__(component, path=component_path)
        next_comp = self.__path__(component_name, path=component_path)
        print(prev_comp, next_comp)
        if prev_comp != next_comp:
            # 컴포넌트 이름 중복 확인
            _info = self.app.get(next_comp)
            if _info is not None:
                self.__error__("Duplicate component name")
            # 기존 파일 삭제
            self.app.delete(component, path=component_path, refresh=False)
            component = next_comp
            package['component'] = component_name

        # check required data
        required = ['api', 'react', 'scss']
        for key in required:
            if key not in data:
                self.__error__(f"'`{key}`' not defined")
        # save data
        self.write.json(f"{next_comp}.json", data['package'])
        self.write.json(f"{next_comp}.dic.json", data['dic'])
        self.write.text(f"{next_comp}.py", data['api'])
        self.write.text(f"{next_comp}.jsx", data['react'])
        self.write.text(f"{next_comp}.scss", data['scss'])

        self.app.refresh(component, path=component_path)
        return self

    def __delete__(self, component, path="", refresh=True):
        filepath = self.__path__(component, path)
        delete_target = [
            f"{filepath}.json",
            f"{filepath}.dic.json",
            f"{filepath}.py",
            f"{filepath}.jsx",
            f"{filepath}.scss",
        ]
        for target in delete_target:
            if self.isfile(target):
                self.delete(target)
        if refresh:
            self.app.refresh(component, path=filepath)
        return self
    
    def __rows__(self, recursive=True, onlyname=True):
        files = self.files(recursive=recursive)
        res = []
        for filename in files:
            if filename.endswith(".jsx") == False:
                continue
            component = filename.replace(".jsx", "")
            if onlyname:
                res.append(component)
            else:
                res.append(self.app.load(component[1:]))
        if onlyname:
            res = sorted(res)
        else:
            res.sort(key=lambda x: self.__path__(x['package']['component'], path=x['package']['path']))
        return res

    def __get__(self, component, path=""):
        try:
            filepath = self.__path__(component, path=path)
            if self.isfile(f"{filepath}.json"):
                return self.app.load(filepath)
                # return self.app.load(component)
        except Exception as e:
            print("do not find component", component)
            print(e)
            pass
        return None

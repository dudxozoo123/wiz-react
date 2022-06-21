import season
from subprocess import check_output, STDOUT, PIPE, Popen
from os import system, popen
import os
import re
import json
import shutil

WIZ_REACT = """
/* WIZ-REACT APP API
 * additional options is refer to 
 * https://developer.mozilla.org/ko/docs/Web/API/Fetch_API/Using_Fetch
 */

const __init<COMPONENT>__ = () => {
    const defaultOptions = {
        method: "GET",
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
        },
    };

    const __onError__ = (err) => {
        console.error(err);
    }

    const URI = (apiName) => {
        return `/app/api/<COMPONENT>/${apiName}`;
    }

    const API = async (apiName, options = {}, json = true, errorDefault = null, onError = __onError__) => {
        const opts = {
            ...defaultOptions,
            ...options,
        };
        try {
            let res = await fetch(URI(apiName), opts);
            if (!json) return res;
            const { code, data } = await res.json();
            if(!/^20[0124]$/.test(code)) {
                throw new Error(data);
            }
            return data;
        }
        catch(err) {
            onError(err);
            return errorDefault;
        }
    }

    return {
        API,
        lang: () => {
            return navigator.language;
        },
    };
}
const wiz = __init<COMPONENT>__();
"""

GIT_IGNORE = """
# dependencies
/node_modules
/.pnp
.pnp.js

# testing
/coverage

# production
/build

# misc
.DS_Store
.env.local
.env.development.local
.env.test.local
.env.production.local
.eslintcache

npm-debug.log*
yarn-debug.log*
yarn-error.log*
"""

class Model:
    def __init__(self, storage):
        self.storage = storage
            
        if storage.exists() is False:
            storage.makedirs()
        self.abspath = storage.abspath()

        # check yarn installed
        if storage.namespace != "":
            return
        args = ["type", "yarn"]
        result = self.cmd(*args)
        if "not found" in result:
            self.__error__("please install yarn")
        self.default_dep = ["react", "react-dom"]
        self.default_devdep = ["@babel/core", "@babel/cli", "@babel/preset-env", "@babel/plugin-transform-react-jsx", "@babel/preset-react"]
        self.default_devdep = self.default_devdep + ["esbuild", "esbuild-sass-plugin", "node-sass"]
        self.default_devdep = self.default_devdep + ["react-vac"]
        self.__init_package_json__()

    @staticmethod
    def __check__():
        return wiz.model("react/storage").use().exists("package.json")

    def __error__(self, msg = ""):
        msg = str(msg)
        raise Exception(f"WIZ-REACT App [model][yarn]: {msg}")

    def __build_absdir__(self):
        return os.path.join(season.core.PATH.PROJECT, "react/build")

    @staticmethod
    def build_absdir():
        return os.path.join(season.core.PATH.PROJECT, "react/build")
    
    def clean_build(self):
        abspath = self.__build_absdir__()
        try:
            shutil.rmtree(abspath)
        except Exception as e:
            try:
                os.remove(abspath)
            except Exception as e:
                return False
        return True

    def __init_package_json__(self):
        if self.storage.exists("package.json"):
            return
        # --minify-whitespace --minify-identifiers --minify-syntax
        package_json = {
            "name": f"WIZ_REACT_APP",
            "version": "0.0.1",
            "license": "MIT",
            "scripts": {
                "version": "esbuild --version",
                "build": f"node ./build"
            }
        }
        print("create package.json", self.storage.abspath())
        self.storage.write.json("package.json", package_json)

        ## build.js
        build_js = """const esbuild = require("esbuild");
const { sassPlugin } = require("esbuild-sass-plugin");
const args = process.argv.slice(2);

const pluginCache = new Map();
esbuild.build({
  entryPoints: [`${args[0]}.jsx`],
  outfile: `${args[1]}.js`,
  bundle: true,
  loader: {
    ".svg": "dataurl",
    ".png": "dataurl",
    ".woff": "dataurl",
    ".woff2": "dataurl",
    ".eot": "dataurl",
    ".ttf": "dataurl",
  },
  plugins: [
    sassPlugin({
        implementation: "node-sass",
        cache: pluginCache,
    }),
  ],
});
        """
        self.storage.write.text("build.js", build_js)

        ## .gitignore
        self.storage.write.text(".gitignore", GIT_IGNORE)

        ## babel
        dev_requirements = self.default_devdep
        self.add(*dev_requirements, mode="dev")
        requirements = self.default_dep
        self.add(*requirements)

    def __script__(self, *args):
        args_str = " ".join(args)
        return f"cd {self.abspath} && {args_str}"

    def cmd(self, *args):
        try:
            script = self.__script__(*args)
            stdout = Popen(script, shell=True, stdout=PIPE).stdout
            return stdout.read().decode().strip()
        except Exception as e:
            self.__error__(f"shell command error: {e}")

    def info(self, key = None):
        data = self.storage.read.json("package.json")
        if key is None:
            return data
        if key in data:
            return data[key]
        return data

    def run(self, script, pre=True, **env):
        scripts = self.info("scripts")
        if script not in scripts:
            return
        envs = []
        for key in env:
            val = env[key]
            envs.append(f"{key}={val}")
        env_str = " ".join(envs)
        if pre:
            args = [env_str, "yarn", "run", script]
        else:
            args = ["yarn", "run", script, env_str]
        script_str = self.__script__(*args)
        system(script_str)

    def add(self, *package_list, mode="normal"):
        if len(package_list) == 0:
            return
        args = ["yarn", "add"]
        if mode == "dev":
            args.append("-D")
        args = args + list(package_list)
        script = self.__script__(*args)
        system(script)

    def remove(self, package, mode="normal"):
        info = self.info()
        checked = info["dependencies"]
        if mode == "dev":
            checked = info["devDependencies"]
        if package not in checked:
            return
        args = ["yarn", "remove"]
        args.append(package)
        script = self.__script__(*args)
        system(script)

    def build(self, component, path=""):
        storage = self.storage
        filepath = storage.__path__(component + ".jsx", path=path)
        code = storage.read.text(filepath)
        _id = f"#{component}-root".replace(" ", "")
        code = f"""{code};\n\nReactDOM.createRoot(document.querySelector("{_id}")).render(<{component} />);\n"""
        # code = f"""{code};\n\nReactDOM.render(<{component} />, document.querySelector("{_id}"));\n"""
        tmpfilepath = storage.__path__(f'.{component}', path=path)
        storage.write.text(tmpfilepath+".jsx", code)
        tmpfilepath = storage.abspath(tmpfilepath)
        build_filepath = os.path.join(self.__build_absdir__(), component)
        args = [
            "yarn",
            "run",
            "build",
            tmpfilepath,
            build_filepath,
        ]
        script_str = self.__script__(*args)
        system(script_str)
        storage.delete(tmpfilepath+".jsx")

        code = storage.read.text(build_filepath+".js")

        lang = wiz.request.language().lower()
        js = WIZ_REACT.replace("<COMPONENT>", component)
        code = f"{js};\n{code}"
        storage.write.text(build_filepath + ".js", code)

import season
import json
import datetime

def spawner(code, namespace, logger, **kwargs):
    fn = {'__file__': namespace, '__name__': namespace, 'print': logger, 'season': season}
    for key in kwargs: fn[key] = kwargs[key]
    exec(compile(code, namespace, 'exec'), fn)
    return fn

class Controller(wiz.controller("base")):
    def __startup__(self, wiz):
        super().__startup__(wiz)
        print(wiz.request.segment)
        segment = wiz.request.segment
        self.api(segment.app_unique_id, segment.app_component, segment.fnname)
        wiz.response.json(wiz.request.segment)
    
    def logger(self, tag=None, log_color=94):
        class logger:
            def __init__(self, tag, log_color, wiz):
                self.tag = tag
                self.log_color = log_color
                self.wiz = wiz

            def log(self, *args):
                tag = self.tag
                log_color = self.log_color
                wiz = self.wiz
                
                if tag is None: tag = "undefined"
                tag = "[wiz]" + tag
                
                args = list(args)
                for i in range(len(args)): 
                    args[i] = str(args[i])
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
                logdata = f"\033[{log_color}m[{timestamp}]{tag}\033[0m " + " ".join(args)
                print(logdata)

                # wiz.socketio.emit("debug", logdata + "\n", namespace="/wiz", broadcast=True)
        return logger(tag, log_color, self).log

    def api(self, app_unique_id, app_component, fnname):
        data = wiz.model("react/storage").use(app_unique_id)
        filename = f"{app_component}.py"
        if data.isfile(filename) == False:
            wiz.response.status(404)

        api = data.read.text(filename)

        logger = self.logger(f"[wiz-react][api][{app_component}]", 93)
        apifn = spawner(api, 'season.wiz.app.api', logger, wiz=wiz)
        
        if fnname not in apifn:
            wiz.response.status(404)
        
        apifn[fnname](wiz)

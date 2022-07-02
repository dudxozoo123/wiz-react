import season
import json
import time
import datetime

def spawner(code, namespace, logger, **kwargs):
    fn = {'__file__': namespace, '__name__': namespace, 'print': logger, 'season': season}
    for key in kwargs: fn[key] = kwargs[key]
    exec(compile(code, namespace, 'exec'), fn)
    return fn

def logger(tag=None, log_color=94):
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
    return logger(tag, log_color, wiz).log

def api(app_id, fnname):
    app = wiz.model("react/main")("apps").load(app_id)
    filename = "api.py"
    if app.fs.isfile(filename) == False:
        wiz.response.status(404)

    api = app.fs.read.text(filename)
    _logger = logger(f"[wiz][api][{app_id}]", 93)
    apifn = spawner(api, 'season.wiz.react.api', _logger, wiz=wiz)
    
    if fnname not in apifn:
        wiz.response.status(404)
    apifn[fnname]()

segment = wiz.request.segment
app_id = segment.app_id
fnname = segment.fnname
api(app_id, fnname)

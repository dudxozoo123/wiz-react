import flask
import season
import markupsafe

paths = wiz.request.segment.path.split("/")
path = "/".join(paths[:-1])
app_id = paths[-1]
app = wiz.model("react/main")("build").load("")

if paths[0] == "build":
    ext = app_id.split(".")[-1]
    extmap = {
        "js": "javascript",
        "css": "css",
    }
    res = ""
    try:
        res = app.fs.read.text(app_id)
    except:
        pass
    wiz.response.send(res, "text/"+extmap[ext])

view = app.fs.read.text(f"{app_id}.html")
view = markupsafe.Markup(view)
wiz.response.send(view, "text/html")

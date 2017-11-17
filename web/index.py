#!/usr/bin/env python3

from wsgiref.handlers import CGIHandler
from werkzeug.wrappers import Request, Response
from os import environ
from time import time
import json

@Request.application
def application(request):
    if not request.path in ("/", "/index", "/index.py"):
        return Response("Not found.", status=404)
    if request.method == "GET":
        with open("template.html", "rt") as templ_file:
            templ = templ_file.read()
        with open("data.json", "rt") as f:
            data = json.load(f)
        value = "ja" if data["value"] else "nein"
        if time() - data["time"] > 30 * 60:
            value = "vermutlich nein"
        lastupdate = "vor {} Minuten".format(int((time() - data["time"]) // 60))
        return Response(templ.format(value=value, lastupdate=lastupdate), content_type="text/html", status=200)
    elif request.method == "POST":
        try:
            data = json.loads(request.data.decode())
            assert isinstance(data, dict)
            assert "value" in data.keys()
            assert data["value"] in [True, False]
            with open("data.json", "wt") as f:
                json.dump({"value": data["value"], "time": time()}, f)
            return Response("", status=204)
        except Exception as exc:
            return Response("Invalid data.", status=400)
    else:
        return Response("Invalid method.", status=405)

if "REQUEST_METHOD" in environ:
    CGIHandler().run(application)
else:
    from werkzeug.serving import run_simple
    from werkzeug.wsgi import SharedDataMiddleware
    run_simple('localhost', 4000, SharedDataMiddleware(application, {
        "/style.css": 'style.css'
    }))

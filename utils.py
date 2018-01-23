from PIL import Image, ImageDraw
from flask import request
import requests

from functools import wraps
from io import BytesIO


def load_webcam(img_url):
    img_request = requests.get(img_url, stream=True)
    img = Image.open(img_request.raw).convert('RGB')
    return img


def img_to_io(img):
    img_io = BytesIO()
    img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return img_io


def draw_rectangle(img, X, Y, color=(0, 0, 0)):
    draw = ImageDraw.Draw(img)
    draw.rectangle(list(zip(X, Y)), fill=(*color, 0),
                   outline='black')
    del draw
    return img


def route_preset(prefix, *args, **kwargs):
    app = route_preset.app
    presets = route_preset.presets
    prefix = prefix.rstrip('/')

    def wrapper(fxn):
        nonlocal prefix

        @wraps(fxn)
        def _(preset=None, x0=None, x1=None, y0=None, y1=None):
            if preset is not None:
                webcam = presets[preset]['webcam']
                X = presets[preset]['X']
                Y = presets[preset]['Y']
            else:
                webcam = request.args.get("webcam")
                X, Y = (x0, x1), (y0, y1)
            return fxn(webcam, X, Y)
        _ = app.route("{}/<int:x0>,<int:x1>/<int:y0>,<int:y1>".format(prefix),
                      *args, **kwargs)(_)
        _ = app.route("{}/<string:preset>".format(prefix), *args, **kwargs)(_)
        return _
    return wrapper


route_preset.app = None
route_preset.presets = None

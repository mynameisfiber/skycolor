from PIL import Image, ImageDraw
from flask import request
import requests

from colormath.color_objects import LabColor, sRGBColor
from colormath.color_conversions import convert_color

from functools import wraps
from io import BytesIO


def image_color(webcam, X, Y):
    img = load_webcam(webcam)
    color = average_color(img, X, Y)
    return color


def average_color(img, X, Y, step=5):
    N = 0
    values = [0] * len(img.getpixel((0, 0)))
    for x in range(*X, step):
        for y in range(*Y, step):
            N += 1
            rgb = sRGBColor(*img.getpixel((x, y)), is_upscaled=True)
            lab = convert_color(rgb, LabColor)
            lab_values = lab.get_value_tuple()
            for i, c in enumerate(lab_values):
                values[i] += c
    average_lab = LabColor(*[int(v/N) for v in values])
    average_rgb = convert_color(average_lab, sRGBColor)
    return average_rgb.get_upscaled_value_tuple()


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
        fxn.route = _
        return fxn
    return wrapper


route_preset.app = None
route_preset.presets = None

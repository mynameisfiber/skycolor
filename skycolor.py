from flask import Flask, jsonify, send_file

from utils import route_preset, load_webcam
from utils import draw_rectangle, img_to_io


app = Flask(__name__)
PRESETS = {
    "brooklyn": {
        "webcam": 'http://207.251.86.238/cctv421.jpg',
        'X': (0, 225),
        'Y': (0, 25),
    }
}
route_preset.app = app
route_preset.presets = PRESETS


def average_color(img, X, Y, step=5):
    N = 0
    values = [0] * len(img.getpixel((0, 0)))
    for x in range(*X, step):
        for y in range(*Y, step):
            N += 1
            for i, c in enumerate(img.getpixel((x, y))):
                values[i] += c
    return [int(v/N) for v in values]


@route_preset("/debug/")
def debug_box(webcam, X, Y):
    img = load_webcam(webcam)
    color = average_color(img, X, Y)
    draw_rectangle(img, X, Y, color=color)
    return send_file(img_to_io(img), mimetype='image/jpeg')


@route_preset("/color/")
def color(webcam, X, Y):
    img = load_webcam(webcam)
    color = average_color(img, X, Y)
    return jsonify(color)


if __name__ == "__main__":
    print("Starting server")
    app.run(
        debug=True,
        host='0.0.0.0',
    )

from flask import Flask, jsonify, send_file, request
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from archiver import Archiver
from utils import route_preset, load_webcam
from utils import average_color, image_color
from utils import draw_rectangle, img_to_io


app = Flask(__name__)
PRESETS = {
    "brooklyn": {
        "webcam": 'http://207.251.86.238/cctv421.jpg',
        'X': (0, 225),
        'Y': (0, 25),
    }
}
ARCHIVER = Archiver(PRESETS, callback_minutes=15).start()
route_preset.app = app
route_preset.presets = PRESETS


@app.route("/archive/<string:location>")
def get_archive(location):
    if location not in PRESETS:
        return jsonify([])
    try:
        N = int(request.args.get("N", 96))
    except ValueError:
        N = 96
    finally:
        N = min(N, 96*7)
    return jsonify(ARCHIVER.get_last_N(location, N))


@app.route("/presets")
def presets_api():
    return jsonify(PRESETS)


@route_preset("/debug/")
def debug_box(webcam, X, Y):
    img = load_webcam(webcam)
    color = average_color(img, X, Y)
    draw_rectangle(img, X, Y, color=color)
    return send_file(img_to_io(img), mimetype='image/jpeg')


@route_preset("/color/")
def color(webcam, X, Y):
    color = image_color(webcam, X, Y)
    return jsonify(color)


if __name__ == "__main__":
    print("Starting server")
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000)
    IOLoop.instance().start()

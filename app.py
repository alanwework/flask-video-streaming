#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, request, Response

# import camera driver
from camera import Camera
from camera_opencv import OpenCVCamera

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

ROOT_DIR = os.path.realpath(os.path.dirname(os.path.realpath(__file__)))

app = Flask(__name__)


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        if frame:
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            yield (b'--frame--\r\n')
            break

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_feed_opencv')
def video_feed_opencv():
    """Video streaming route for opencv."""
    return Response(gen(OpenCVCamera(video_source=os.path.join(ROOT_DIR, '1.mp4'))),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video/<path:filename>')
def video(filename):
    """Video streaming route for opencv."""
    return Response(gen(OpenCVCamera(video_source=os.path.join(ROOT_DIR, filename))),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)

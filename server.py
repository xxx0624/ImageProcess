from flask import Flask, request, Response
import jsonpickle, json
import numpy as np
import cv2
import io, zlib
import urllib.parse as urlparse
from urllib.parse import parse_qs

app = Flask(__name__)


def compress_nparr(nparr):
    """
    Returns the given numpy array as compressed bytestring,
    the uncompressed and the compressed byte size.
    """
    bytestream = io.BytesIO()
    np.save(bytestream, nparr)
    uncompressed = bytestream.getvalue()
    compressed = zlib.compress(uncompressed)
    return compressed, len(uncompressed), len(compressed)


@app.route('/img/resize', methods=['POST'])
def resize():
    # convert string of image data to uint8
    bi_img = request.data
    img_arr = np.fromstring(bi_img, np.uint8)
    # get params
    width = request.args.get('w')
    height = request.args.get('h')
    if width is None or height is None:
        return Response(response=json.dumps({'msg': 'missing paramaters'}), status=400, mimetype="application/json")
    width = float(width)
    height = float(height)
    # decode image
    img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
    # resize image
    img = cv2.resize(img, (0,0), fx=width, fy=height)
    resp, _, _ = compress_nparr(img)
    return Response(response=resp, status=200, mimetype="application/octet_stream")


@app.route('/img/rotate', methods=['POST'])
def rotate():
    # convert string of image data to uint8
    bi_img = request.data
    img_arr = np.fromstring(bi_img, np.uint8)
    # get params
    angle = request.args.get('angle')
    if angle is None:
        return Response(response=json.dumps({'msg': 'missing paramaters'}), status=400, mimetype="application/json")
    angle = int(angle)
    # decode image
    img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
    # rotate image
    img_center = tuple(np.array(img.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(img_center, angle, 1.0)
    img = cv2.warpAffine(img, rot_mat, img.shape[1::-1], flags=cv2.INTER_LINEAR)
    resp, _, _ = compress_nparr(img)
    return Response(response=resp, status=200, mimetype="application/octet_stream")


@app.route('/img/flip', methods=['POST'])
def flip():
    # convert string of image data to uint8
    bi_img = request.data
    img_arr = np.fromstring(bi_img, np.uint8)
    # get params
    dir = request.args.get('dir')
    if dir is None:
        return Response(response=json.dumps({'msg': 'missing paramaters'}), status=400, mimetype="application/json")
    dir = int(dir)
    # decode image
    img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
    # rotate image
    img = cv2.flip(img, dir)
    resp, _, _ = compress_nparr(img)
    return Response(response=resp, status=200, mimetype="application/octet_stream")

@app.route('/img/gray', methods=['POST'])
def gray():
    # convert string of image data to uint8
    bi_img = request.data
    img_arr = np.fromstring(bi_img, np.uint8)
    # decode image
    img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
    # rotate image
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resp, _, _ = compress_nparr(img)
    return Response(response=resp, status=200, mimetype="application/octet_stream")


def main():
    app.run(host="0.0.0.0", port=5000)

if __name__ == '__main__':
    main()
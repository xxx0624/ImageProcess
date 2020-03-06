from __future__ import print_function
from pathlib import Path

import requests
import json
import cv2
import os
import io
import numpy as np
import zlib
import random
import string

addr = 'http://localhost:5000'

def file_exist(file_path):
    return os.path.isfile(file_path)


def random_string(len = 5):
    return ''.join(random.choice(string.digits) for i in range(len))


def parse_file_path(file_path):
    """
    Return the folder path, file name, file extension
    """
    base=Path(file_path)
    return str(base.parents[0]), str(base.stem), str(base.suffix) 


def uncompress_nparr(bytestring):
    """
    Returns the given compressed bytestring as numpy array
    """
    return np.load(io.BytesIO(zlib.decompress(bytestring)))


def check_file_exist_decorator(func):
    def inner_func(*args, **kwargs):
        if(len(args) < 1):
            print ("missing parameters")
            return
        if not file_exist(args[0]):
            print ("file not exist")
            return
        func(*args, **kwargs)
    return inner_func


@check_file_exist_decorator
def resize(file_path, width_ratio, height_ratio):
    folder, file_name, ext = parse_file_path(file_path)
    url = addr + '/img/resize'
    # encode image
    img = cv2.imread(file_path)
    _, img_encoded = cv2.imencode('.jpg', img)
    payload = img_encoded.tostring()
    response = requests.post(url, data=payload, params = {'w': width_ratio, 'h': height_ratio})
    if response.status_code != 200:
        print (json.loads(response.content))
        return 
    # decode response
    img_array = uncompress_nparr(response.content)
    file_path = os.path.join(folder, file_name + '-' + random_string() + '-resized' + ext)
    cv2.imwrite(file_path, img_array)

@check_file_exist_decorator
def generate_thumbnail(file_path):
    folder, file_name, ext = parse_file_path(file_path)
    url = addr + '/img/resize'
    # encode image
    img = cv2.imread(file_path)
    _, img_encoded = cv2.imencode('.jpg', img)
    payload = img_encoded.tostring()
    response = requests.post(url, data=payload, params = {'w': 0.1, 'h': 0.1})
    if response.status_code != 200:
        print (json.loads(response.content))
        return 
    # decode response
    img_array = uncompress_nparr(response.content)
    file_path = os.path.join(folder, file_name + '-' + random_string() + '-thumbnail' + ext)
    cv2.imwrite(file_path, img_array)


@check_file_exist_decorator
def rotate(file_path, angle):
    """
    rotate the image given angle
    when angle < 0, clockwise rotation
    when angle > 0, counter-clockwise rotation
    """
    folder, file_name, ext = parse_file_path(file_path)
    url = addr + '/img/rotate'
    # encode image
    img = cv2.imread(file_path)
    _, img_encoded = cv2.imencode('.jpg', img)
    payload = img_encoded.tostring()
    response = requests.post(url, data=payload, params = {'angle': angle})
    if response.status_code != 200:
        print (json.loads(response.content))
        return 
    # decode response
    img_array = uncompress_nparr(response.content)
    file_path = os.path.join(folder, file_name + '-' + random_string() + '-rotate' + ext)
    cv2.imwrite(file_path, img_array)


@check_file_exist_decorator
def flip(file_path, flip_dir):
    """
    flip the image given angle
    when flip_dir is v, flip the image vertically
    when it's h, flip the image horizontally
    """
    if flip_dir != 'v' and flip_dir != 'h':
        print ('wrong parameter')
        return
    folder, file_name, ext = parse_file_path(file_path)
    url = addr + '/img/flip'
    # encode image
    img = cv2.imread(file_path)
    _, img_encoded = cv2.imencode('.jpg', img)
    payload = img_encoded.tostring()
    response = requests.post(url, data=payload, params = {'dir': (0 if flip_dir == 'v' else 1)})
    if response.status_code != 200:
        print (json.loads(response.content))
        return 
    # decode response
    img_array = uncompress_nparr(response.content)
    file_path = os.path.join(folder, file_name + '-' + random_string() + '-flip' + ext)
    cv2.imwrite(file_path, img_array)


@check_file_exist_decorator
def gray(file_path):
    """
    convert the image from BRG to GRAY
    """
    folder, file_name, ext = parse_file_path(file_path)
    url = addr + '/img/gray'
    # encode image
    img = cv2.imread(file_path)
    _, img_encoded = cv2.imencode('.jpg', img)
    payload = img_encoded.tostring()
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print (json.loads(response.content))
        return 
    # decode response
    img_array = uncompress_nparr(response.content)
    file_path = os.path.join(folder, file_name + '-' + random_string() + '-gray' + ext)
    cv2.imwrite(file_path, img_array)


if __name__ == '__main__':
    resize('/Users/xxx0624/Downloads/drives/IMG_8440.JPG', 0.5, 0.5)
    rotate('/Users/xxx0624/Downloads/drives/IMG_8440.JPG', 90)
    flip('/Users/xxx0624/Downloads/drives/IMG_8440.JPG', 'h')
    generate_thumbnail('/Users/xxx0624/Downloads/drives/IMG_8440.JPG')
    gray('/Users/xxx0624/Downloads/drives/IMG_8440.JPG')
    pass
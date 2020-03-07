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
import argparse


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


def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='commands', dest='subparsers')

    resize_parser = subparsers.add_parser('resize', help='resize images')
    resize_parser.add_argument('--file', '-f', action='store',
            help='the local path of images', required=True, type=str)
    resize_parser.add_argument('--widthRatio', '-wr', action='store', 
            help='the width ratio to the old image width, from 0.0 to 1.0', required=True, type=float)
    resize_parser.add_argument('--heightRatio', '-hr', action='store', 
            help='the height ratio to the old image height, from 0.0 to 1.0', required=True, type=float)
    
    flip_parser = subparsers.add_parser('flip', help='flip images')
    flip_parser.add_argument('--file', '-f', action='store',
            help='the local path of images', required=True, type=str)
    flip_parser.add_argument('--dir', '-d', action='store', 
            help='the flip direction, v for vertically, h for horizontally', required=True, type=str)
    
    rotate_parser = subparsers.add_parser('rotate', help='rotate images')
    rotate_parser.add_argument('--file', '-f', action='store',
            help='the local path of images', required=True, type=str)
    rotate_parser.add_argument('--angle', '-a', action='store', 
            help='the rotate angle, <0 for clockwise rotation, >0 counter-clockwise rotation', required=True, type=int)

    gray_parser = subparsers.add_parser('gray', help='gray images')
    gray_parser.add_argument('--file', '-f', action='store',
            help='the local path of images', required=True, type=str)

    thumb_parser = subparsers.add_parser('thumb', help='get thumbnail images')
    thumb_parser.add_argument('--file', '-f', action='store',
            help='the local path of images', required=True, type=str)
    
    return parser.parse_args()

def apply_op(results):
    op = results.subparsers
    if op == 'flip':
        # print (results.dir)
        # print (results.file)
        flip(results.file, results.dir)
    if op == 'resize':
        # print (results.widthRatio, results.heightRatio)
        # print (results.file)
        resize(results.file, results.widthRatio, results.heightRatio)
    if op == 'rotate':
        # print (results.angle)
        # print (results.file)
        rotate(results.file, results.angle)
    if op == 'gray':
        # print (results.file)
        gray(results.file)
    if op == 'thumb':
        # print (results.file)
        generate_thumbnail(results.file)
    

if __name__ == '__main__':
    # resize('/Users/xxx0624/Downloads/drives/IMG_8440.JPG', 0.5, 0.5)
    # rotate('/Users/xxx0624/Downloads/drives/IMG_8440.JPG', 90)
    # flip('/Users/xxx0624/Downloads/drives/IMG_8440.JPG', 'h')
    # generate_thumbnail('/Users/xxx0624/Downloads/drives/IMG_8440.JPG')
    # gray('/Users/xxx0624/Downloads/drives/IMG_8440.JPG')
    apply_op(parse_args())
    pass
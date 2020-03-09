from __future__ import print_function
from pathlib import Path

import requests
import json
import cv2
import os
import io
import sys
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
        return func(*args, **kwargs)
    return inner_func


@check_file_exist_decorator
def resize(file_path, width, height):
    """resize the image to the given width and height"""
    folder, file_name, ext = parse_file_path(file_path)
    url = addr + '/img/resize'
    # encode image
    img = cv2.imread(file_path)
    _, img_encoded = cv2.imencode('.jpg', img)
    payload = img_encoded.tostring()
    response = requests.post(url, data=payload, params = {'w': width, 'h': height})
    if response.status_code != 200:
        print (json.loads(response.content))
        return None
    # decode response
    img_array = uncompress_nparr(response.content)
    file_path = os.path.join(folder, file_name + '-' + random_string() + '-resized' + ext)
    cv2.imwrite(file_path, img_array)
    return file_path

@check_file_exist_decorator
def generate_thumbnail(file_path):
    """generate a thumbnail for the given image"""
    folder, file_name, ext = parse_file_path(file_path)
    url = addr + '/img/resize'
    # encode image
    img = cv2.imread(file_path)
    _, img_encoded = cv2.imencode('.jpg', img)
    payload = img_encoded.tostring()
    response = requests.post(url, data=payload, params = {'w': 0.1, 'h': 0.1})
    if response.status_code != 200:
        print (json.loads(response.content))
        return None
    # decode response
    img_array = uncompress_nparr(response.content)
    file_path = os.path.join(folder, file_name + '-' + random_string() + '-thumbnail' + ext)
    cv2.imwrite(file_path, img_array)
    return file_path


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
        return None
    # decode response
    img_array = uncompress_nparr(response.content)
    file_path = os.path.join(folder, file_name + '-' + random_string() + '-rotate' + ext)
    cv2.imwrite(file_path, img_array)
    return file_path


@check_file_exist_decorator
def flip(file_path, flip_dir):
    """
    flip the image given angle
    when flip_dir is v, flip the image vertically
    when it's h, flip the image horizontally
    """
    if flip_dir != 'v' and flip_dir != 'h':
        print ('wrong parameter')
        return None
    folder, file_name, ext = parse_file_path(file_path)
    url = addr + '/img/flip'
    # encode image
    img = cv2.imread(file_path)
    _, img_encoded = cv2.imencode('.jpg', img)
    payload = img_encoded.tostring()
    response = requests.post(url, data=payload, params = {'dir': (0 if flip_dir == 'v' else 1)})
    if response.status_code != 200:
        print (json.loads(response.content))
        return None
    # decode response
    img_array = uncompress_nparr(response.content)
    file_path = os.path.join(folder, file_name + '-' + random_string() + '-flip' + ext)
    cv2.imwrite(file_path, img_array)
    return file_path


@check_file_exist_decorator
def gray(file_path):
    """convert the image from BRG to GRAY"""
    folder, file_name, ext = parse_file_path(file_path)
    url = addr + '/img/gray'
    # encode image
    img = cv2.imread(file_path)
    _, img_encoded = cv2.imencode('.jpg', img)
    payload = img_encoded.tostring()
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print (json.loads(response.content))
        return None
    # decode response
    img_array = uncompress_nparr(response.content)
    file_path = os.path.join(folder, file_name + '-' + random_string() + '-gray' + ext)
    cv2.imwrite(file_path, img_array)
    return file_path


def parse_args():
    """parse all the given arguments in the command line"""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='commands', dest='subparsers')

    resize_parser = subparsers.add_parser('resize', help='resize images')
    resize_parser.add_argument('--file', '-f', action='store',
            help='the local path of images', required=True, type=str)
    resize_parser.add_argument('--width', '-w', action='store', 
            help='the new width', required=True, type=int)
    resize_parser.add_argument('--height', '-hi', action='store', 
            help='the new height', required=True, type=int)
    
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
    
    return parser


_ops=['resize', 'flip', 'gray', 'thumb', 'rotate']   
def apply_ops(parser):
    """
    apply all the operations given in the command line
    and if all are successful, the last image path will be returned; if not, None will be returned.
    """
    all_argvs = sys.argv[1:]
    argvs_list = []
    temp_argvs = []
    index = 0
    while index < len(all_argvs):
        if all_argvs[index] in _ops:
            temp_argvs.append(all_argvs[index])
            index += 1
            while index < len(all_argvs):
                if all_argvs[index] in _ops:
                    argvs_list.append(temp_argvs)
                    temp_argvs = []
                    break
                temp_argvs.append(all_argvs[index])
                index += 1
        else:
            # something wrong in the parameter list
            return None

    argv_space = argparse.Namespace()
    file_path = None
    for argvs in argvs_list:
        if not file_path is None:
            argvs.append('-f')
            argvs.append(file_path)
        argv_space, _ = parser.parse_known_args(argvs, namespace=argv_space)
        file_path = apply_op(argv_space)
        if file_path is None:
            print ('{', argvs, '} failed')
            return None
        else:
            print ('{', argvs, '} is done')
    return file_path

    # while all_argvs:
    #     argv_space, all_argvs = parser.parse_known_args(all_argvs, namespace=argv_space)
    #     file_path = apply_op(argv_space)
    #     if file_path is None:
    #         return None
    #     if len(all_argvs) == 0:
    #         return file_path
    #     all_argvs.append('-f')
    #     all_argvs.append(file_path)
    # return argv_space.file


def apply_op(results):
    """apply one operation into current parser space"""
    op = results.subparsers
    if op == 'flip':
        # print (results.dir)
        # print (results.file)
        return flip(results.file, results.dir)
    if op == 'resize':
        # print (results.width, results.height)
        # print (results.file)
        return resize(results.file, results.width, results.height)
    if op == 'rotate':
        # print (results.angle)
        # print (results.file)
        return rotate(results.file, results.angle)
    if op == 'gray':
        # print (results.file)
        return gray(results.file)
    if op == 'thumb':
        # print (results.file)
        return generate_thumbnail(results.file)
    return None
    

if __name__ == '__main__':
    parser = parse_args()
    updated_file_path = apply_ops(parser)
    print (updated_file_path)
    pass
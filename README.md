## Image Process [Main Documentation]

This project is used to help users to do some simple process work, including rotating, fliping, resizing, graying and generating thumbnail images. Users can apply one / many actions to the image at one time. At the end, the new image will be created in local disk where the client is running.

`To applying multiple actions, these actions will be applied in order and you just need specify the location only once. if provided the location for more than 2 times, it will fail. Please see the below examples.`

## Architecture

[Software Architecture Link(same as the below snapshot)](https://drive.google.com/file/d/1MMYJ4xT0gDfB25MNG_GbHQfWYqefYjo-/view?usp=sharing)

### 1. Pattern & Justification about Arch
It's a `client-server` pattern. The most important reason why I use this pattern is that I try to seperate the `image processing part` from the whole process and put it in the server side, and put the `prepare process part`, including parsing arguments and lots of checking things, in the client side. In this way, it's easy for us to apply any kind of operations / any kind of combinations of operations to the given image by calling the server. And in the future, we can also make some interesting features in the server side, such as save processed images in cloud platform.

### 2. architecture snapshot
![Arch](image/arch.png)

### 3. Components & Connector
1. ArgumentCheck Decorator
It's used to check if users' actions are legal and if their parameters are missing. Implemented with `python.argparser`, it can also split these operations if there are multiple and then apply them to the image one by one.
2. FileExist Decorator
It's used to make sure the image users specify exist in the local disk.
3. Resize, Gray, Flip, Thumb, Rotate in the client side
These components are used to parse arguments from python argument list/actions and send the request to the server by HTTP.
4. API
It's responsible for receiving requests from clients and call other components to help itself to do some things, then send a response back to clients.
5. Resize, Gray, Filp, Thumb, Rotate in the server side
These components are implemented with `opencv` lib and can take in any kind of images, make some modifications on them, and then return the new images back to the caller.

### 4. Communication protocols
1. HTTP is used in the communication between server and client to exchange images and other necessary data.
2. More details about data format in the whole process is like this:
```
`Client side`: (read data from local disk) -> Image format(png, jpg, ...) -> binary array -> string -> (send data to server side)`

`Server side`: (receive data from client side) -> string -> binary array -> string -> (send data to client side)`

`Client side`: (receive data from server side) string -> Image format(jpg) -> (save data in local disk)
```

## Sample code

Pls see the below `Prepare` & `How to use` section.

## Design Pattern

`Decorator`: As we all know, there are multiple operations available for images and for each one of them, it's necessary to check if arguments in the user command line are legal and correct. So we can make use of `Decorator` to help us check some important things instead of checking everywhere by copying and pasting same code.


## APIs

[API documents by Swagger](https://xxx0624.github.io/ImageProcess/)


## Prepare

1. an image in the local disk
2. the operations you want to apply to the image
2. a python3 environment to run the client: `pip3 install -r /path/to/requirements.txt`
## How to use

1. Start the server
```
python3 server.py
```

2.1 Apply only one action to the image
```
// resize the imageExample.jpg to the new size with width 100 and height 200
python3 client.py resize -f /path/to/imageExample.jpg -w 100 -hi 200

// flip the imageExample.jpg vertically
python3 client.py flip -d v -f /path/to/imageExample.jpg

More info: python3 client3.py -h
```
2.2 Apply multiple actions to the image
```
// resize the image twice but finally the image size is 50*20
python3 client.py resize -f /path/to/imageExample.jpg -w 100 -hi 200 resize -w 50 -hi 20

// resize -> flip -> rotate -> gray -> thumb
// specify the image location only one time
python3 client.py resize -f /path/to/image.jpg -w 100 -hi 200 flip -d v rotate -a 100 gray thumb
```
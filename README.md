## Image Process

This project is used to help users to do some simple process work, including rotating, fliping, resizing and graying images. Users can apply one action / many actions to the image at one time.

### What does the processor need
1. the local image path
2. the operations you want to apply to the image
2. a python3 environment to run the client
### what will users get
1. the processed image with a new name `oldFileName-randomInteger-theOperationName.jpg`, and it's created in the location same as where the client run at
```
eg. resize this image:
Old Image: /path1/path2/img1.png 
New Image: /path1/path2/img1-12345-resized.jpg
```

## Architecture

[Software Arch](https://drive.google.com/file/d/1MMYJ4xT0gDfB25MNG_GbHQfWYqefYjo-/view?usp=sharing)

### snapshot
![Arch](image/arch.png)


## APIs
[API documents by Swagger](https://xxx0624.github.io/ImageProcess/)

## How to use the processor

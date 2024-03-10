import os
import numpy as np
from os import walk
import cv2

def resize_and_pad_images(width, height, input_dir, output_dir):
    print("Working...")
    
    # Get all the pictures in directory
    images = []
    ext = (".jpeg", ".jpg", ".png")
 
    for (dirpath, dirnames, filenames) in walk(input_dir):
        for filename in filenames:
            if filename.endswith(ext):
                images.append(os.path.join(dirpath, filename))
 
    for image in images:
        img = cv2.imread(image, cv2.IMREAD_UNCHANGED)
 
        h, w = img.shape[:2]
        pad_bottom, pad_right = 0, 0
        ratio = w / h
 
        if h > height or w > width:
            # shrinking image algorithm
            print('shrinking')
            interp = cv2.INTER_AREA
        else:
            # stretching image algorithm
            print('stretching')
            interp = cv2.INTER_CUBIC
 
        w = width
        h = round(w / ratio)
        if h > height:
            h = height
            w = round(h * ratio)
        pad_bottom = abs(height - h)
        pad_right = abs(width - w)
 
        scaled_img = cv2.resize(img, (w, h), interpolation=interp)
        padded_img = cv2.copyMakeBorder(
            scaled_img,0,pad_bottom,0,pad_right,borderType=cv2.BORDER_CONSTANT,value=[0,0,0])
    
        if not cv2.imwrite(os.path.join(output_dir, os.path.splitext(os.path.basename(image))[0] + ".png"), padded_img):     
            raise Exception("Could not write image")
        else:
            print('Written')

 
    print("Completed!")

# Example usage:
width = 1280
height = 720
input_dir = "./images"
output_dir = "./images_resized"

resize_and_pad_images(width, height, input_dir, output_dir)
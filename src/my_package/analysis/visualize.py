#Imports
from PIL import Image, ImageDraw
import PIL
import numpy as np


def plot_visualization(image, seg_store): # Write the required arguments

  # The function should plot the predicted segmentation maps and the bounding boxes on the images and save them.
  # Tip: keep the dimensions of the output image less than 800 to avoid RAM crashes.

    # Image reading
    image = image.T
    im2 = Image.fromarray(np.uint8((image*255)))
    im2 = im2.rotate(270, PIL.Image.NEAREST, expand = True)
    im2 = im2.transpose(Image.FLIP_LEFT_RIGHT)
    # Pasting mask on image
    for index in range(min(3, len(seg_store[1]))):
        mask = seg_store[1][index]
        mask = mask.T
        if(index == 0):
            image = image + mask*[1, 0.1, 0.1]
        if(index == 1):
            image = image + mask*[0.1, 1, 0.1]
        if(index == 2):
            image = image + mask*[0.1, 0.1, 1]
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            for k in range(image.shape[2]):
                if(image[i][j][k] > 1):
                    image[i][j][k] = 1
    
    # np array to image, and processing the properties
    im = Image.fromarray(np.uint8((image*255)))
    im = im.rotate(270, PIL.Image.NEAREST, expand = True)
    im = im.transpose(Image.FLIP_LEFT_RIGHT)

    img_path = f"output/Image_Segments.png"
    im.save(img_path, dpi = (800, 800))
    
    draw = ImageDraw.Draw(im2)
    # Drawing the boxes and printing the probabilities on the image
    for index in range(min(3, len(seg_store[1]))):
        top_left, bottom_right = seg_store[0][index]
        text = seg_store[2][index] + " | "+str(seg_store[3][index])
        if(index == 0):
            draw.rectangle([top_left[0], top_left[1], bottom_right[0], bottom_right[1]], outline='green', width=3)
            draw.text([top_left[0], top_left[1]-10], text, fill="#f00")
        if(index == 1):
            draw.rectangle([top_left[0], top_left[1], bottom_right[0], bottom_right[1]], outline='blue', width=3)
            draw.text([top_left[0], top_left[1]-10], text, fill="#0f0")
        if(index == 2):
            draw.rectangle([top_left[0], top_left[1], bottom_right[0], bottom_right[1]], outline='red', width=3)
            draw.text([top_left[0], top_left[1]-10], text, fill="#00f")
    # Saving the output
    img_path = f"output/Image_BoundingBox.png"
    im2.save(img_path, dpi = (800, 800))

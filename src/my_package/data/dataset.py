#Imports
import re
from PIL import Image
import numpy as np
import jsonlines

class Dataset(object):
    '''
        A class for the dataset that will return data items as per the given index
    '''

    def __init__(self, annotation_file, transforms = None):
        '''
            Arguments:
            annotation_file: path to the annotation file
            transforms: list of transforms (class instances)
                        For instance, [<class 'RandomCrop'>, <class 'Rotate'>]
        '''

        self.data = []

        # Reading .jsonl line by line
        with jsonlines.open(annotation_file) as f:
            for line in f.iter():
                self.data.append(line)

        self.transforms = transforms
        
    def __len__(self):
        '''
            return the number of data points in the dataset
        '''
        length = len(self.data)
        return length


    def __getitem__(self, idx):
        '''
            return the dataset element for the index: "idx"
            Arguments:
                idx: index of the data element.

            Returns: A dictionary with:
                image: image (in the form of a numpy array) (shape: (3, H, W))
                gt_png_ann: the segmentation annotation image (in the form of a numpy array) (shape: (1, H, W))
                gt_bboxes: N X 5 array where N is the number of bounding boxes, each 
                            consisting of [class, x1, y1, x2, y2]
                            x1 and x2 lie between 0 and width of the image,
                            y1 and y2 lie between 0 and height of the image.

            You need to do the following, 
            1. Extract the correct annotation using the idx provided.
            2. Read the image, png segmentation and convert it into a numpy array (wont be necessary
                with some libraries). The shape of the arrays would be (3, H, W) and (1, H, W), respectively.
            3. Scale the values in the arrays to be with [0, 1].
            4. Perform the desired transformations on the image.
            5. Return the dictionary of the transformed image and annotations as specified.
        '''
        # Final dictionary to be returned
        result = {}

        Img = Image.open('data/'+self.data[idx]["img_fn"])
        gt_png_ann_Img = Image.open('data/'+self.data[idx]["png_ann_fn"])

        gt_png_ann = np.array(gt_png_ann_Img)/255
        gt_png_ann = np.rollaxis(gt_png_ann.reshape(*(gt_png_ann.shape), 1), 2, 0)

        for transform_instance in self.transforms:
            Img = transform_instance(Img)

        # CHanging image characteristics for fiiting into segmentor
        image = np.array(Img)/255
        image = np.rollaxis(image, 2, 0)

        result["image"] = image
        result["gt_png_ann"] = gt_png_ann
        result["gt_bboxes"] = []

        for item in self.data[idx]["bboxes"]:
            result["gt_bboxes"].append([item["category"]]+item["bbox"])
        result["gt_bboxes"] = np.array(result["gt_bboxes"])

        return result
        
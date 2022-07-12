#Imports
from PIL import Image

class CropImage(object):
    '''
        Performs either random cropping or center cropping.
    '''

    def __init__(self, shape, crop_type='center'):
        '''
            Arguments:
            shape: output shape of the crop (h, w)
            crop_type: center crop or random crop. Default: center
        '''

        # Write your code here
        self.shape = shape
        self.crop_type = crop_type

    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)
        '''

        # Write your code here

        width, height = image.size
        crop_width = self.shape[0] if self.shape[0]<width else width
        crop_height = self.shape[1] if self.shape[1]<height else height
        mid_x, mid_y = int(width/2), int(height/2)
        cw2, ch2 = int(crop_width/2), int(crop_height/2) 
        crop_img = image.crop(((mid_x-cw2), (mid_y-ch2), (mid_x+cw2), (mid_y+ch2)))
        return crop_img

        

 
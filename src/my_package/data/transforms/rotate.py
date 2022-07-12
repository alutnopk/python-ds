#Imports
import PIL
from PIL import Image

class RotateImage(object):
    '''
        Rotates the image about the centre of the image.
    '''

    def __init__(self, degrees):
        '''
            Arguments:
            degrees: rotation degree.
        '''
        
        # Write your code here
        self.degrees = degrees

    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)
        '''

        # Write your code here

        rotated = image.rotate(self.degrees, PIL.Image.NEAREST, expand = True)
        return rotated

# img = Image.open(r'C:\Users\tanma\Desktop\IIT Kharagpur\Semester 4\SWLab\Assignment3\Assign3_20CS10089\Python_DS_Assignment\data\imgs\9.jpg')
# img.show()

# rotate = RotateImage(60)
# rotated = rotate(img)

# rotated.show()
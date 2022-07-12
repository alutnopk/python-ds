#Imports
from PIL import Image

class RescaleImage(object):
    '''
        Rescales the image to a given size.
    '''

    def __init__(self, output_size):
        '''
            Arguments:
            output_size (tuple or int): Desired output size. If tuple, output is
            matched to output_size. If int, smaller of image edges is matched
            to output_size keeping aspect ratio the same.
        '''

        # Write your code here
        self.output_size = output_size

    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)

            Note: You do not need to resize the bounding boxes. ONLY RESIZE THE IMAGE.
        '''

        # Write your code here
        if(isinstance(self.output_size, tuple)):
            resized = image.resize(self.output_size)
        else:
            width, height = image.size
            ratio = width/height
            if(width < height):
                width = self.output_size
                height = int(width/ratio)
                resized = image.resize((width, height))
            else:
                height = self.output_size
                width = int(height*ratio)
                resized = image.resize((width, height))
        return resized


# img = Image.open(r'C:\Users\tanma\Desktop\IIT Kharagpur\Semester 4\SWLab\Assignment3\Assign3_20CS10089\Python_DS_Assignment\data\imgs\9.jpg')
# img.show()

# a = RescaleImage(200)
# b = a(img)
# b.show() 
# a = RescaleImage((200, 400))
# b = a(img)
# b.show() 
# a = RescaleImage((400, 200))
# b = a(img)
# b.show() 
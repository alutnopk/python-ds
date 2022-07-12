from my_package.model import InstanceSegmentationModel
from my_package.data.dataset import Dataset
from my_package.analysis.visualize import plot_visualization
from my_package.data.transforms.rescale import RescaleImage
from my_package.data.transforms.flip import FlipImage 
from my_package.data.transforms.blur import BlurImage 
from my_package.data.transforms.crop import CropImage 
from my_package.data.transforms.rotate import RotateImage

####### ADD THE ADDITIONAL IMPORTS FOR THIS ASSIGNMENT HERE #######
from functools import partial
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import warnings
warnings.filterwarnings("ignore")


# Define the function you want to call when the filebrowser button is clicked.

def fileClick(clicked, dataset, segmentor, img_path, e):

    ####### CODE REQUIRED (START) #######
    # This function should pop-up a dialog for the user to select an input image file.
    # Once the image is selected by the user, it should automatically get the corresponding outputs from the segmentor.
    # Hint: Call the segmentor from here, then compute the output images from using the `plot_visualization` function and save it as an image.
    # Once the output is computed it should be shown automatically based on choice the dropdown button is at.
    # To have a better clarity, please check out the sample video.

    name = filedialog.askopenfilename(filetypes=[('JPG Image Format', '*.jpg'), ('JPEG Image Format', '*.jpeg'), ('PNG Image Format', '*.png')])
    if name =="":
        return
        
    print("Opening:", name)
    e.delete(0, 'end')
    e.insert(0, name)
    img_path["path"] = name
    PILimage = Image.open(name)
    img_path["image"] = PILimage
    # scaling the image between [0,1]
    image = np.array(PILimage)/255
    # rolling the axis of image to bring it from (H,W,3) to (3,H,W)
    image = np.rollaxis(image, 2, 0)

    print("****************************************************")
    print("                 ...MODEL RUNNING...                ")
    segmented_item = segmentor.__call__(image)
    plot_visualization(image, segmented_item)
    print("****************************************************")
    print("Done!")

    image = PILimage
    resize = RescaleImage(400)
    image = resize(image=image)

    #To see directly on selecteing an image
    process(clicked, img_path, e)

    ####### CODE REQUIRED (END) #######

    # `process` function definition starts from here.
    # will process the output when clicked.


def process(clicked, img_path, e):

    ####### CODE REQUIRED (START) #######
    # Should show the corresponding segmentation or bounding boxes over the input image wrt the choice provided.
    # Note: this function will just show the output, which should have been already computed in the `fileClick` function above.
    # Note: also you should handle the case if the user clicks on the `Process` button without selecting any image file.
 
    global photo
    global photo2

    if img_path["path"] == -1:
        err_msg = Label(text="No image is selected!", bg='#FFEDDB')
        print("No image is selected !")
        e.delete(0, 'end')
        e.insert(0, "Please select an image...")
        err_msg.grid(row=1, column=0)
        return

    image = Image.open(img_path["path"])
    resize = RescaleImage(400)
    image = resize(image=image)
    photo = ImageTk.PhotoImage(image)
    image_label = Label(image=photo, bg='#FFEDDB')

    if clicked.get() == "View Segmentations":
        result_img_path = r"output\Image_Segments.png"
        result_img = Image.open(result_img_path)
        result_img = resize(image=result_img)
        photo2 = ImageTk.PhotoImage(result_img)
        image_label2 = Label(root, image=photo2, bg='#FFEDDB')
        image_label.grid(row=2, column=0, columnspan=2)
        image_label2.grid(row=2, column=2, columnspan=4)
        err_msg = Label(text="                                      ", bg='#FFEDDB')
        err_msg.grid(row=1, column=0)
    else:
        result_img_path = r"output\Image_BoundingBox.png"
        result_img = Image.open(result_img_path)
        result_img = resize(image=result_img)
        photo2 = ImageTk.PhotoImage(result_img)
        image_label2 = Label(root, image=photo2, bg='#FFEDDB')
        image_label.grid(row=2, column=0, columnspan=2)
        image_label2.grid(row=2, column=2, columnspan=4)
        err_msg = Label(text="                                     ", bg='#FFEDDB')
        err_msg.grid(row=1, column=0)
    ####### CODE REQUIRED (END) #######

    # `main` function definition starts from here.
if __name__ == '__main__':

    # CODE REQUIRED (START) ####### (2 lines)
    # Instantiate the root window.
    # Provide a title to the root window.
    root = Tk()
    root.title("20CS10089 | Tkinter Python Assignment | Assignment 4")
    root.minsize(0, 0)
    root.configure(bg='#FFEDDB')

    ####### CODE REQUIRED (END) #######

    # Setting up the segmentor model.
    annotation_file = './data/annotations.jsonl'
    transforms = []

    # Instantiate the segmentor model.
    segmentor = InstanceSegmentationModel()
    # Instantiate the dataset.
    dataset = Dataset(annotation_file, transforms=transforms)

    # Declare the options.
    options = ["View Segmentations", "View Bounding Boxes"]
    clicked = StringVar()
    clicked.set("View Segmentations")
    e = Entry(root, width=70, bg="#FFF5EB")
    e.grid(row=0, column=0)

    ####### CODE REQUIRED (START) #######
    # Declare the file browsing button
    print("Please select an image...")
    
    img_path = {}
    img_path["path"] = -1
    selectButton = Button(text='Click to Open File', command=partial(fileClick, clicked, dataset, segmentor, img_path, e), bg="#EDCDBB")

    ####### CODE REQUIRED (END) #######

    ####### CODE REQUIRED (START) #######
    # Declare the drop-down button
    clicktypeDropDown = ttk.Combobox(root, width=27, values=options, textvariable=clicked, state="readonly")
    ####### CODE REQUIRED (END) #######

    # This is a `Process` button, check out the sample video to know about its functionality
    myButton = Button(root, text="Process", command=partial(process, clicked, img_path, e), bg="#EDCDBB")
    selectButton.grid(row=0, column=1)
    clicktypeDropDown.grid(row=0, column=2)
    myButton.grid(row=0, column=3)
    # CODE REQUIRED (START) ####### (1 line)
    # Execute with mainloop()
    root.mainloop()

    ####### CODE REQUIRED (END) #######
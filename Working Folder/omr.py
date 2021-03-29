"""
This script applies image recognition process to identify musical notes from an 
image. 

Course: Computer Vision, SP 21, Indiana University, Bloomington
Assignment 1: OMR
Submission by: S. Tyagi, R. Mariyappan, K. Pimparkar, N. Faro [Group 3]

Usage:
  omr.py <image_name> [--img_location=<loc>] [--with_test=<wt>]

Options:
  -h --help            Shows usage and other details
  --img_location=<loc> Path to the image.  [default: .]
  --with_test=<wt>     Compare results with standard libraries. [default: False]

"""
from docopt import docopt
from pathlib import Path
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

class omr:
    """
    Optical Music Recognition class
    """
    def __init__(self, img_name, img_location=".", with_test=False) -> None:
        """
        Constructor method
        Args:
            img_name (str): name of the image. ex. music1.png
            img_location (str, optional): Location of the image. Defaults to "."
                                          ex. ./test-images
            with_test (bool, optional): Compare with standard libraries. 
                                        Defaults to False.
        """
        self.img_name = img_name
        self.img_file = Path(img_location, img_name)
        # print(self.img_file)
        self.img_obj = Image.open(self.img_file).convert("L")
        # self.img_obj.show()
        self.img_array = np.asarray(self.img_obj)
        self.img_width = self.img_obj.width
        self.img_height = self.img_obj.height

    def convolve(self, kernel):
        """
        Method to perform 2D convolution of self.img_array and kernel.

        Args:
            kernel (np.Array): Kernel to used for the convolution.

        Return:
            Array resulted after the convolution having shape same as input 
            image array.
        """
        kernel_rows, kernel_cols = kernel.shape
        img_rows, img_cols = self.img_array.shape

        print("imgae shape: ", self.img_array.shape)
        print(self.img_array[:10,:10])

        # flip the kernel
        flipped_kernel = np.zeros(kernel.shape)
       
        ## column flips
        for i in range(flipped_kernel.shape[1]):
            flipped_kernel[:,i] = kernel[:,kernel_cols-i-1]
        kernel = flipped_kernel.copy()

        ## row flips
        for i in range(flipped_kernel.shape[0]):
            flipped_kernel[i,:] = kernel[kernel_rows-i-1,:]
        kernel = flipped_kernel.copy()
        print("Flipped kernel:\n", kernel)

        # Handle broders by padding the image with white pixels.
        ## padwidth = kernel_rows // 2 
        padwidth = kernel_rows // 2
        self.img_array_padded = np.pad(self.img_array, padwidth, 
                                    mode='constant', constant_values=255)
        
        # cross correlation
        self.img_array_out = np.zeros(self.img_array.shape)

        for y in range(img_cols):
            for x in range(img_rows):
                self.img_array_out[x, y] = \
                (kernel * self.img_array_padded[x:x+kernel_cols, y:y+kernel_rows]).sum()
        
        # print(self.img_array_out.shape)
        # print(self.img_array_out[:10,:10])
        return self.img_array_out

if __name__=="__main__":
    arguments = docopt(__doc__)
    # print(arguments)
    img_name = arguments['<image_name>']
    img_location = arguments['--img_location']
    with_test = arguments['--with_test']

    omr_obj = omr(img_name, img_location, with_test)

    # kernel = np.array([[1,2,3,11],[4,5,6,12],[7,8,9,13],[14,15,16,17]])
    kernel = np.array([[0,0,0],[0,1,0],[0,0,0]])
    omr_obj.convolve(kernel)

#PDF TO IMAGE CONVERSION 
#This script modified from https://iq.opengenus.org/pdf_to_image_in_python/

#IMPORT LIBRARIES
import pdf2image
from PIL import Image 
import time 

#DECLARE CONSTANTS
# PDF_PATH = "document.pdf" # I added this as an argument to the function below 
                            #so that I can call the function from another script
DPI = 300
OUTPUT_FOLDER = None
FIRST_PAGE = None
LAST_PAGE = None
FORMAT = 'tiff'
THREAD_COUNT = 1
USERPWD = None
USE_CROPBOX = False
STRICT = False

def pdftopil(pdf_filepath):
    #This method reads a pdf and converts it into a sequence of images
    #dpi parameter assists in adjusting the resolution of the image
    #output_folder parameter sets the path to the folder to which the PIL images can be stored (optional)
    #first_page parameter allows you to set a first page to be processed by pdftoppm 
    #last_page parameter allows you to set a last page to be processed by pdftoppm
    #fmt parameter allows to set the format of pdftoppm conversion (PpmImageFile, TIFF)
    #thread_count parameter allows you to set how many threads will be used for conversion.
    #userpw parameter allows you to set a password to unlock the converted PDF
    #use_cropbox parameter allows you to use the crop box instead of the media box when converting
    #strict parameter allows you to catch pdftoppm syntax error with a custom type PDFSyntaxError

    start_time = time.time()
    pil_images = pdf2image.convert_from_path(pdf_filepath, dpi=DPI, output_folder=OUTPUT_FOLDER, first_page=FIRST_PAGE, last_page=LAST_PAGE, fmt=FORMAT, thread_count=THREAD_COUNT, userpw=USERPWD, use_cropbox=USE_CROPBOX, strict=STRICT)
    print ("Time taken : " + str(time.time() - start_time))
    return pil_images

def save_images(pil_images, pdf_filepath):
    #This method helps in converting the images in PIL Image file format to the required image format
    index = 1
    for image in pil_images:
        image_name = pdf_filepath.split("/")[-1] #get just the filename
        image.save("{}_page_".format(image_name) + str(index).zfill(4) + ".tiff") #was .jpg in the original #to specify another folder, add it in the filename before "page"
        index += 1
        
if __name__ == "__main__":
    pil_images = pdftopil()
    save_images(pil_images) 

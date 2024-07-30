#Description: This script uses Tesseract's Uyghur OCR engine to generate machine-readable
#text files from pdf files.

#This file and pdf_to_image.py should be in the same folder 
#as the pdfs to be processed, and there should be an output folder
#specified, probably an empty folder within the one that contains the scripts
#and pdfs.

import glob
import pdf_to_image
import argparse
from PIL import Image 
import pytesseract
import cv2
import os
import numpy as np

                
def ocr_then_delete(image_filepath, lang, method=1):
    # overall structure mostly from https://www.pyimagesearch.com/2017/07/10/using-tesseract-ocr-python/ 
    """Preprocesses an image file, runs it through tesseract OCR to produce a .txt file,
    then deletes the original image file
    
    Arguments
    --------
    image_filepath = str; the filepath to the image to be OCR'd
    lang = str; a 3-letter code to tell tesseract which language the image contains
    method = str; which preprocessing method to use to enhance the image before scanning
    """
                     
    # load the image
    image = cv2.imread(image_filepath) 

    # rescale the image, if needed.
    image = cv2.resize(image, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)

    # convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    gray = cv2.dilate(gray, kernel, iterations=1)
    gray = cv2.erode(gray, kernel, iterations=1)

    # image preprocessing
    # code here mostly from https://www.freecodecamp.org/news/getting-started-with-tesseract-part-ii-f7f9a0899b3f/ 
    if method == 1:
        gray = cv2.threshold(cv2.GaussianBlur(gray, (9, 9), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    elif method == 2:
        gray = cv2.threshold(cv2.GaussianBlur(gray, (7, 7), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    elif method == 3:
        gray = cv2.threshold(cv2.GaussianBlur(gray, (5, 5), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    elif method == 4:
        gray = cv2.adaptiveThreshold(cv2.medianBlur(gray, 7), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    
    elif method == 5:
        gray = cv2.adaptiveThreshold(cv2.medianBlur(gray, 5), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    
    elif method == 6:
        gray = cv2.adaptiveThreshold(cv2.medianBlur(gray, 3), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
    
    if method == 7:
        gray = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    
    # write the grayscale image to disk as a temporary file so we can OCR it
    temp_filename = "{}.png".format(os.getpid())
    cv2.imwrite(temp_filename, gray)    
    
    # load the image as a PIL image, apply OCR, and then delete the temp file
    text = pytesseract.image_to_string(Image.open(temp_filename), lang=lang)
    os.remove(temp_filename)
    
    #write the text to a .txt document
    outfile_name = image_filepath.split("/")[-1] #get just the filename 
    outfile_name = outfile_name.split(".tiff")[0] #then remove the extension
    outfile_path = "{}.txt".format(outfile_name)
    with open(outfile_path, "w") as out_file:
        out_file.write(text)
    
    #delete the image file that we started with
    os.remove(image_filepath)
    

def merge_txt_files(input_folder, output_folder, ext):  
    """Writes a file that merges the contents of all the files in 
    a given folder with a given extension, and deletes the individual files.
    
    Arguments
    ---------
    input_folder: str; representing the path to the folder containing
                       the files to be merged, should NOT end in trailing /
    output_folder: str; representing the path to the folder containing
                       the files to be merged, should NOT end in trailing /,
                       should not be the same as input_folder
    ext: str; a text file extension of the files to be merged
    """
    
    # Creates a list of the .txt files in the input folder
    txt_filelist = glob.glob("{}/*.txt".format(input_folder))
    sorted_txt_files = sorted(txt_filelist)
    
    # Creates a custom path for the output file
    outfile_name = sorted_txt_files[0].split("_page_0001.txt")[0]
    outfile_path = "{}/{}.{}".format(output_folder, outfile_name, ext)
    
    with open(outfile_path, "w") as out_file:
        # Opens each file
        for txt_file in sorted_txt_files:
            with open(txt_file, encoding="utf-8") as in_file:
                # Writes the contents of each file followed by a line break
                out_file.write(in_file.read() + "\n")
            os.remove(txt_file)

            
if __name__=="__main__":
    parser = argparse.ArgumentParser(description="creates a machine-readable .txt version of any pdfs files in a folder using tesseract OCR engine")

    parser.add_argument("pdf_folder_path", help="the path to a folder where the pdf file(s) can be found. This should *not* have a trailing /")
    parser.add_argument("output_folder_path", help="the path to a folder where the output files will be written. This should *not* have a trailing / and it should not be the same as the pdf_folder_path")
    parser.add_argument("--ext", default="txt", help="the extension type that the final output file will have (e.g. txt if you want to output a .txt filetype)")
    parser.add_argument("--method", default="thresh", help="the preprocessing method")
    parser.add_argument("--lang", default="uig+chi_sim", help="language that Tesseract will use when OCR'ing")
    args = parser.parse_args()
    
    #get a list of all the .pdf files in the specified folder
    pdf_filelist = sorted(glob.glob("{}/*.pdf".format(args.pdf_folder_path)))
    
    for pdf in pdf_filelist:
        #split the pdf into a series of single-page images
        pil_images = pdf_to_image.pdftopil(pdf)
        pdf_to_image.save_images(pil_images, pdf)
            
        #run the image files through the OCR engine
        tiff_filelist = sorted(glob.glob("{}/*.tiff".format(args.pdf_folder_path)))
        for image_path in tiff_filelist:
            ocr_then_delete(image_path, args.lang, args.method)
            #try blur as the method arg if output is poor
                
        #splice the resulting .txt files together into a single long .txt file   
        merge_txt_files(args.pdf_folder_path, args.output_folder_path, args.ext) 

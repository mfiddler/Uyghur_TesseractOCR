# Uyghur_TesseractOCR

# Overview
The tools here take a pdf file with text in Uyghur Arabic (kona yéziq) script, scans it with an OCR engine called Tesseract, and outputs a file containing the text from the pdf.

The script called pdf_ocr.py splits the pdf files in the specified input folder into one-page .tiff image files. These are converted to .txt, then merged into a longer document (which can be .txt, .pdf, or other specified extensions) containing the entire text of the original pdf. The functions in pdf_to_image.py are called when pdf_ocr.py is run. By default the script tells the OCR engine to process files in Uyghur and simplified Chinese fonts, but language(s) can be specified as an optional argument. 

Caveat: As always, the accuracy of the OCR scanning will depend on the quality of the original pdf. I have also observed unexpected characters (e.g. Arabic letters not in the Uyghur alphabet) in the output. Manual correction is necessary if a fully accurate output is desired.

An additional script txts_to_csv.py can be used to dump the contents of multiple .txt files (presumably the output of pdf_ocr.py) into a single .csv which has the content of one .txt file per row.

# Prerequisites:
pdf2image (pip install pdf2image)
pytesseract (pip install pytesseract)
cv2 (pip install opencv-python)

# Examples
(run from the terminal):
python pdf_ocr.py . output --lang uig --method 1

Here pdf_ocr.py is the script filename, the period indicates that it should look for pdf files in the same folder where the script is located, it should save the output files in a folder called <output>, it should only scan for text in Uyghur, and it should use method 1 for preprocessing (see details of preprocessing methods in the script).

Running txts_to_csv.py from the terminal:
python txts_to_csv.py /output
Here it takes the default directory for input, i.e. the folder the script is located in, and a folder called <output> to save the output csv.




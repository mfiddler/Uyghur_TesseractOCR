# TXTS_TO_CSV
# This script takes all .txt files in the specified folder 
# and dumps their contents into a csv, one row per .txt file.

import argparse
import glob
import csv
import re
    
    
def txts_to_csv(txts_folder_path):
    """reads in any .txt files in a folder and compiles their contents in a csv"""
    
    # Creates a list of the .txt files in the input folder
    txt_filelist = glob.glob("{}/*.txt".format(txts_folder_path))
    sorted_txt_files = sorted(txt_filelist)

    # Writes the entire contents of the .txt file to a single row of the output csv
    case_number = 0
    #txt1_name = file = re.sub(r"^.*/(.*)\.txt$", r"\1", sorted_txt_files[0])
    
    #open a csv file to write the contents to
    folder_name = txts_folder_path.split("/")[-1]
    with open("{}/{}.text_compilation.csv".format(txts_folder_path, folder_name), "w", newline="") as out_file:
        writer = csv.writer(out_file, delimiter="\t")
        writer.writerow(["CASE", "FILENAME", "TEXT"])
        for txt_file in sorted_txt_files:    
            with open(txt_file, encoding="utf-8") as in_file:
                text = in_file.read()
                case_number = case_number + 1
                pdf_name = txt_file.split("/")[-1]
                pdf_name = pdf_name.split(".txt")[0]
                writer.writerow([case_number, pdf_name, text])

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="reads in any .txt files in a folder and compiles their contents in a csv")

    parser.add_argument("txts_folder_path", help="the path to a folder where the text file(s) can be found. This should *not* have a trailing /")
    args = parser.parse_args()
    
    txts_to_csv(args.txts_folder_path)

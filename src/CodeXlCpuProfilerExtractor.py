'''
Created on Dec 19, 2017

@author: dws
'''
import csv
import getopt
import os
import re
import sys
from _ast import arg

def main(argv):
    input_csv_folder = None
    output_csv = None
    try:
        opts, args = getopt.getopt(argv,"hi:o:")
    except:
        print('CodeXlCpuProfilerExtractor.py -i <input csv folder path> -o <output csv path>')
        sys.exit(2)
        
    for opt, arg in opts:
        if opt == '-h':
            print('CodeXlCpuProfilerExtractor.py -i <input csv folder path> -o <output csv path>')
            sys.exit()
        elif opt in ("-i"):
            input_csv_folder = arg
        elif opt in ("-o"):
            output_csv = arg
            
    if not input_csv_folder or not output_csv:
        print('CodeXlCpuProfilerExtractor.py -i <input csv folder path> -o <output csv path>')
        sys.exit(2)
        
    # Get all of the .csv file names.
    csv_files = [filename for filename in os.listdir(input_csv_folder) if filename.endswith(".csv")]
        
    collected_data = {}
    for input_csv_filename in csv_files:
        duration = None
        input_csv_filepath = input_csv_folder + '/' + input_csv_filename
        with open(input_csv_filepath) as f:
            reader = csv.reader(f)
    
            for row in reader:
                if 'Profile Duration:' in row:
                    duration = row
                    break
        
            if duration:
                # Expecting the string to look like this: ['Profile Duration:', '74 seconds']
                duration_time = re.search("^.*', '([0-9]+).*$", str(duration))

                if duration_time:
                    filename = os.path.splitext(input_csv_filename)[0]
                    collected_data[filename] = duration_time.group(1)
            else:
                sys.exit("Profile Duration was not found in the input .csv.  No output .csv was created.")
    
    if collected_data:
        fieldnames = []            
        with open(output_csv, 'w', newline='') as csvfile:
            for key, value in collected_data.items():
                fieldnames.append(key)
                
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
                
            writer.writerow(collected_data)    

if __name__ == "__main__":
    main(sys.argv[1:])
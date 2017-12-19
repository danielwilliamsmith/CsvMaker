'''
Created on Dec 19, 2017

@author: dws
'''
import csv
import getopt
import re
import sys
from _ast import arg

def main(argv):
    input_csv = None
    output_csv = None
    try:
        opts, args = getopt.getopt(argv,"hi:o:")
    except:
        print('CodeXlCpuProfilerExtractor.py -i <input csv path> -o <output csv path>')
        sys.exit(2)
        
    for opt, arg in opts:
        if opt == '-h':
            print('CodeXlCpuProfilerExtractor.py -i <input csv path> -o <output csv path>')
            sys.exit()
        elif opt in ("-i"):
            input_csv = arg
        elif opt in ("-o"):
            output_csv = arg
            
    if not input_csv or not output_csv:
        print('CodeXlCpuProfilerExtractor.py -i <input csv path> -o <output csv path>')
        sys.exit(2)
        
    duration = None
    with open(input_csv) as f:
        reader = csv.reader(f)
    
        for row in reader:
            if 'Profile Duration:' in row:
                duration = row
                break
        
        if duration:
            # Expecting the string to look like this: ['Profile Duration:', '74 seconds']
            duration_time = re.search("^.*', '([0-9]+).*$", str(duration))
            duration_unit = re.search("^.*', '[0-9]+ ([a-zA-Z]+)'.*$", str(duration))

            if duration_time:
                with open(output_csv, 'w', newline='') as csvfile:
                    fieldnames = ['Duration', 'Unit']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerow({'Duration': duration_time.group(1), 'Unit': duration_unit.group(1)})
        else:
            sys.exit("Profile Duration was not found in the input .csv.  No output .csv was created.")
                    
if __name__ == "__main__":
   main(sys.argv[1:])
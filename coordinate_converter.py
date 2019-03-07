import os
import csv
import glob
import re
from pyproj import Proj, transform

def clean_value(value):
    '''
    removed alphabet characters, converted double dashes to singular negative signs
    '''
    print("uncleaned: " + value)
    cleaned_value = re.sub(r'[A-z]', '', value)
    cleaned_value = re.sub(r'--', '-', cleaned_value)
    cleaned_value.strip()
    cleaned_value.rstrip()

    # print(cleaned_value)
    print("cleaned: %s"  % cleaned_value)
    return cleaned_value

def convert_nzgd2000_to_wgs84(x, y):
    '''
    Casts coordinates into numeric floats, converts them from NZGD2000 to epsg:4326
    '''
    print("converting from nzgd2000")
    coordinate_system = ({
        # New Zealand Mercator 2000
        "NZGD2000": "epsg:2193",
        # New Zealand Transverse Mercator 2000. Not supported by pyproj
        "NZTM2000": "epsg:19971",
        # WGS 84
        "WGS84": "epsg:4326",
        })
    inProj = Proj(init='epsg:2193')
    outProj = Proj(init='epsg:4326')
    out_x, out_y = transform(inProj, outProj, x, y)
    print("converted: %s %s"  % (out_x, out_y))
    return out_x, out_y

def is_dms_format(value):
    '''checks text value to see if it's a dms format'''
    spaces = [i for i in re.finditer(' ', value)]
    if len(spaces) > 1:
        return True
    else:
        return False

def is_nzgd2000(value):
    '''
    speculatively check if the value is probably nzgd2000 or at least not epsg4326.
    '''
    if float(x) > 1000 or float(y) > 0:
        return True
    else:
        return False

def extract_bad_rows(x, y, writer):
    '''
    only write the coordinate columns to the output file
    '''
    x = x.replace('-', '')
    y = y.replace('-', '')
    print(y, x)
    writer.writerow([y, x])

def DMS_to_DD(coordinate):
    '''
    Convert degrees, minutes, seconds format to decimal degrees format
    '''
    coordinate = coordinate.rstrip()
    [degrees, minutes, seconds] = [float(segment.strip(" ")) for segment in coordinate.split(" ")]
    print('d', degrees,'m', minutes,'s', seconds)
    # # rr = 10/0
    degree_decimal = degrees + (minutes/60) + (seconds/3600)
    print(degree_decimal)
    return degree_decimal

# Change to file you want to convert.
# target_directory = input("enter target directory or full file path: ")

fname = './mastersheet.tsv'
file = open(fname)
# reader = csv.reader(file, delimiter=',')

# Change change to desired output name
output_rows = input('just extract the rows? [y/n]: ')
file_reader = csv.DictReader(file, delimiter='\t')
with open(fname + "-converted", "w") as output_file:
    writer = csv.writer(output_file, delimiter="\t")
    first_line = True
    header_row = []
    for input_row_dict in file_reader:
        if first_line:
            # conditional to make first row the header
            first_line = False
            header_row = input_row_dict
            print(header_row)
            output_file.write('\t'.join(input_row_dict) + '\n')
            continue
        # Change to match the column numbers that need to be converted.
        else:
            # print(input_row)
            if output_rows == "y" or output_rows == "Y":
                try:
                    # try for original file headers
                    extract_bad_rows(input_row_dict['x'], input_row_dict['y'], writer)
                except:
                    # new file headers
                    extract_bad_rows(input_row_dict['Longitude'], input_row_dict['Latitude'], writer)
            else:
                # try to output a complete row with the converted coordinates
                field_term_x = ""
                field_term_y = ""
                try:
                # trying to get the x and y values from the input row
                    x = input_row_dict['x']
                    y =input_row_dict['y']
                    field_term_x = 'x'
                    field_term_y = 'y'
                except:
                    print("couldn't find x and y fields, resorting to long, lat")
                    x = input_row_dict['Longitude']
                    y =input_row_dict['Latitude']
                    field_term_x = 'x'
                    field_term_y = 'y'
                
                x = clean_value(x)
                y = clean_value(y)
                if is_dms_format(x) or is_dms_format(y):
                    x = DMS_to_DD(x)
                    y = DMS_to_DD(y)
                elif is_nzgd2000(x) or is_nzgd2000(y):
                    x, y = convert_nzgd2000_to_wgs84(x, y)
                    field_term_x = 'Longitude'
                    field_term_y = 'Latitude'
                print(x, y)
                # assumes x is the second row in the file, and y is the second
                output_row_dict = input_row_dict
                # insert back into the right dictionary spot
                output_row_dict[field_term_x] = str(x)
                output_row_dict[field_term_y] = str(y)
                output_file.write("\t".join(output_row_dict.values()) + '\n')



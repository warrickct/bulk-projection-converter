import csv
from pyproj import Proj, transform

def convert_coordinate(x, y):
    '''
    Casts coordinates into numeric floats, converts them from NZGD2000 to epsg:4326
    '''
    coordinate_system = ({
        # New Zealand Mercator 2000
        "NZGD2000": "epsg:2193",
        # New Zealand Transverse Mercator 2000. Not supported by pyproj
        "NZTM2000": "epsg:19971",
        # WGS 84
        "WGS84": "epsg:4326",
        })
    
    x = x.replace('--', '-')
    y = y.replace('--', '-')
    x = float(x)
    y = float(y)
    inProj = Proj(init='epsg:2193')
    outProj = Proj(init='epsg:4326')
    out_x, out_y = transform(inProj, outProj, x, y)
    return out_x, out_y

def output_only_rows(x, y, writer):
    x = x.replace('-', '')
    y = y.replace('-', '')
    print(y, x)
    writer.writerow([y, x])

def DMS_to_DD(coordinate):
    '''
    Convert degrees, minutes, seconds format to decimal degrees format
    '''
    [degrees, minutes, seconds] = [float(segment.strip(" ")) for segment in coordinate.split(" ")]
    print('d', degrees,'m', minutes,'s', seconds)
    # rr = 10/0
    degree_decimal = degrees + (minutes/60) + (seconds/3600)
    print(degree_decimal)

# Change to file you want to convert.
file = open('./input/Syrie-metadata-trimmed.csv')
reader = csv.reader(file, delimiter=',')
# Change change to desired output name
output_rows = input('output just the rows? [y/n]: ')
with open("./output/new_meta.tsv", "w") as output_file:
    writer = csv.writer(output_file, delimiter=" ")
    firstLine = True
    header_row = []
    for row in reader:
        if firstLine:
            firstLine = False
            header_row = row
            output_file.write('\t'.join(row) + '\n')
            continue
        # Change to match the column numbers that need to be converted.
        if output_rows == "y" or output_rows == "Y":
            output_only_rows(row[1], row[2], writer)
        else:
            x, y = convert_coordinate(row[1], row[2])
            converted_row = row
            converted_row[1] = str(x)
            converted_row[2] = str(y)
            output_file.write("\t".join(converted_row) + '\n')



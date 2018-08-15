import csv
from pyproj import Proj, transform

def convert_coordinate(x, y):
    '''
    Casts coordinates into numeric floats, converts them from NZGD2000 to epsg:4326
    '''
    x = x.replace('--', '-')
    y = y.replace('--', '-')
    x = float(x)
    y = float(y)
    inProj = Proj(init='epsg:2193')
    outProj = Proj(init='epsg:4326')
    out_x, out_y = transform(inProj, outProj, x, y)
    return out_x, out_y

# Change to file you want to convert.
file = open('./input/Syrie-metadata-trimmed.csv')
reader = csv.reader(file, delimiter=',')
# Change change to desired output name
with open("./output/new_meta.tsv", "w") as output_file:
    firstLine = True
    header_row = []
    for row in reader:
        if firstLine:
            firstLine = False
            header_row = row
            output_file.write('\t'.join(row) + '\n')
            continue
        # Change to match the column numbers that need to be converted.
        x, y = convert_coordinate(row[1], row[2])
        converted_row = row
        converted_row[1] = str(x)
        converted_row[2] = str(y)
        output_file.write("\t".join(converted_row) + '\n')



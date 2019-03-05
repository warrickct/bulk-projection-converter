
import json
# import shapely
import glob
import csv

def find_closest_coord(x, y):
	smallest_diff = 100000
	curHeight =  0
	for i in range(len(coordinates)):
		coord_set = coordinates[i]
		diff = abs(x - coord_set[0]) + abs(y - coord_set[1])
		if smallest_diff > diff:
			smallest_diff = diff
			curHeight = height_values[i]
			# print(smallest_diff)
		i += 1
	return curHeight

glob = glob.glob('./geojsons/nz-height-points-topo-150k.json')
# Load all the data into one fat dictionary.
height_data = {}
fname = './geojsons/nz-height-points-topo-150k.json'
with open(fname, "r") as file:
	height_data = json.load(file)
	
# order by lat, then by lon
coordinates = []
height_values = []
for feature in height_data['features']:
	coordinates.append(feature['geometry']['coordinates'])
	height_values.append(feature['properties']['Name'])

with open('./output/Gavin_water_data_2010_metadata_converted.tsv') as file:
	with open('./output_height_comparison.tsv', 'w') as output_file:
		reader = csv.reader(file, delimiter='\t')
		writer = csv.writer(output_file, delimiter='\t')
		next(reader)
		writer.writerow(['site', 'linz elevation', 'gavin elev', 'difference'])
		for line_index, line in enumerate(reader):
			x = float(line[1])
			y = float(line[2])
			height = find_closest_coord(x, y)
			print(str(line_index) +" HEIGHT " +  height)
			dif = float(height) - float(line[19])
			writer.writerow([line[0], height, line[19], dif])



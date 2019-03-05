
import json
# import shapely
import glob
import csv

def lerp(min, max, value): 
	return ((value * min) + ((1-value) * max))

def interpolateHeightFromNearbyCoords(x, y):
	smallest_diff = 100000
	smallest_diff2 = 100000
	predictedHeights =  [[0, 0], [0, 0]]
	# iterate through all the coordinates from point map.
	for i in range(len(coordinates)):
		coord_set = coordinates[i]
		diff = abs(x - coord_set[0]) + abs(y - coord_set[1])
		if smallest_diff2 > diff and smallest_diff < diff:
			smallest_diff2 = diff
			predictedHeights[1] = height_values[i]
		elif smallest_diff > diff:
			predictedHeights[0] = height_values[i]
		i += 1
	return predictedHeights

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
			heights = interpolateHeightFromNearbyCoords(x, y)
			print(str(line_index) +" HEIGHT " +  heights)
			dif = float(heights) - float(line[19])
			writer.writerow([line[0], heights, line[19], dif])



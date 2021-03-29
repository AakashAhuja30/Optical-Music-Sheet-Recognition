import numpy as np
from matplotlib import pyplot as plt
import os
from PIL import Image
import math

def hough_transform(image):
	note_image = Image.open(image).convert('L')
	axis0_accum = note_image.height
	#the space to explore and vote for each black pixel in the black n' whitye grayscale image
	axis1_accum = math.floor(note_image.height / 5)
	accumulator = np.zeros([axis0_accum, axis1_accum])
	print(accumulator.shape)
	# all pixels lower than this value will be considered as black pixels, hopefully belonging to the lines of the staff.
	pixel_threshold = 180
	# for groups of five lines on a staff
	lines_to_detect = 5

	for x in range(0,note_image.width):
		for y in range(0,note_image.height):
			pixel_val = note_image.getpixel((x,y))
			if pixel_val < pixel_threshold:
				for hough_axis1 in range(1, axis1_accum):
					for space in range(0,lines_to_detect):
						# following the format y = m*x + b where y is y-coord, x is x-coord, 
						# m is slope and b is bias. x and y are in image space, while m and b are in hough space
						# to detect five lines groups, we subsitute b with row coordinate of the first stave line
						# and m by the spacing between the lines
						hough_axis0 = abs(space * hough_axis1 + y)
						# ignore values if they exceed the image height, i.e., dim 0 of accumulator array
						if hough_axis0 < axis0_accum:
							accumulator[hough_axis0, hough_axis1] += 1

	return accumulator

def plot_hough_transform_space(accumulator):
    plt.figure(figsize=(5,10))
    plt.imshow(accumulator)
    plt.xlabel('Spacing')
    plt.ylabel('Row Coord')
    plt.savefig('hough_transform_space.png')

def traverse_hough_space(accumulator):
    max_position = (0,0)
    max_val = 0
    for x in range(0, accumulator.shape[0]):
        for y in range(0, accumulator.shape[1]):
            if max_val < accumulator[x,y]:
                max_val = accumulator[x,y]
                max_position = (x,y)
                
    return max_position[1]

def find_row_coord_first_staves(accumulator, max_val_space):
	row_coordinates_values = list(accumulator[:,max_val_space])
	row_coordinates_values.sort(reverse=True)
	row_coordinates_values = row_coordinates_values[0:50]
	coord_val = []
	for v in row_coordinates_values:
		for x in range(0, accumulator.shape[0]):
			acc_val = accumulator[x,max_val_space]
			if v == acc_val:
				coord_val.append(x)

	return coord_val

def generate_spacing_coords_hough(image):
	accumulator = hough_transform(image)
	max_val_space = traverse_hough_space(accumulator)
	print(max_val_space)
	row_coords = find_row_coord_first_staves(accumulator, max_val_space)
	print(row_coords)

	trebel_stave = row_coords[0]
	bass_stave = row_coords[1]
	print('row coordinate of trebel ' + str(trebel_stave) + ' and row coordinate of bass stave ' + str(bass_stave) + ' with spacing ' + str(max_val_space))
	plot_hough_transform_space(accumulator)
	return max_val_space, trebel_stave, bass_stave


note_image = os.path.join(os.getcwd() + '/test-images/', 'music1.png')
space, trebel_stave, bass_stave = generate_spacing_coords_hough(note_image)


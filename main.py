# Script to take a base .bmp map and compare a theoretically arbitrary number
# of variants to it, and detecting where the variants diverge from the base.
#
# The output for the script will be a map with all changes made in the map
# variants applied to the base map, except where multiple variants disagree
# with each other and the base map. Should that happen, the pixel value of
# where it occurs will be logged.
#
# The output of this script will be a .bmp map with all changes from the 
# variants applied to it, except in the cases outlined above where different
# variants disagree with not only each other, but also the base map.

from PIL import Image
import os
import numpy as np

X_MAX = 5632
Y_MAX = 2048

TOLERANCE = 100
FILENAME = 'base.bmp'

os.chdir('maps')

def set_base_map():
    print('Initializing the base map.')
    im = Image.open(FILENAME)
    base_map_raw = np.array(im)
    
    base_map = np.zeros((X_MAX, Y_MAX), dtype = list)
    for x in range(X_MAX):
        for y in range(Y_MAX):
            base_map[x,y] = tuple(base_map_raw[y, x])
        
    return base_map 
    
def scan_other_maps(base_map):
    # Scans other maps in the dictionary, and creates a list of lists for the
    # changes in each variant of the base map. Each entry in a sublist will  
    # have two values, the first being the pixel coordinate, and the second  
    # being the color that said variant wants to place in the pixel coordinate.
    directory_files = os.listdir()
    
    directory_files.remove('unused')
    directory_files.remove('base.bmp')
    
    changes = []
        
    for filename in directory_files:
        print('Initializing {}.'.format(filename))
        im = Image.open(filename)
        variant_map = np.array(im)
        
        variant_changes = []
        
        for x in range(X_MAX):
            for y in range(Y_MAX):
                variant_val = tuple(variant_map[y, x])
                
                if variant_val != base_map[x, y]:
                    variant_changes.append([(x, y), variant_val])
        
        changes.append(variant_changes)
        
    return base_map, changes
                    

def check_proximity(changes, noise = 'quiet'):
    # Setting up list for pixels to be aware of. The first sublist is for
    # pixels which are merely too close to a pixel from another map variant.
    # The second sublist is for pixels which two variants both want to change.
    warning_pixels = [[], []]
    
    directory_files = os.listdir()
    
    directory_files.remove('unused')
    directory_files.remove('base.bmp')

    
    if len(changes) > 1:
        for i, change_list_1_raw in enumerate(changes):
            for j, change_list_2_raw in enumerate(changes):
                if i != j and i < j:
                    if noise == 'loud':
                        print('Comparing proximity for {} and {}.'
                              .format(directory_files[i], directory_files[j]))

                    change_list_1 = [i for i in change_list_1_raw if i not in change_list_2_raw]
                    change_list_2 = [i for i in change_list_2_raw if i not in change_list_1_raw]
                    
                    min_distance, warning_pixels = get_min_distance_changes(change_list_1, change_list_2, warning_pixels)
                    
                    if min_distance < TOLERANCE and noise == 'loud':
                        print('{} and {} have a pixel distance of {}.'
                              .format(directory_files[i], directory_files[j], min_distance))
    
    # Removing duplicates from warning_pixels.
    warning_pixels[0] = set(warning_pixels[0])
    warning_pixels[1] = set(warning_pixels[1])
    
    return warning_pixels

def get_min_distance_changes(change_list_1, change_list_2, warning_pixels):
    min_distance = np.inf
    
    for pixel_1 in change_list_1:
        for pixel_2 in change_list_2:
            pixel_1_coord, pixel_1_color = pixel_1
            pixel_2_coord, pixel_2_color = pixel_2

            distance = np.sqrt((pixel_2_coord[0] - pixel_1_coord[0])**2 + 
                               (pixel_2_coord[1] - pixel_1_coord[1])**2)
            
            if distance == 0:
                warning_pixels[1].append(pixel_1_coord)
            elif distance < TOLERANCE:
                warning_pixels[0].append(pixel_1_coord)
                warning_pixels[0].append(pixel_2_coord)
            
            if distance < min_distance:
                min_distance = distance
                
    
    return min_distance, warning_pixels

def output(base_map, changes, warning_pixels):
    '''
    Creating the output files, applying all changes to the base map.
    
    A log file will also be created, which will be a blank map where no changes
    have occurred. Red pixels will represent conflicting changes, yellow will
    represent changes too close to changes being made by another map, while
    green pixels represent changes which are sufficiently far away from any
    changes made by another map.
    '''
        
    output_map = Image.open(FILENAME)
    output_log = Image.new('RGB', (X_MAX, Y_MAX), color = (255, 255, 255))    

    os.chdir('..')
    
    for variant_changes in changes:
        for pixel_change in variant_changes:
            pixel_coord, pixel_color = pixel_change
            
            if pixel_coord in warning_pixels[1]:
                output_log.putpixel(pixel_coord, (255, 0, 0))
                
            elif pixel_coord in warning_pixels[0]:
                output_log.putpixel(pixel_coord, (255, 255, 0))
                output_map.putpixel(pixel_coord, pixel_color)

            else:
                output_log.putpixel(pixel_coord, (0, 255, 0))
                output_map.putpixel(pixel_coord, pixel_color)                
                
    output_map.save('output_map.bmp')
    output_log.save('output_log.bmp')

def main():
    base_map = set_base_map()
    base_map, changes = scan_other_maps(base_map)
    warning_pixels = check_proximity(changes)
    output(base_map, changes, warning_pixels)
        
main()
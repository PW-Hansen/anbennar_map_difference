## Map difference finder 1.0.0
Finds differences between a base .bmp file and variants made on said base, then creates an output .bmp file with changes made in those variants (if there are no conflicting changes made in the various variants), as well as creating a .bmp log file showing where changes have been made. Red pixels in this log file will represent conflicting changes, while green pixels represent unopposed changes. Yellow pixels in this log file, however, will represent pixels which are close to changes being made by another variant of the base map.

The tolerance for when other changes are too close is set to 100, but this can be changed on line 20 of the script.

# Usage guidelines
* The script needs to know the base version from which multiple variants are working off of. Put this into the maps folder, and either rename the .bmp file to "base.bmp" or change line 21 in the script to match the name of the base map.
* Add variants of the base map to the maps folder. Note: Do not add anything other than .bmp files to this folder.
* Adjust the tolerance as needed.
* Run the script. Note that it may take the script about a minute to run for each .bmp file, since each file has more than 10M pixels that must be accessed.
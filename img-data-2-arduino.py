#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3

from collections import defaultdict
import png
import argparse

parser = argparse.ArgumentParser(description='Convert piskel png to Arduino code')
parser.add_argument('png_filename', type=str, nargs=1,
                   help='The name of the file to convert')
args = parser.parse_args()

import pdb; pdb.set_trace()

# Now let's read in the file
reader=png.Reader(args.png_filename[0])
img_def=reader.read()

n_columns = img_def[0]
n_rows = img_def[1]
image = list(img_def[2])       #  convert the iterator to a list (to print later)
n_planes = img_def[3]['planes']

print("There are {} columns of pixels in the image".format(n_columns))
print("There are {} rows of pixels in the image".format(n_rows))
print("There are {} planes of color in the data".format(n_planes))
print("And here is the image data")
print(image)

#
# Convert each row of the image (it is a two dimensional array)
# to color_value and then to palette index.  (In the process of
# doing that, the palette should get built)
#
# Dump the palette out as an array of uint32_t (C++ code) definition
#
# Rotate the image to column major form and generate the data in
# column major form (to be shift in to the matrix 1 colum at a time)
#
#

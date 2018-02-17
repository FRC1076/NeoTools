#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
from collections import defaultdict
import png
import argparse
import neo_palette as pal

# Number of rows in the display (the length of glyph columns)
ROWS_PER_GLYPH = 8

def planes_to_color(planes):
    return (planes[0] << 16) | (planes[1] <<  8) | planes[2]

def collapse_planes_helper(n_planes, pal, colors, img_data):
   if len(img_data) == 0:
       return colors
   else:
       colors.append(neo_pal.color_index(planes_to_color(img_data[0:n_planes])))
       return collapse_planes_helper(n_planes, pal, colors, img_data[n_planes:])

def collapse_planes(n_planes, pal, planes):
    """
    Collapse the color planes into a single color index and build
    the color palette as you do so.
    """
    colors = []
    return collapse_planes_helper(n_planes, pal, colors, planes)

parser = argparse.ArgumentParser(description='Convert piskel png to Arduino code')
parser.add_argument('png_filename', type=str, nargs=1,
                   help='The name of the file to convert')
args = parser.parse_args()


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
#  Let's use a palette to record colors and build the index
#
neo_pal = pal.NeoPalette()

if n_planes > 1:
    colors = [collapse_planes(n_planes, neo_pal, p) for p in image]

# OR  colors = map(lambda p: collapse_planes_helper(p), img_data)

#   zip(*foo) gathers first element of each sublist into a new tuple and
#   returns an array of tuples.
#   This gives us an inversion.    Handle multiple font lines for
#   the purposes of 16x16 image representations.
rotated_colors = []
n_glyphsets = n_rows // ROWS_PER_GLYPH

for gset in range(0,n_glyphsets):
    rotated_colors.append(list(zip(*colors[gset*ROWS_PER_GLYPH:(gset+1)*ROWS_PER_GLYPH])))

print("Palette is:")
print([hex(c) for c in neo_pal.colors()])

print("static uint32_t colors = {")
for c in neo_pal.colors():
    print(f"        {hex(c)},")
print("};")


print("GlyphColumn32 column_data[{}][{}] = {{".format(n_glyphsets, len(rotated_colors[0])))
for gset in range(0,n_glyphsets):
    print("  {")
    for col_tup in rotated_colors[gset]:
        print(f"    GC32{col_tup},")
    print("  },")
print("};")


#
# Convert each row of the image (it is a two dimensional array)
# to color_value and then to palette index.  (In the process of
# doing that, the palette should get built)
#
# Dump the palette out as an array of uint32_t (C++ code) definition
#
# Rotate the image to column major form and generate the data in
# column major form (to be shifted in to the matrix 1 colum at a time)
#
#

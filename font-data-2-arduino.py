#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
from collections import defaultdict
import png
import argparse
import neo_palette as pal

# Number of rows in the display (the length of glyph columns)
ROWS_PER_GLYPH = 8

def planes_to_color(planes):
    if len(planes) > 1:
      return (planes[0] << 16) | (planes[1] <<  8) | planes[2]
    else:
      return planes[0]

def color_dim(color):
    r = (color & 0xff0000) >> 16
    g = (color & 0xff00) >> 8
    b = (color & 0xff)
    r = r >> 2
    g = g >> 2
    b = b >> 2
    return (r << 16) | (b << 8) | g

def collapse_planes_helper(n_planes, pal, colors, img_data):
   if len(img_data) == 0:
       return colors
   else:
       colors.append(pal.color_index(planes_to_color(img_data[0:n_planes])))
       return collapse_planes_helper(n_planes, pal, colors, img_data[n_planes:])

def collapse_planes(n_planes, pal, planes):
    """
    Collapse the color planes into a single color index and build
    the color palette as you do so.
    """
    colors = []
    return collapse_planes_helper(n_planes, pal, colors, planes)

parser = argparse.ArgumentParser(description='Convert font png to Arduino code for font')
parser.add_argument('png_filename', type=str, nargs=1,
                   help='The name of the file to convert')
parser.add_argument('font_index', type=int, nargs=1,
                   help='The index of the font to extract', default=0)
args = parser.parse_args()


# Now let's read in the file
reader=png.Reader(args.png_filename[0])
img_def=reader.read()

n_columns = img_def[0]
n_rows = img_def[1]
image = list(img_def[2])       #  convert the iterator to a list (to print later)
n_planes = img_def[3]['planes']
palette = img_def[3]['palette']


print("There are {} columns of pixels in the image".format(n_columns))
print("There are {} rows of pixels in the image".format(n_rows))
print("There are {} planes of color in the data".format(n_planes))
print("And here is the palette data")
print(palette)
#print(image)

#
#   Extract only the 8 lines representing the font glyphs
#   This is a bit of a hack.  Have to adjust n_rows accordingly
#
font_index = args.font_index[0]
image = image[font_index*8:font_index*8+8]
n_rows = ROWS_PER_GLYPH

#
#  Let's use a palette to record colors and build the index
#
neo_pal = pal.NeoPalette()

#
#  Build a collection of the color indices
#
colors = [collapse_planes(n_planes, neo_pal, p) for p in image]

compressed_palette = []
for ci in neo_pal.colors():
    print(f"Color Index = {ci} planes {palette[ci]} color {hex(planes_to_color(palette[ci]))}")
    compressed_palette.append(planes_to_color(palette[ci]))


# OR  colors = map(lambda p: collapse_planes_helper(p), img_data)

#   zip(*foo) gathers first element of each sublist into a new tuple and
#   returns an array of tuples.
#   This gives us an inversion.    Handle multiple font lines for
#   the purposes of 16x16 image representations.
rotated_colors = []
n_glyphsets = n_rows // ROWS_PER_GLYPH

for gset in range(0,n_glyphsets):
    rotated_colors.append(list(zip(*colors[gset*ROWS_PER_GLYPH:(gset+1)*ROWS_PER_GLYPH])))

#
#  Dig it out
#
rotated_colors = rotated_colors[0]

print("/* extracted color palette */")
print("static uint32_t colors[] = {")
for c in compressed_palette:
    print(f"        {hex(c)},")
print("};")

n_glyphs = n_columns // ROWS_PER_GLYPH

print(f"FontGlyph32 font_data[{n_glyphs}] = {{")
for glyphindex in range(0,n_glyphs):
    glyphchar = glyphindex + ord(' ')
    x = glyphindex*8
    print(f"FontGlyph32(     /* '{chr(glyphchar)}' = {glyphchar} */")
    for col_tup in rotated_colors[x:x+7]:
      print(f"    GC32{col_tup},")
    print(f"    GC32{rotated_colors[x+7]}")      
    print("        ),")
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

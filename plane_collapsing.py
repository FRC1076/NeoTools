#  This fake combiner just combines 4 values into a single
#  value.   You'll want to use the color fn to combine color
#  planes eventually.  But if you want to stay in the decimal
#  world so everything is easy then this is fine for getting
#  everything working.   Then you'll swap out the combiner
#  for the NeoPalette::neo_color()  function or something.
#
def test_fake_combiner():
    assert(combiner([1,2,3,4]) == 1234)

def combiner(values):
    return values[0]*1000 + values[1]*100 + values[2]*10 + values[3]


#  Some .png image formats provide image data as an array of color values
#  called planes.   The header identifies how many planes there are.
#  For now, we will just assume we have 4 planes.    So, to represent
#  the data for a row of 10 pixels, there is an array of 40 color values.
#  Those need to be grouped into an array of 10 numbers representing the
#  color values for the pixel.   With the aid of the NeoPalette class,
#  we can put those color values into an index and then represent each
#  pixel value with a small number that is the color index.
#
#  So, for example.  Here is an image with 4 pixels.  Imagine it could
#  be 4000, though.
#
#  img = [ 1, 2, 3, 4, 0, 0, 0, 0, 1, 2, 3, 4, 0, 0, 0, 0]
#
#  If we collapse this into 4 pixels representing the color we get:
#
#  collapsed_img = [ 1234, 0, 1234, 0]
#
#  If we put those into a NeoPalette, and it assigns an index of 0 to the 0
#  and 1 to the 1234 value, then we can represent our image with:
#
#  NeoPalette =>  index: 0  color: 0     index: 1   color: 1234
#  paletted_img = [ 1, 0, 1, 0 ]
#
#  So, we could represent the image data for 4000 pixels with 500 bytes.
#  One bit for each pixel.   And then a few more bytes for the palette.
#
#  Now here are the tests to work on your collapse_planes function.  It should
#  combine 4 numbers into a single value.    So, for example, a list of
#  40 values should be combined into a list of 10 values.
#
#  Use the combiner() function from above.   We will, of course use
#  the NeoPixel color function (see color.py TDD project)
#
#
def test_empty_list():
    assert(collapse_planes([]) == [])
    
def test_single_collapse():
    assert(collapse_planes([0,0,0,0]) == [0])

def test_two_collapse():
    assert(collapse_planes([0,0,0,0,1,2,3,4]) == [0,1234])

def test_many_collapse():
    assert(collapse_planes([0,0,0,0,1,2,3,4,5,6,7,8,1,2,3,4,5,6,7,8,2,3,4,5,1,2,3,4]) == [0,1234,5678,1234,5678,2345,1234])

def collapse_planes(planes):
    """
    Given a list of color planes, reduce the list by combining factor elements
    using the a combiner function  (see above).   We will change that fn later and use
    methods in the NeoPalette class the do both collapse and combine.   But for now just
    figure out how to do this elegantly.
    
    You might want to try it using iteration (using for loops with index+=4,
    using recursion, and even using functional style to see what works best,
    and to sharpen your python skills.   Ask for hints if you want some.

    Here are a few:
          You can slice four elements from an array A using:   A[0:4]
          You can refer to the remainder of the array A as:    A[4:]
          This could help in writing a recursive version of this function.
    """
    return 0


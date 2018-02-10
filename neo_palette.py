# neo_palette.py
def test_initialized_palette():
    """
    Test freshly initialized empty palette.  It should have
    the one (off) color 0 at index 0.
    """
    pal = NeoPalette()
    assert(pal.n_colors() == 1)
    assert(pal.color_index(0) == 0)
    assert(pal.n_colors() == 1)      # should be no change

def test_single_color_add():
    pal = NeoPalette()
    pal.color_index(10)
    assert(pal.n_colors() == 2)

def test_dupli_color_add():
    pal = NeoPalette()
    assert(pal.color_index(10) == 1)
    assert(pal.n_colors() == 2)
    assert(pal.color_index(5) == 2)
    assert(pal.n_colors() == 3)

def test_multi_color_add():
    pal = NeoPalette()
    for c in [0, 10, 50, 75]:
        pal.color_index(c)
    assert(pal.color_index(75) == 3)
    assert(pal.n_colors() == 4)

def test_multi_dupli_color_add():
    pal = NeoPalette()
    helper_add_or_get_color(pal, [75, 75, 50, 10, 0, 50, 10, 75, 33])

def helper_add_or_get_color(pal, color_list):
    """
    Add or get a color and do some generic checks for each color added
    Record each index returned in a dictionary so we can check correctness
    at the end.
    """
    #
    #  Use assigned dictionary to check our work
    #
    assigned = { }
    nc = pal.n_colors()
    for c in color_list:
        ci = pal.color_index(c)         #  get color or assign new index for new color
        # when a new color is added to the palette
        if (ci == nc):
            nc += 1
            assert(pal.n_colors() == nc)
        # no matter what we got, remember the result so we
        # can check at the end.
        assigned[str(c)] = ci

    # Now check to make sure that returned values are
    # still the same for each color and that no new indices
    # are created.

    nc = pal.n_colors()
    assert(len(pal.colors()) == nc)
    for c in color_list:
        assert(assigned[str(c)] == pal.color_index(c))
        assert(pal.n_colors() == nc)

class NeoPalette:
    def __init__(self):
        """
        Create the palette for use.
        Note: Developer may choose a different organization for the color index.
        Empty palette always has a single color (off) at index 0
        """
        self._colors = [0]
        self._num_colors = 1

    def color_index(self, neo_color):
        """
        If the neo_color is already in the existing palette, then
        return the index of the color.  If it is not, add it and return
        the color index for the added entry.
        """
        
        try:
            ci = self._colors.index(neo_color)
            return ci
        except ValueError:
            self._colors.append(neo_color)
            return len(self._colors)-1

    def n_colors(self):
        """
        Return how many colors are in the palette.   We try to keep this under
        control.
        """
        return len(self._colors)       

    def colors(self):
        """
        Return the collection of colors in the index
        """
        return self._colors

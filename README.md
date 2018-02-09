# NeoTools
Python Tools to convert .png files into Arduino Font and Graphics formats we can display on NeoMatrix sheets

We are interested in transforming the contents of .png graphics or font files into a form that can be
use by simple Arduino sketches.     The font files that we have found are encoded with a palette, and
so the image representation is sufficiently compact.  However, some other sources (www.piskel.com, for
example, generate images with color planes in the pixel data).

Here we are creating some tools that will reduce the color planes to a palette and re-encode the array
representation of the planes as compact (4-bit) index values into the palette.

These values can then be imported into arduino sketches as simple arrays then displayed -- with the palette
representation applied just in the time that it is needed.

Also to be added here are tools that write/read a friendly representation to SD card so that the Arduino sketches
can read palette and image data easily and then display images/fonts as needed.

So far, I've framed the tasks as TDD (Test Driven Development) tasks, with most of the needed tests already
written.   It takes a lot of time, but it is a good methodology to learn, as it can really improve your code.

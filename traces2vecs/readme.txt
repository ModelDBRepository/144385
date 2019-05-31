This is the readme.txt for traces2vecs.py, a python program by Tom
Morse that hopefully conveniently converts traces from a paper figure
into NEURON vectors. 20120308.

SUMMARY:

First use idraw to manually create (by clicking) polylines (many point
lines) which trace over the curves you would like as vectors in
NEURON, saving this idraw file, and then secondly running
traces2vecs.py which will read the idraw file and create the NEURON
vector files.

DIRECTIONS:

To use idraw to prepare an input file for traces2vecs.py:

First be aware of these general directions for how-to make a polyline
in idraw:

In left panel of idraw, select e - polygon line.  Then:
left button adds a point
right button subtracts a point (use to remove accidental left click)
middle button ends the polyline.

Here we go:

1) File->Import your figure into idraw as a tif.  It may show up with
   teal background.

2) Enter in this order (the order is crucial): a) the axes by clicking
   three clicks, first on the upper y axis at an identified tic mark,
   second at the intersection of the axes, third at an identified tic
   mark at the far right on the x axis. (end this first
   polyline). These points will correspond to an axis_limits.dat file
   that you will create manually below.
   b) Enter polylines (many point lines-see above for how) for all traces.
3) Save the file from idraw with an id extension (for idraw).
4) create an axis_limits.dat file which has four lines:
   the max y value (the y value where your first click will be) 
   the min y value (the y value where your second click will be)
   the min x value (the x value where your second click will be)
   the max x value (the x value where your third click will be) 
   which are the paper's scale values.
5) If there is only one input file with extension id then
   traces2vecs.py will find if automatically, otherwise you will need
   to start supplying the name of the file created from idraw, say
   traced.id

./traces2vecs.py traced.id

If successful, the program will create traceX.dat, vectors files
suitable for reading into NEURON, where trace0.dat is the axes, and
trace1.dat, trace2.dat, ... are the traces your subsequently supplied with
mouse clicked polylines.

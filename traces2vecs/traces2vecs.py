#!/usr/bin/python
# traces2vecs.py
# This program is for converting traces in a graph to an approximation
# of those traces as vectors whose values are the values on the axes of 
# the figure.  It relies on the user having access to idraw (comes with
# NEURON).
# traces2vecs.py accepts as input a postscript file and writes either
# NEURON or matlab/octave style vectors of the traces in the graph.
# This postscript file is assumed to be the result of importing
# a research paper's figure (as a tif) into a new idraw figure and then
# editing the figure (using idraw) by selecting the polygon writing tool (e)
# and then left clicking to start and add points to a polygon, the right
# click will remove one or more accidental points from the line you are
# creating and the middle click supplies the end point for the line.
# When done tracing the curves in idraw, select file -> save and
# type or click a file name.  When the file is saved the pixel values
# of all the points will be written as text at the end of the file.
# The begining of the file will include the image that was imported.
# Important:
# The first three points you click will need to be the axis
# traces2vecs.py assumes that the first three points (at the end of the postscript
# file) delimit the axis by tracing
# the (x,y) points on the axis:
# (0, y_axis_extreme), (0,0), (x_axis_extreme,0)
# The order of the mouse clicks on the max y, (0,0), max x axis is important
# because the values of these points are user pre-supplied in a data file
# called axis_limits.dat whose first line is the x_axis_extreme and the second
# line is y_axis_extreme.  traces2vecs.py uses the linear transformation created
# by using axis_limits.dat and the pixel values recorded on the first three
# clicks.
# The output files are given the names traceX.dat where
# trace0.dat should reflect the values in axis_limits.dat and
# traceX with X from 1 to the number of traces are the subsequent traces.


""" usage:
 traces2vecs.py input.ps
 or
 traces2vecs.py input.id
 (it doesn't matter what the input file is called as long it's idraw output)
 Running assumes axis_limits.dat exists in the current dir and has four lines:
 the max y value (the yvalue where your first click will be)
 the min y value (the y value where your second click will be
 the min x value (the x value where your second click will be)
 the max x value (the x value where your third click will be)
 which are the paper's scale values.
"""

# note that the extreme points on the axis are called max below
# and that each point has an x,y value, e.g. the first point
#
# Variables with suffix pix are pixel values, otherwise they are
# the "graphed" values, i.e. correspond to the numbers on the graph tic marks or scales
#

import os
import sys
input_ps_name = ""
if (len(sys.argv)!=2):
  print "I notice no idraw output file was supplied as an argument - I will look later for one..."
else:
  input_ps_name = sys.argv[1]
  print input_ps_name
  #
  # read in the values from the axis limits file
  print("Opening "+input_ps_name +" for finding your manually entered")
  print("axis clicks (top y, origin, left x) and subsequent traces.\n")

fid=0 # file id for idraw file given global scope for later analysis

try:
  axis_limits_file = open( "axis_limits.dat","r")
except:
    print("Couldn't open axis_limits.dat file")
    print("This file needs to be in the current directory and")
    print("contains:\nthe max y value\nthe min y value\nthe min x value")
    print("the max x value\n(on seperate lines)\n")
    print("These user supplied numbers are the paper figures values corresponding to your")
    print("first three mouse clicks on the figure (high y axis, origin, far right x axis)")
    print("Then traces2vecs.py will use the pixel values as returned by idraw matched")
    print("to the above axis_limits user supplied data to transform the subsequent curves.")
    exit(1)

  # another possibility would be to use while (fgets(buf,1000, axis_limits_file)!=NULL) {}
axis_limits_array=axis_limits_file.readlines()

global y_axis_max_y, y_axis_min_y, x_axis_min_x, x_axis_max_x 
y_axis_max_y = eval(axis_limits_array[0])
y_axis_min_y = eval(axis_limits_array[1])
x_axis_min_x = eval(axis_limits_array[2])
x_axis_max_x = eval(axis_limits_array[3])

print("From axis_limits.dat:\n")
print("y_axis_max_y = "+str(y_axis_max_y)+"\ny_axis_min_y = "+str(y_axis_min_y)+\
  "\nx_axis_min_x = "+str(x_axis_min_x)+"\nx_axis_max_x = "+str(x_axis_max_x))

found_idraw_file=0 # 0 is false: set true if find an idraw file
if (len(sys.argv)>1):
  try:
    fid=open(sys.argv[1],"r")
    found_idraw_file=-1 # set true
  except:
    print("Couldn't open "+sys.argv[1]+" file")
    print("This file needs to be in the current directory/specified path")
    exit(1)
else:
  print "No idraw file supplied as input."
  print "I am going to look for an idraw file"
  files=os.listdir(".")
  for f in files:
    if (f[-3:]=='.id'):
      try:
        print "*** Found one!: Using "+f+" as idraw file (to read)."
        fid=open(f,"r")
        found_idraw_file=-1
      except:
        print("For some reason could not open an idraw file, "+f+", I found")
        exit(1)
      break
if (~found_idraw_file):
  print ("Wasn't supplied or couldn't find an idraw (.id) file in current directory.")
  exit(1)
# print 
start_position=0
file_data=fid.readlines()
for i in range(len(file_data)):
  # print "Checking: "+file_data[i]
  if file_data[i]=="Begin %I MLine\n":
    # print "found an MLine at line "+str(i)
    start_position=i
    break
yaxis_vecs=file_data[start_position+11] # the x,y pix vector of top of y axis
yaxis_vecs_array=yaxis_vecs.split(" ")
# print "start_position="+str(start_position)
# print yaxis_vecs_array
yaxis_xvec=eval(yaxis_vecs_array[0])
yaxis_yvec=eval(yaxis_vecs_array[1])
origin_vecs=file_data[start_position+12] # the x,y pix vector of top of y axis
origin_vecs_array=origin_vecs.split(" ")
origin_xvec=eval(origin_vecs_array[0])
origin_yvec=eval(origin_vecs_array[1])
xaxis_vecs=file_data[start_position+13] # the x,y pix vector of top of y axis
xaxis_vecs_array=xaxis_vecs.split(" ")
xaxis_xvec=eval(xaxis_vecs_array[0])
xaxis_yvec=eval(xaxis_vecs_array[1])
#
# now have the pixel values for the top y, origin, left x axes so
# need to combine them with the read-in figure scale values
#
print "Using your idraw 'first three clicks' line for the axis values:\n"
print "yaxis max: ",yaxis_xvec, ", ", yaxis_yvec
print "origin:    ",origin_xvec, ", ", origin_yvec
print "xaxis max: ",xaxis_xvec, ", ", xaxis_yvec

#x_fig = ((x_axis_max_x-x_axis_min_x)/(x_axis_pix_max - x_axis_pix_origin))*(x_pix - x_axis_pix_origin)
#y_fig = ((y_axis_max_y-y_axis_min_y)/(y_axis_pix_max - y_axis_pix_origin))*(y_pix - y_axis_pix_origin)

x_axis_pix_max = xaxis_xvec
x_axis_pix_origin = origin_xvec

y_axis_pix_max = yaxis_yvec
y_axis_pix_origin = origin_yvec

def x_pix2x_fig(x_pix):
  # converts a pixel x-coordinate to a figure x coordintate
  # note that without float below it is possible that integer arithmatic will corrupt the calculation
  return (float(x_axis_max_x-x_axis_min_x)/(x_axis_pix_max - x_axis_pix_origin))*(x_pix - x_axis_pix_origin)+x_axis_min_x

def y_pix2y_fig(y_pix):
  # note that without float below it is possible that integer arithmatic will corrupt the calculation
  return (float(y_axis_max_y-y_axis_min_y)/(y_axis_pix_max - y_axis_pix_origin))*(y_pix - y_axis_pix_origin)+y_axis_min_y

print "confirmation run of conversions x_pix2xfig, y_pix2y_fig:"
print "upper y axis: "+str(x_pix2x_fig(yaxis_xvec))+", "+str(y_pix2y_fig(yaxis_yvec))
print "graph origin: "+str(x_pix2x_fig(origin_xvec))+", "+str(y_pix2y_fig(origin_yvec))
print "right x axis: "+str(x_pix2x_fig(xaxis_xvec))+", "+str(y_pix2y_fig(xaxis_yvec))

# now use the transformation functions to create a list of traces, where each trace
# is a list of (x,y) points:
# [[[trace0_x_0, trace0_y_0], [trace0_x_1, trace0_y_1], ..., [trace0_x_n0, trace0_y_n0]],
#  [[trace1_x_0, trace1_y_0], [trace1_x_1, trace1_y_1], ..., [trace1_x_n1, trace1_y_n1]],
# ...
#  [[tracej_x_0, tracej_y_0], [tracej_x_1, tracej_y_1], ..., [tracej_x_nj, tracej_y_nj]]]
# where trace0 corresponds to the first three clicks being the axis (it is OK to add subsequent clicks
# to make a greater then three point line for this first trace, the zeroth trace.
#
#  There are n_j (nj) traces in all with the ith trace containing n_i (ni) points.

# count the number of traces
num_of_traces=0
trace_start_index=[] # a list of the indicies i of file_data[i] of the line
# before a trace starts.  Includes the line that contains the number of points in the format
# "
index=0
for d in file_data:
  if (d=="Begin %I MLine\n"):
    num_of_traces = num_of_traces + 1
    trace_start_index.append(index+10)
  index=index+1
#
# now ready to read in the traces
#
num_in_trace=[]
traces = []
current_trace=[]
# print "trace_start_index:"
# print trace_start_index
for index in trace_start_index:
  current_trace=[] # reinitialize the current trace
  # the number in the current trace
  # print "file_data[index][3:]="+file_data[index][3:]
  points_in_polyline=eval(file_data[index][3:])
  # for i in range(points_in_polyline):
  #   print "i = "+str(i)
  #   print file_data[index+1+i][:]
  num_in_trace.append(points_in_polyline) # gets the 6 from "%I 6\n"
  # get the traces
  for i in range(num_in_trace[-1]):
    current_vector=file_data[index+1+i]
    current_vector_array = current_vector.split(" ")
    current_vector_x = eval(current_vector_array[0])
    current_vector_y = eval(current_vector_array[1])
    vector_list_element = [current_vector_x, current_vector_y]
    current_trace.append(vector_list_element)
  # now add the trace to the list of traces
  traces.append(current_trace)
# the traces pixel list vectors have been created
# write them as NEURON vectors traceX.dat
for X in range(len(traces)): # iterate over the number of traces
  filename="trace"+repr(X)+".dat"
  file=open(filename,"w")
  file.write("label: trace"+repr(X)+"\n")
  file.write(repr(len(traces[X]))+"\n")
  for i in range(len(traces[X])):
    file.write(repr(x_pix2x_fig(traces[X][i][0]))+" "+repr(y_pix2y_fig(traces[X][i][1]))+"\n")
  file.close()


  


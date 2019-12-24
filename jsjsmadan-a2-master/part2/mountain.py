#!/usr/local/bin/python3
#
# Authors: [Jashjeet, Devansh, Sanyam - jsmadan,devajain,srajpal]
#
# Mountain ridge finder
# Based on skeleton code by D. Crandall, Oct 2019
#

from PIL import Image
from numpy import *
import numpy as np
from scipy.ndimage import filters
import sys
import imageio
from sklearn.preprocessing import normalize

# calculate "Edge strength map" of an image
#
def edge_strength(input_image):
    grayscale = array(input_image.convert('L'))
    filtered_y = zeros(grayscale.shape)
    filters.sobel(grayscale,0,filtered_y)
    return sqrt(filtered_y**2)

# draw a "line" on an image (actually just plot the given y-coordinates
#  for each x-coordinate)
# - image is the image to draw on
# - y_coordinates is a list, containing the y-coordinates and length equal to the x dimension size
#   of the image
# - color is a (red, green, blue) color triple (e.g. (255, 0, 0) would be pure red
# - thickness is thickness of line in pixels
#
def draw_edge(image, y_coordinates, color, thickness):
    for (x, y) in enumerate(y_coordinates):
        for t in range( int(max(y-int(thickness/2), 0)), int(min(y+int(thickness/2), image.size[1]-1 )) ):
            image.putpixel((x, t), color)
    return image

# main program
#
(input_filename, gt_row, gt_col) = sys.argv[1:]

# load in image 
input_image = Image.open(input_filename)

# compute edge strength mask
edge_strength = edge_strength(input_image)
imageio.imwrite('edges.jpg', uint8(255 * edge_strength / (amax(edge_strength))))

# You'll need to add code here to figure out the results! For now,
# just create a horizontal centered line.
ridge_blue=list(np.argmax(edge_strength, axis=0))

# output answer
imageio.imwrite("output_simple.jpg", draw_edge(input_image, ridge_blue, (0, 0, 255), 5))

def viterbi( input_image , ep , tp , init_dist ) :
    
    input_array = np.array( input_image )
    dims = input_array.shape[ 0 ]
    
    dimse = ep.shape[ 0 ]
    trans_array = np.zeros( ( dimse , dims ) )

    trans_array[ 0 , : ] = np.log( init_dist * tp[ : , 0 ] )
    
    arr = np.zeros( ( dimse - 1 , dims ) )
    
    for i in range(1, dimse):
        for j in range(1, dims):
            prob = trans_array[ i - 1 ][ j ] + np.log( ep[ i , : ] )
            arr[ i - 1 ][ j ] = np.argmax( prob )
            trans_array[ i ][ j ] = np.amax( prob )
    
    array_3 = np.zeros( dimse )
    
    final = np.argmax( trans_array[ 0 , : ] )
    array_3[ 0 ] = final
    
    a=1
    
    for i in range( 1 , dimse - 1 ) :
        array_3[ a ] = arr[ i , final ]
        final = np.argmax( arr[ i , : ] )
        a += 1
    answer = [ ]
    for i in array_3 :
        answer.append( i )
    return array_3








#input_image1 = Image.open(input_filename)
widthofimage=np.array(input_image).shape[0]
#edge_strength = edge_strength(input_image1)



t1 = [ ]
t2 = [ ]
for i in range( widthofimage ) :
    t1.clear( )
    for j in range( widthofimage ) :
        d = abs( i - j )
        if d<20:
            t1.append( i-j )
        else:
            t1.append( widthofimage )
    t2.append( list(t1 ) )   
tt1 = np.array( t2 )
tt2 = tt1 - widthofimage
tt2 *=- 1
#tp=tt2
tp = normalize( tt2 , axis = 1 , norm = 'l1' )



t1 = [ ]
t2 = [ ]
t1.clear( )
t2.clear( )
ridge=list(np.argmax(edge_strength, axis=0))

for i in ridge:
    t1.clear( )
    for j in range( widthofimage ) :
        d = abs( i-j )
        t1.append( d )
    t2.append( list( t1 ) )
    
tt = np.array( t2 )
tt1 = tt - widthofimage
tta = tt1*-1

#ep1=tta
ep1 = normalize( tta , axis = 1 , norm = 'l1' )

#ep2=np.array( edge_strength )
ep2 = normalize( np.array( edge_strength ) , axis = 1 , norm = 'l1' )
ep2 = ep2.T



init_dist = ep2[ 0 ]

answer1 = viterbi( np.array( edge_strength ) , np.array( ep1 ) , np.array( tp ) , init_dist )
answer2 = viterbi( np.array( edge_strength ) , np.array( ep2 ) , np.array( tp ) , init_dist )
answer=np.minimum( answer1 , answer2 )
#print( answer )
input_image1 = Image.open(input_filename)
imageio.imwrite("output_map.jpg", draw_edge(input_image1, answer , (255, 0, 0), 5))



gt_row=int(gt_row)
gt_col=int(gt_col)


ep1[ : , gt_col ] = 0
ep1[ gt_row , gt_col ] = 1

ep2[ : , gt_col ] = 0
ep2[ gt_row , gt_col ] = 1


ip = np.ones( ( widthofimage ) ) / widthofimage


answer1 = viterbi( np.array( edge_strength ) , np.array( ep1 ) , np.array( tp ) , ip )
answer2 = viterbi( np.array( edge_strength ) , np.array( ep2 ) , np.array( tp ) , ip )
answer=np.minimum( answer1 , answer2 )




input_image2 = Image.open(input_filename)
imageio.imwrite("output_human.jpg", draw_edge(input_image2, answer , (0, 255, 0), 5))


from __future__ import division
import random
import numpy 
import math
import prims1


def gen_array(dimensions,init_elem = 0):
    size = 1
    for d in dimensions: size = size * d
    a = numpy.array(prims1.n_of(size,init_elem)) 
    a.shape=tuple(dimensions)
    return a

def lists_to_array(lists):
    numrows = len(lists)
    numcols = len(lists[0])
    a = gen_array([numrows,numcols])
    for i in range(numrows):
	for j in range(numcols):
	    a[i][j] = lists[i][j]
    return a

def gen_vector(elems):
    return numpy.array(elems)

def randint_vector(size,a,b):
    ints = numpy.ones(size)
    for i in range(size): ints[i] = random.randint(a,b)
    return ints  # return map((lambda a1: a1 * random.randint(a,b)), ints) converted array to list

def vector_avg(vect):
    sum = 0
    for i in range(len(vect)):
	sum += vect[i]
    return sum/len(vect)



def array_swap(a1,a2,index1,index2):
    temp = a1[index1:index2].copy()
    a1[index1:index2] = a2[index1:index2]
    a2[index1:index2] = temp

def array_crossover(a1,a2,num_cross_pts):
    cross_pts = random.sample(range(1,len(a1)-1),num_cross_pts)
    cross_pts.sort()
    if len(cross_pts) % 2 == 0: cross_pts.append(len(a1)-1) # Add len-1 to end of pts list when size was even.
    cross_pts.insert(0,0)  # Add 0 to front.
    c1 = a1.copy()
    c2 = a2.copy()
    while len(cross_pts) > 1:
	pt1 = cross_pts.pop(0) # need 0 to pop from front, since default is back
	pt2 = cross_pts.pop(0)
	array_swap(c1,c2,pt1,pt2)
    return[c1,c2]

# This assumes that the bits are arranged least-significant first
def bitarray_to_integer(bits):
    sum = 0
    for b in range(len(bits)-1,-1,-1):
	sum = sum*2 + bits[b]
    return sum

def integer_to_bitarray(int, min_size = False):
    remains = int
    bits = []
    while remains > 0:
	bits.append(remains % 2)
	remains = remains // 2
    if min_size: # pad with zeros
	for i in range(min_size - len(bits)): bits.append(0)
    return bitarray.bitarray(bits)
	
# This maps func to the array, but returns a list
def do_2d_array(a, func):
    return map((lambda row: map(func, row)), a)

# This maps func to the array and returns an array of results
def map_array_2d(a,func):
    rows,cols = a.shape
    a2 = gen_array(a.shape,init_elem = apply(func, [a[0,0]])) # taking init_elem from a insures that correct type of array is created.
    for i in range(rows):
	for j in range(cols):
	    a2[i,j] = apply(func,[a[i,j]])
    return a2

def transpose_array(a):
    rows,cols = a.shape
    a2 = gen_array((cols,rows), init_elem = a[0,0])
    for i in range(rows):
	for j in range(cols):
	    a2[j,i] = a[i,j]
    return a2
	       

# types are: sum, max, const
# This is not as elegant as Lisp, because python doesn't seem to wrap a lexically-scoped
# environment around lambda funcs.  So I can't call do_2d_array to find the sum or max of the array.

def normalize_array_2d(a, type = 'sum', const = 1.0):
    if type == 'sum' or type == 'max':
	cache = 0.0
	if type == 'max': cache = -99999999999.0
	rows,cols = a.shape 
	for i in range(rows):
	    for j in range(cols):
		if type =='sum':
		    cache += a[i,j]
		elif type =='max':
		    cache = max(cache,a[i,j])
    elif type == 'const': # Just divide by a constant => no need for summing or finding the max
	cache = const
    if cache <> 0:
	cache = float(cache)
	return map_array_2d(a,(lambda val: val/cache))


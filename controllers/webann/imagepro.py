# For simple image-processing operations on python "Image" objects

import Image
import ImageFilter
import math
import kd_array

# These fetch the red, green or blue components of an RGB triple.  A normal Image
# pixel is an RGB triple, whereas the black-white and grayscale images have scalar pixels.


def get_red(image,x,y): return image.getpixel((x,y))[0]
def get_scaled_red(image,x,y,maxval = 256.0): return get_red(image,x,y) / maxval
def get_red_image(image): return image.split()[0]

def get_green(image,x,y): return image.getpixel((x,y))[1]
def get_scaled_green(image,x,y,maxval = 256.0): return get_green(image,x,y) / maxval
def get_green_image(image): return image.split()[1]

def get_blue(image,x,y): return image.getpixel((x,y))[2]
def get_scaled_blue(image,x,y,maxval = 256.0): return get_blue(image,x,y) / maxval
def get_blue_image(image): return image.split()[2]

# Here, we fetch pixel values from black-white and grayscale images

# For grayscale images (mode = 'L'), each value is a simple 8-bit integer
def get_gray(image,x,y): return image.getpixel((x,y))
def get_scaled_gray(image,x,y,maxval = 256.0): return get_gray(image,x,y) / maxval

def get_bw(image,x,y): return image.getpixel((x,y)) # Returns either 255 (white) or 0 (black)

# This returns all the image pixels in one big list.

def image_list(image): return list(image.getdata())

# This compares two pixels and computes the mean square error between them.  For RGB images, these
# pixels are triples, whereas black-white or grayscale pixels consist of scalar values. 

def pixel_error(p1,p2, vector = True):
   if vector:
      return  math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2)
   else:
      return abs(p1 - p2)

# This calculates an average pixel over an entire image.

def avg_color(image, vector = True):
   if vector:
      return avg_rgb(image)
   else:
      return avg_scalar_color(image)

# Calc avg r, g and b values over an entire image.
def avg_rgb(image):
    x,y = image.size
    total = float(x*y)
    sum_r, sum_g, sum_b = 0.0, 0.0, 0.0
    for i in range(x):
	for j in range(y):
	    r,g,b = image.getpixel((i,j))
	    sum_r, sum_g, sum_b = sum_r + r, sum_g + g, sum_b + b
    return [sum_r/total, sum_g/total, sum_b/total]

# For scalar pixels
def avg_scalar_color(image):
    x,y = image.size
    total = float(x*y)
    sum = 0.0
    for i in range(x):
	for j in range(y):
	    sum += image.getpixel((i,j))
    return sum/total

# Returns an array of average band strengths, one per column.  band = red, green, blue, gray or bw(black-white)
def column_avg(image,band='red',y_scope_to=1,y_scope_from=0):
   """
    Extended with scope settings for Y-axis.
   """
   x,y = image.size
   func = eval("get_"+band)
   a = kd_array.gen_array([x], init_elem = 0.0)
   for i in range(x):
      sum_band = 0
      from_ = int(math.ceil(y*y_scope_from))
      to_ = int(math.floor(y*y_scope_to))
      for j in range(from_, to_):
         sum_band += func(image,i,j)
      a[i] = float(sum_band)/float(to_-from_)
   return a


def image_avg(image,band='red',scale = 1.0):
   return kd_array.vector_avg(column_avg(image,band=band)) / scale

def scaled_column_avg(image,band='red',scale=256.0, target = 0.0, scaler = (lambda x, targ: x - targ)):
   a = column_avg(image,band=band)
   # print "column avgs: ", a
   for i in range(a.size): a[i] = apply(scaler, [a[i]/scale , target])
   return a

# Apply func to each R,G,B triple of the image, returning an array of whatever type that func returns.
# Note: Image module includes an "eval" method, which is similar, but it's function must take
# a single argument and will be applied to each color band in each pixel.
def map_image(image,func):
    x,y = image.size
    a = kd_array.gen_array((x,y), init_elem = apply(func, [image.getpixel((0,0))]))
    for i in range(x):
	for j in range(y):
	    a[i,j] = apply(func, [image.getpixel((i,j))])
    return a

def split_list(li,columns):
    length = len(li)
    return [(sum(li[i*length // columns: (i+1)*length // columns])/(len(li)/columns)) for i in range(columns) ]

def process_snapshot(image,columns=5,color='red'):

    cut_top = .4
    cut_bot = .6

    avg_red = column_avg(image,'red',y_scope_from=cut_top,y_scope_to=cut_bot)
    avg_green= column_avg(image,'green',y_scope_from=cut_top,y_scope_to=cut_bot)
    avg_blue = column_avg(image,'blue',y_scope_from=cut_top,y_scope_to=cut_bot)

    diff = []
    for i in range(len(avg_red)):

      if color == 'red':
        f = (max(0, min(1, ((avg_red[i] - ((avg_blue[i] + avg_green[i]) / 2)) / 90))))
      elif color == "green":
        f = (max(0, min(1, ((avg_green[i] - ((avg_blue[i] + avg_red[i]) / 2)) / 90))))
      else:
        f = (max(0, min(1, ((avg_blue[i] - ((avg_green[i] + avg_red[i]) / 2)) / 90))))

      diff.append(f)

    # diff = [max(0, ((avg_red[i]*rf)+(avg_green[i]*gf)+(avg_blue[i]*bf))/255.0)for i,j in enumerate(avg_red)]
    output = split_list(diff,columns)
    return output


from __future__ import division
import random
import numpy 
import math
import time
import re # For handling regular expressions


def protected_div(x,y):
    if y == 0.0:
	return 0.0
    else: return x / y

def kdwait(self, seconds = 1.0):
      time.sleep(seconds)

def set_slot(obj,slot_name,value):
    setattr(obj,slot_name,value)

def get_slot(obj,slot_name):
    return getattr(obj,slot_name)

def find_list_item(L,item,key=(lambda x: x)):
    for x in L:
	if item == key(x):
	    return x

def find_list_satisfier(L,pred):
    for x in L:
	if pred(x): return x
    return None

def boolean_true_p(x): return (isinstance(x,bool) and x)
def boolean_false_p(x): return (isinstance(x,bool) and not(x))

def forall(L,pred):
    for item in L:
	if not(pred(item)): return False
    return True

def exists(L,pred):
    for item in L:
	if pred(item): return True
    return False

def number_list_p(L):
    return type(L) == list and forall(L,(lambda x: type(x) in [int,float]))

def normalize_list(elems):
    s = sum(elems)
    if s <> 0:
      return [elem/s for elem in elems]
    else: return []

def general_sum(elems,prop_func=(lambda x: x)):
    return sum(map(prop_func,elems))

def general_avg(elems,prop_func=(lambda x: x)):
    if elems:
	return sum(map(prop_func,elems))/len(elems)

def general_variance(elems,prop_func=(lambda x: x),avg = None):
    if not(avg): avg = general_avg(elems,prop_func=prop_func)
    if len(elems) > 1:
	sum = 0
	for elem in elems:
	    sum += (prop_func(elem) - avg)**2
	return (sum / len(elems))
    else: return 0

def general_stdev(elems,prop_func=(lambda x: x),avg = None):
    return math.sqrt(general_variance(elems,prop_func=prop_func,avg=avg))

def logistic(x,k):
    return 1 / (1 + math.exp(k - x))

def n_of(count,item): return [item for i in range(count)]

def num_satisfiers(elems,predicate):
    count = 0
    for elem in elems:
	if predicate(elem): count += 1
    return count

# Find the positions of all elems that satisfy the predicate
def pos_satisfiers(elems,predicate):
    positions = []
    for i in xrange(len(elems)):
	if predicate(elems[i]): positions.append(i)
    return positions

# Gens a number cycle, starting at a, going (up or down) to b, and then back to a.  If size is even, b is repeated in
# the middle of the list.

def gen_cycle(a,b, size):
    mid = int(round(size/2.0) - 1)
    dx = (b - a)/mid
    elems = []
    for i in range(mid + 1):
	elems.append(a + i*dx)
    if (mid+1)*2 == size: start = 0
    else: start = 1
    for j in range(start,mid + 1):
	elems.append(b - j*dx)
    return elems
	
def biased_coin_toss(prob = .5):
    if random.uniform(0,1) <= prob:
	return True
    else: return False

def randab(a,b):
    return a + (b - a)*random.uniform(0,1)

def randelem(elems):
    return elems[random.randint(0,len(elems)-1)]

def stochpick(elems,prop_func=(lambda x: x), sum = 0):
    if sum == 0: sum = general_sum(elems,prop_func)
    randnum = random.uniform(0,sum)
    running_sum = 0
    for elem in elems:
	running_sum += prop_func(elem)
	if running_sum >= randnum: return elem

def stochpick_subset(elems, subset_size, prop_func=(lambda x: x)):
    items = list(elems)  # copies the elems list
    subset = []
    sum = general_sum(elems,prop_func)
    for i in range(subset_size):
	item = stochpick(items,prop_func,sum=sum)
	sum = sum - prop_func(item)
	subset.append(item)
	items.remove(item)
    return subset

 # The python manual says that it is faster to sort in ascending order (the default) and then
# do a reverse afterwards, as opposed to sorting by a different comparator function.

def kd_sort(elems, prop_func = (lambda x: x), dir = 'increase'):
    elems.sort(key=prop_func) # default of the sort func is increasing order
    if dir =='decrease' or dir =='decr':
	elems.reverse()

def partition(elems, prop_func = (lambda x:x), eq_func = (lambda x,y: x == y)):
    kd_sort(elems,prop_func=prop_func)
    partition = []
    subset = False
    last_key = False
    counter = 0
    for elem in elems:
	new_key = apply(prop_func, [elem])
	if not(subset) or last_key <> new_key:
	    if subset: partition.append(subset)
	    subset = [elem]
	    last_key = new_key
	else: subset.append(elem)
    if subset: partition.append(subset)
    return partition

def sorted_partition(elems,elem_prop = (lambda x:x), subset_prop = (lambda ss: len(ss)), eq_func = (lambda x,y: x ==y), dir = "decrease"):
	p = partition(elems,prop_func = elem_prop, eq_func = eq_func)
	kd_sort(p,prop_func = subset_prop,dir = dir)
	return p


# Loads in all lines of a file

def load_file_lines(fid):
    return [line.rstrip() for line in open(fid,'r').readlines()]
  # rstrip strips the newline character

# Split a list at the target item

def split_at (L, target, include = False):
    first_half =[]
    while L and L[0] != target:
	first_half.append(L[0])
        L = L[1:] # cdr
    if L:
        second_half = {True: L, False: L[1:]}[include]
	return [first_half,second_half]
    else:
	return[first_half,[]]

def split_at_sat(L,predicate, include = False):
    first_half =[]
    while L and not(apply(predicate,L[0:1])):
	first_half.append(L[0])
	L = L[1:] # cdr
    if L:
        second_half = {True: L, False: L[1:]}[include]
	return [first_half,second_half]
    else:
	return[first_half,[]]

# Detect keyword strings as those beginning with a colon (as in Lisp) and as done in ann-topology files
def keyword_p(str): return  str[0] == ":" 
def strip_keyword_colon(str): return str[1:]

 # Substitute underscores for hyphens, but only hyphens that come after an alphanumeric.  Those that
# come before an alphanumeric are considered minus signs and left as is.

def replace_hyphens(strings):
   return [re.sub(r'(\w+)-',r'\1_',s) for s in strings]

# This replaces all question marks at the end of symbols by "_p", as only the latter is an acceptable argument name in python.
# E.g., the argument 'empty?' is changed to 'empty_p'.
def replace_question_marks(strings):
   return[re.sub(r'(\w+)\?( |$)',r'\1_p\2',s) for s in strings]

# This bundles up keyword-value pairs into a dictionary, which Python can then use directly in calls to functions
# with default (keyword) arguments.

def bundle_keyword_args (arguments):
    dict = {}
    while arguments and keyword_p(arguments[0]):
	dict[strip_keyword_colon(arguments[0])] = arguments[1]
	arguments = arguments[2:]
    return dict
  
    
# **** Trigonometry

def kd_atan(dx, dy):
    if dx == 0: 
	return (math.pi / 2.0)
    else:
	return math.atan(dy/dx)

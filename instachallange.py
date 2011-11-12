# /usr/bin/python

### UNSHREDDER

# Solution regarding:
# http://instagram-engineering.tumblr.com/post/12651721845/instagram-engineering-challenge-the-unshredder
# author: Max Brauer
# requires PIL and NumPy

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def mostCommon(l):
	"""
	Find the most common element in a list.
	"""
	d = {}
	for i in l:
		if i in d:
			d[i] += 1
		else:
			d[i] = 1
	return sorted(d, key = d.get, reverse = True)[0]

def columnWidth(shred):
	"""
	Returns the column width of each column given
	a shredded image.
	"""
	# this where the bonus challenge could be solved
	# but until then simply return fixed 32
	# return 32
	#
	# BONUS CHALLENGE
	x = map(np.sum, reduce(lambda x,y: x+y, shred.astype(float)))
	x = np.abs(np.diff(x))
	x /= np.max(np.abs(x),axis=0)
	x[x<.2]=0
	x = np.diff(np.nonzero(x)[0])
	return mostCommon(x)

def findMatch(column, othercolumns, left):
	"""
	Find the best left or right side match for a given column from a list of
	other columns. If param 'left' is True look for a left side match other
	wise right side.
	"""
	# set indizes according to left or right side
	if left:
		firstindex = 0
		secondindex = -1
	else:
		firstindex = -1
		secondindex = 0
	# compute euclidean distances between the column and all other columns
	dists = [np.linalg.norm(column[:,firstindex] - c[:,secondindex]) for c in othercolumns]
	# get the index of the 'nearest' column
	minindex = np.argmin(dists)
	# return the distance to that column and it's index regarding 'othercolumns'
	return dists[minindex], minindex

def bestRMatch(column, othercolumns):
	"""
	Returns the best right-side match of a given column and
	all other columns as an index on 'othercolumns'.
	Basically interfaces to findMatch.
	"""
	return findMatch(column, othercolumns, left=False)	

def bestLMatch(column, othercolumns):
	"""
	Returns the best left-side match of a given column and
	all other columns as an index on 'othercolumns'.
	Basically interfaces to findMatch.
	"""
	return findMatch(column, othercolumns, left=True)	

def bestMatch(column, othercolumns):
	"""
	Returns the best match for a column from a given list of
	columns. If neither right nor left side match is better,
	return the right side match.
	"""
	# get the best left side match and it's euclidean distance
	ldist, lmatch = bestLMatch(column, othercolumns)
	# same for the right hand side
	rdist, rmatch = bestRMatch(column, othercolumns)
	# return the better/ the one with the smaller
	# euclidean distance
	if ldist < rdist:
		return lmatch, 'l'
	return rmatch, 'r'

def match(column, othercolumns):
	"""
	Match a column to another given a list of other columns
	by glueing them together accordingly. Returns a list
	of the new piece and the rest of columns.
	"""
	# get the best match for the column
	matchidx, side = bestMatch(column, othercolumns)
	# pop that best match from the othercolumns list
	matchcolumn = othercolumns.pop(matchidx)
	# depending on the side merge those two columns
	if side == 'l':
		glued = np.hstack((matchcolumn, column))
	elif side == 'r':
		glued = np.hstack((column, matchcolumn))
	# return a list containing all remaining pieces)
	return othercolumns, glued

if __name__ == '__main__':
	# read the image
	# shred = np.asarray(Image.open('./TokyoPanoramaShredded.png'))
	shred = np.asarray(Image.open('./sample_shredded.png'))
	# determine the number of columns
	cwidth = columnWidth(shred)
	print 'estimated column width %s' % cwidth
	nocolumns = shred.shape[1]/cwidth
	# get the columns
	columns = np.split(shred, nocolumns, axis=1)
	# match piece by piece until only on whole remains
	while len(columns) > 1:
		column = columns.pop(0)
		othercolumns, glued = match(column, columns)
		othercolumns.append(glued)
		columns = othercolumns
	# save result
	Image.fromarray(columns[0]).save('./result.png')

	#x = map(np.sum, reduce(lambda x,y: x+y, shred.astype(float)))
	#x = np.abs(np.diff(x))
	#x /= np.max(np.abs(x),axis=0)
	#x[x<.2]=0
	#plt.scatter(x])

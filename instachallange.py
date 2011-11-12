# /usr/bin/python

### UNSHREDDER

# Solution regarding:
# http://instagram-engineering.tumblr.com/post/12651721845/instagram-engineering-challenge-the-unshredder
# author: Max Brauer
# requires PIL and NumPy

from PIL import Image
import numpy as np

def columnWidth(shred):
	"""
	Returns the column width of each piece.
	"""
	# this where the bonus challenge could be solved
	# but until then simply return fixed 32
	return 32

def findMatch(column, othercolumns, left):
	"""
	Find the best left or right side match for a given column and a list of
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
	
	ldist, lmatch = bestLMatch(column, othercolumns)
	rdist, rmatch = bestRMatch(column, othercolumns)
	if ldist < rdist:
		return lmatch, 'l'
	return rmatch, 'r'

def match(column, othercolumns):
	matchidx, side = bestMatch(column, othercolumns)
	print 'matching with %s on %s' % (matchidx, side) 
	matchcolumn = othercolumns.pop(matchidx)
	if side == 'l':
		glued = np.hstack((matchcolumn, column))
	elif side == 'r':
		glued = np.hstack((column, matchcolumn))
	return othercolumns, glued

shred = np.asarray(Image.open('./TokyoPanoramaShredded.png'))
columns = np.split(shred, 20, axis=1)

while len(columns) > 1:
	column = columns.pop(0)
	othercolumns, glued = match(column, columns)
	othercolumns.append(glued)
	columns = othercolumns

Image.fromarray(columns[0]).save('./result.png')

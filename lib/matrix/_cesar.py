from math import *
from random import*
import numpy as ny
import scipy as sp

seed()

class Higham(Exception):
    pass


def pdtoep(n, m=None, w=None, theta=None):
   
    if m is None:
        m = n

    if w is None:
        w = ny.random.rand(m)

    if theta is None:
        theta = ny.random.rand(m)

    try:
        if ny.max(w.shape) != m or ny.max(theta.shape) != m:
            raise Higham('Arguments w and theta must be vectors of length M.')
    except:
        raise Higham('Arguments w and theta must be vectors of length M.')

    t = ny.zeros(n)
    e = 2 * ny.pi * (ny.outer(ny.arange(1, n + 1), ny.ones(n)) -
                     ny.ones(n) * ny.arange(1, n + 1))

    for i in range(m):
        t = t + w[i] * ny.cos(theta[i] * e)

    return t



def chebspec(n, k=0):

    if k == 1:
        n += 1

    n = n - 1
    c = ny.zeros((n + 1, n + 1))

    one = ny.ones(n + 1)
    x = ny.cos(ny.arange(0, n + 1) * (ny.pi / float(n)))
    d = ny.ones(n + 1)
    d[0] = 2
    d[n] = 2

    # np.eye(n + 1) in next expression avoids div by zero.
    c = ny.outer(d, (one / d)) / (ny.outer(x, one) -
                                  ny.outer(one, x) + ny.eye(n + 1))

    #  Now fix diagonal and signs.
    c[0, 0] = (2 * n ** 2 + 1) / 6.0
    for i in range(1, n + 1):
        if ((i + 1) % 2) == 0:
            c[:, i] = -c[:, i]
            c[i, :] = -c[i, :]

        if i < n:
            c[i, i] = -x[i] / (2 * (1 - x[i] ** 2))
        else:
            c[n, n] = -c[0, 0]

    if k == 1:
        c = c[1::, 1::]

    return c



def matrice_random(n,borne):
	"""int*int->list(list(complex))"""

	res = [[0 for j in range(n)]for i in range(n)]
	for i in range(n) : 
		for j in range(n) : 
			res[i][j] = complex(randint(-borne,borne),randint(-borne,borne))
	return res

def matrice_top(n):
	a = complex(0,0)
	b = complex(0,0)
	c = complex(1/2,1/8)
	d = complex(1,0)
	e = complex(0,0)
	res = [[0 for j in range(n)]for i in range(n)]
	for i in range(n) : 
		for j in range(n) : 
			if(i==j ):
				res[i][j] = a
			elif(i == j-1):
				res[i][j] = b
			elif(i == j+1):
				res[i][j] = c
			elif(i == j-2):
				res[i][j] = d
			elif(i==j+2):
				res[i][j] = e
			else:
				res[i][j] = complex(0,0)
	return res


def matrice_top4(n):
	p = uniform(0,1)
	a =  complex(0,0)
	b =  complex(-p,0)
	c =  complex(-p,0)
	d =  complex(p,0)
	e =  complex(-p,0)
	f =  complex(p,0)
	g =  complex(p,0)
	res = [[0 for j in range(n)]for i in range(n)]
	for i in range(n) : 
		for j in range(n) : 
			if(i==j ):
				res[i][j] = a
			elif(i == j-1):
				res[i][j] = b
			elif(i == j+1):
				res[i][j] = c
			elif(i == j-2):
				res[i][j] = d
			elif(i==j+2):
				res[i][j] = e
			elif(i==j-3):
				res[i][j] = f
			elif(i==j+3):
				res[i][j] = g
			else:
				res[i][j] = complex(0,0)
	return res

def matrice_top5(n):
	a = complex(0,0)
	b = complex(0,0)
	c = complex(0,0)
	d = complex(0,0)
	e = complex(1,0)
	f = complex(1/2,0)
	g = complex(0,0)
	res = [[0 for j in range(n)]for i in range(n)]
	for i in range(n) : 
		for j in range(n) : 
			if(i==j ):
				res[i][j] = a
			elif(i == j-1):
				res[i][j] = b
			elif(i == j+1):
				res[i][j] = c
			elif(i == j-2):
				res[i][j] = d
			elif(i==j+2):
				res[i][j] = e
			elif(i==j-3):
				res[i][j] = f
			elif(i==j+3):
				res[i][j] = g
			else:
				res[i][j] = complex(0,0)
	return res

def matrice_top3(n):
	a = complex(0,0)
	b = complex(1,0)
	c = complex(0,0)
	d = complex(0,0)
	e = complex(1/2,0)
	res = [[0 for j in range(n)]for i in range(n)]
	for i in range(n) : 
		for j in range(n) : 
			if(i==j ):
				res[i][j] = a
			elif(i == j-1):
				res[i][j] = b
			elif(i == j+1):
				res[i][j] = c
			elif(i == j-2):
				res[i][j] = d
			elif(i==j+2):
				res[i][j] = e
			else:
				res[i][j] = complex(0,0)
	return res
def matrice_top2(n):
	a = complex(1,0)
	b = complex(-1,0)
	res = [[0 for j in range(n)]for i in range(n)]
	for i in range(n) : 
		for j in range(n) : 
			if(i==j or i==j-1 or i==j-2 or i==j-3 ):
				res[i][j] = a
			elif(i==j+1):
				res[i][j] = b
			else:
				res[i][j] = complex(0,0)
	return res


def smoke(n, k=0):

    w = ny.exp(2 * ny.pi * 1j / n)
    a = (ny.diag(ny.hstack((w ** ny.arange(1, n), 1))) +ny.diag(ny.ones(n - 1), 1))
    if k == 0:
        a[n - 1, 0] = 1

    return a

def riemann(n):
	n = n + 1
	i = np.outer(np.arange(2, n + 1), np.ones(n - 1))
	j = i.T
	a = np.where(np.remainder(j, i) == 0, i, -1)
	return a

def hilb(n,m=0):
	if (n == 1 and (m == 0 or m == 1)):
		return np.array([[1]])
	elif m == 0:
		m = n

	v = np.arange(1, n + 1) + np.arange(0, m)[:, np.newaxis]
	return 1. / v

def matrice_fibo(n):
	res = [[0 for j in range(n)]for i in range(n)]
	for i in range(n) : 
		for j in range(n) : 
			if(i>=j):
				res[i][j]=complex(0,0)
			else:
				res[i][j] = complex(0,0)
				while(res[i][j].real == 0):
					res[i][j] = complex(randint(-1,2),0)
	while(res[n-1][0].real == 0):
		res[n-1][0] = complex(randint(-1,2),0)
	return res

def affiche_matrice(M,n):
	"""list(list(complex))*int->void"""
	for i in range(n):
		print()
		for j in range(n):
			if(M[i][j].real == 0):
				print("   ",end = '')
				print(M[i][j] , end = '')
				print("   ",end = '')
			elif(M[i][j].real == -1):
				print(M[i][j] , end = '')
				print(" ",end = '')
			else :
				print(M[i][j] , end = '')
				print("  ",end = '')
	print()


	
def top3(n):
	r = []
	for a in range(1,n+1):
		r.append(-complex(0,1)/a)
	c = [-complex(0,1)]
	c.append(pi)
	for a in range(1,n-1):
		c.append(complex(0,1)/a)

	return sp.linalg.toeplitz(c,r=r)

def gearm(n, i=None, j=None):
#nice
    if i is None:
        i = n - 1
        j = -(n - 1)

    if not(abs(i) < n and abs(j) < n):
        raise ValueError('Invalid i and j parameters')

    a = np.diag(np.ones(n - 1), -1) + np.diag(np.ones(n - 1), 1)
    a[0, np.abs(i)] = np.sign(i)
    a[n - 1, n - 1 - np.abs(j)] = np.sign(j)

    return a

def frank(n, k=0):
    #nice
    f = np.ones((n, n)) * np.arange(n, 0, -1)
    f = np.minimum(f, f.T)
    #   take upper Hessenberg part.
    f = np.triu(f, -1)
    if k == 1:
        f = f[::-1, ::-1].T
    return f
class Higham(Exception):
    pass


def invhess(x, y=None):
#nice
    try:
        n = np.max(x.shape)
    except AttributeError:
        n = x
        x = np.arange(1, n + 1)
        y = -1 * x

    a = np.outer(np.ones(n), x)
    for j in range(1, n):
        a[:j - 1, j] = y[:j - 1]

    return a


def ohess(x):
#nice
    if type(x) == int:
        n = x
        x = np.random.uniform(size=n - 1) * 2 * np.pi
        h = np.eye(n)
        h[n - 1, n - 1] = np.sign(np.random.randn())
    elif type(x) == numpy.ndarray:
        if np.imag(x).any():
            raise Higham('Parameter must be real.')
        n = np.max(x.shape)
        h = np.eye(n)
        # Second term ensures h[n-1, n-1] nonzero.
        h[n - 1, n - 1] = np.sign(x[n - 1]) + float(x[n - 1] == 0)
    else:
        raise Higham('Unknown type in ohess')        
        
        
    for i in range(n - 1, 0, -1):
        # Apply Givens rotation through angle x[i - 1]
        theta = x[i - 1]
        c = np.cos(theta)
        s = np.sin(theta)
        h[i - 1:i + 1, :] = np.vstack((c * h[i - 1, :] + s * h[i, :],-s * h[i - 1, :] + c * h[i, :]))
    return h
def redheff(n):
#ok
    i = np.outer(np.arange(1, n + 1), np.ones(n))
    a = np.where(np.remainder(i.T, i) == 0, 1, 0)
    a[:, 0] = np.ones(n)

    return a

def triw(n, alpha=-1, k=0):
#bof
    try:
        m, n = n
    except TypeError:
        m = n

    if k == 0:
        k = n - 1

    if np.array(alpha).size != 1:
        raise Higham("Second Argument Must Be A Scalar.")

    t = np.tril(np.eye(m, n) + alpha * np.triu(np.ones((m, n)), 1), k)

    return t

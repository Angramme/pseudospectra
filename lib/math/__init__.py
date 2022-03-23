import numpy as np
import math

def ssvd_min(A):
    # TODO: find a faster implementation
    _, s, _ = np.linalg.svd(A)
    return np.min(s)

def svd_min(A):
    # TODO: find a faster implementation
    u, s, v = np.linalg.svd(A)
    i = np.argmin(s)
    # return u[i, :], s[i], v[:, i]
    return u[:, i], s[i], v[i, :]

def segment_point_distance(a, b, z):
    l2 = (a.real-b.real)**2 + (a.imag-b.imag)**2
    if l2 == 0.0: return np.abs(z, a)
    t = max(0, min(1, np.dot(z - a, b - a) / l2))
    projection = a + t * (b - a); 
    return np.abs(z - projection)

def gershgorin(A, eps):
    lb = +math.inf # left bound
    rb = -math.inf # right bound
    tb = -math.inf # top bound
    bb = +math.inf # bottom bound

    n, _ = A.shape
    sqrtn = np.sqrt(n)

    for i in range(n):
        a = A[i, i]
        rA = np.sum(np.abs(A[i])) - np.abs(A[i, i])
        # r = nsqrt * eps + rA
        r = sqrtn * eps + rA
        lb = min(lb, a.real-r)
        rb = max(rb, a.real+r)
        bb = min(bb, a.imag-r)
        tb = max(tb, a.imag+r)

    return lb, rb, bb, tb


class SegmentGrid():
    def __init__(self, lb, rb, bb, tb, gs, max_eps_dist):
        self.max_eps_dist = max_eps_dist

        self.lb, self.rb, self.bb, self.tb = lb, rb, bb, tb
        self.w, self.h = rb-lb, tb-bb
        self.gs = gs
        self.cw, self.ch = math.ceil(self.w/gs), math.ceil(self.h/gs)
        
        self.__grid = [[self.__make_cell() for y in range(self.ch)] for x in range(self.cw)]

    def __check_cell(self, cell, z):
        for B in cell:
            # iterate over bound segments
            for i in range(len(B)-1):
                a = B[i]
                b = B[i+1]
                if segment_point_distance(a, b, z) < self.max_eps_dist: return True
        return False

    def __make_cell(cell):
        return []

    def get_cell_xy(self, z):
        x = int((z.real - self.lb)/self.gs)
        y = int((z.imag - self.bb)/self.gs)
        x = max(0, min(x, self.cw-1))
        y = max(0, min(y, self.ch-1))
        return (x, y)

    def get_cell(self, z):
        i, j = self.get_cell_xy(z)
        return self.__grid[i][j]

    def is_segment(self, z):
        cell = self.get_cell(z)
        return self.__check_cell(cell, z)

    def insert_segment(self, seg):
        ccell = self.get_cell_xy(seg[0])
        last_i = 0
        for i in range(len(seg)-1):
            a = seg[i]
            b = seg[i+1]
            ncell = self.get_cell_xy(b)
            if ccell != ncell:
                self.__grid[ccell[0]][ccell[1]].append(seg[last_i:i+1])
                last_i = i
                ccell = ncell
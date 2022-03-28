########### code python Gershgorin ##############

from sympy import *
from numpy import linalg #permet le calcul des valeurs propres d'une matrice 
import numpy as ny
from random import randint 
from pylab import *
from tkinter import * #pour tracer des cercles entre autres
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
from math import *
import easygui as eg
import sys
import time

###### create random matrix ########

def matrice(n):
    M=[[0 for j in range(0,n)]for i in range(0,n)]

    for i in range(0,n):
        for j in range(0,n):
            M[i][j]=complex(randint(0,10),randint(0,10))#genere des nombres aleatoires de 1 a 10  
    return(M)

if len(sys.argv) >3:
    sys.argv[1], sys.argv[2],sys.argv[3] #pour n, eps et le pas 
else:
    if len(sys.argv)>2:
        sys.argv[1],sys.argv[2]
    else:
        print("pb")


###### variables globales ####                                                                                                

pas=sys.argv[3]
M=matrice(int(sys.argv[1]))


##### calcule ses valeurs propres ############
#Pour calculer les valeurs propres on va faire appel a la fonction linalg de numpy

valeurs_p,vecteurs=linalg.eig(M)

##########On applique le theoreme de gershgorin au pseudospectre afin de renvoyer les valeurs maximales que prennent x et y ###########

#1.utilisation gershgorin (il faut qu'on l'applique au pseudospectre)

eps =int(sys.argv[2])

def gershgorin(M,eps,valeurs_p):
    ligne,colonne=shape(M)
    N=256
    t=[]
    h = 0
    k = 0
    t.append(0)
    r=0
    A = []
    B = []
    X = [0,0]
    Y = [0,0]

    for z in range(0,N+1): #pour constituer le cercle 
        t.append(z*2*pi/N)
  
    if ligne!=colonne:
        print('Il faut une matrice carree')
    else:
        for i in range(0,len(M)): #on recupere les centres 
            h = M[i][i].real #va nous donner les points pour les centres des cercles 
            k = M[i][i].imag
            r = 0
            for j in range(1,len(M)):
                if i!=j:
                    r=r+norm(M[i][j])
            r = r + sqrt(len(M)) * eps
            for a in range(len(t)):
                A.append(r*cos(t[a]) + h)
                B.append(r*sin(t[a]) + k)
            
            if ((h+r) > X[1]):
                X[1] = h+r
            if ((k+r) > Y[1]):
                Y[1] = k+r
            if ((h-r)<X[0]):
                X[0] = h-r
            if ((k-r)<Y[0]):
                Y[0] = k-r
        
    return(X,Y)
#constitution des bornes pour grid 
      
X,Y = gershgorin(M,eps,valeurs_p)

def min(T):
    m = T[0]
    for i in range(len(T)):
        if (abs(m) > abs(T[i])):
            m = T[i]
    return(m)

###### Fonction GRID#######
def grid(M,eps,X,Y,valeurs_p,pas):
    n=int(pas)
    i = complex(0,1)
    x = ny.linspace(X[0],X[1],n)
    y = ny.linspace(Y[0],Y[1],n)
    sigmin= zeros((n,n))
    for k in range(n):
        for j in range(n):
            A,B,C = linalg.svd((x[k]+y[j]*i)*eye(len(M))-M)
            sigmin[j][k] = min(B)
    contour(x,y,sigmin,[eps])

    for i in range(len(valeurs_p)):
        plt.plot(valeurs_p[i].real,valeurs_p[i].imag,'o')
    title("Pseudospectre avec la méthode GRID")
    axis('equal')
    plt.show()

grid(M,eps,X,Y,valeurs_p,pas)

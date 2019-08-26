# coding: utf-8

import random as rd
import matplotlib.pyplot as plt


def gauss2d(N,mu=(0,0),s=(1,1)):
    x, y = [], []
    muX, muY = mu
    sX, sY = s
    for i in range(N):
        x.append(rd.gauss(muX,sX))
        y.append(rd.gauss(muY,sY))

    return x, y

def deuxModes(N,p=0.5,mu1=(0,0), mu2=(5,5)):
    x1, y1 = gauss2d(N,mu=mu1)
    x2, y2 = gauss2d(N,mu=mu2)

    indices = [rd.random()>p for _ in range(N)]
    
    for i in range(N):
        I = indices[i]
        if not I         :
            x1[i], y1[i] = x2[i], y2[i]

    return x1, y1

if __name__ == '__main__':
    #x, y = gauss2d(1000)
    x, y = deuxModes(1000,p=0.1)
    
    plt.scatter(x,y,marker='+')
    plt.show()


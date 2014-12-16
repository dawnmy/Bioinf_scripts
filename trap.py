#!/usr/bin/env python

best = -40

bestxy = [0,0]

newxy = [0,0]



for  x in range(11):

    for  y in range(11):

        f = -(x-5)**2 - (y-5)**2 + 10
        newxy[0]=x
        newxy[1]=y


        if f > best:

            best = f
            print newxy
            # Here is a list reference, be careful, wrong usage
            bestxy = newxy
            
            # Right one
            bestxy = [x, y]


print '%s : %s' % (bestxy, best)

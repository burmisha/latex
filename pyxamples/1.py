#!/usr/bin/env python2

for n in range(17):
    # n = 10
    n0 = n
    k = 0
    while n > 0:
        k = k + 1
        n = n - k

    print k
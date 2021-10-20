# * Copyright 2020 Michael Pollak.
# *
# * Use of this source code is governed by an Apache-style
# * licence that can be found in the LICENSE file.

from elliptic_weierstrass import EllipticWeierstrass
from utility_functions import mod

from math import factorial, gcd
from random import randint

def lenstra(n):
    """
    Args:
        n: The number to factor (do not enter a prime number).
    Returns:
        A prime factor of n.
    """
    
    # No safety net here. It is assumed that n is composite!
    while(True):
        # Find a non-singular elliptical curve
        d = n
        while(d == n):
           ELL,  P = randEllip(n)
           d = gcd(4 * ELL.a**3 + 27 * ELL.b**2, n)
        
        # We got lucky and found a factor somehow!
        if d > 1:
           return d

        # Look for weakness in curve.
        i = 1
        while(factorial(i) < pow(n.bit_length(), 2) * n.bit_length() / 10):
            P = ELL.mul(P, factorial(i))
            i += 1
            if P[2] != 1:
                # n is a factor of itself... cool. (try something else)
                if (P[2] == 0 or P[2] == n):
                    pass
                else:
                    # We found a factor of n... yay!
                    return gcd(P[2], n)

def randEllip(n):
    """
    Args:
        n: The modulus for the curve
    Returns:
        A random elliptic curve and a random point on the curve.
    """
    
    P = randint(0, n - 1), randint(0, n - 1), 1
    a = randint(0, n - 1)
    b = mod(P[1] ** 2 - P[0] ** 3 - a * P[0], n)
    E = EllipticWeierstrass(a, b, n)
    return (E, P)

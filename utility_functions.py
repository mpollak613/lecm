# * Copyright 2020 Michael Pollak.
# *
# * Use of this source code is governed by an Apache-style
# * licence that can be found in the LICENSE file.

import time

# boilerplate Extended Euclidean algorithm
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

# I want to mod 0, thank you!
def mod(x, m):
    if (m != 0):
        x %= m
    return x

def modInv(x, m):
    g, x, _ = egcd(x, m)
    return mod(x, m)

def log(msg, newl = True):
    """
    Args:
        msg: The msg you want to log on the screen.
        end: If you want an endline or not.
    Return:
        None!
    """
    t = time.strftime("%H:%M:%S", time.localtime())

    if (newl == True):
        print(t, msg)
    elif (newl == False):
        print(t, msg, end='')

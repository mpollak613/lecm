# * Copyright 2021 Michael Pollak.
# *
# * Use of this source code is governed by an Apache-style
# * licence that can be found in the LICENSE file.

from module_lenstra import lenstra
from utility_functions import log

from collections import Counter
from math import gcd, sqrt
import time

# Sample keys
rsa_10 = 793
rsa_20 = 727423
rsa_30 = 753695911
rsa_40 = 941591608261
rsa_50 = 900933076730653
rsa_60 = 725208246377758261
non_rsa = 11741730

answers = {
    793: [13, 61],
    727423: [439, 1657],
    753695911: [13063, 57697],
    941591608261: [521981, 1803881],
    900933076730653: [14929679, 60345107],
    725208246377758261: [449159129, 1614590909],
    11741730: [2, 3, 5, 7, 11, 13, 17, 23]
}

def check_answers(n, ans):
    if (n not in answers):
        return ""
    elif (Counter(ans) == Counter(answers[n])):
        return "✓"
    else:
        return "🗴"

def is_prime(p):
    r = 2
    while r <= sqrt(p):
        if p % r < 1:
            return False
        r = r + 1
    return p >= 2

def Example(n):
    log("Starting factorization:")
    factors = []

    if (not is_prime(n)):
        t1 = time.time()
        cur_num = n
        needs_factoring = [n]
        while(len(needs_factoring) != 0):
            cur_num = needs_factoring[0]
            fac = lenstra(cur_num)
            if (is_prime(fac)):
                factors.append(fac)
                needs_factoring = [num // fac for num in needs_factoring]
                while (len(needs_factoring) != 0 and is_prime(needs_factoring[0])):
                    factors.append(needs_factoring[0])
                    needs_factoring = [num // needs_factoring[0] for num in needs_factoring[1:]]
            else:
                needs_factoring.insert(0, fac)
        t2 = time.time()
    else:
        factors.append(n)

    log("{}({} bits) = ".format(n, n.bit_length()), False)
    factors.sort()
    for f in factors[:-1]:
        print(f, "x ", end='')
    print(factors[-1], check_answers(n, factors))
    log('Found in {}s\n'.format(str(round(t2 - t1, 3))))
    return None

Example(non_rsa)
Example(rsa_10)
Example(rsa_20)
Example(rsa_30)
Example(rsa_40)
Example(rsa_50)
# This one could take a while depending on your computer and luck.
#Example(rsa_60)

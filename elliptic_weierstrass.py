# * Copyright 2020 Michael Pollak.
# *
# * Use of this source code is governed by an Apache-style
# * licence that can be found in the LICENSE file.

from utility_functions import mod, modInv

from math import gcd

class EllipticWeierstrass(object):
    """
    - Elliptical curves of the form (y^2 = x^3 + ax + b) mod m where
    - a, b are parameters of the curve formula and
    - m is the curve modulus
    """

    def __init__(self, a, b, m = 0):
        self.a = a
        self.b = b
        self.m = m
        self.discriminate = mod(-16 * (4 * a**3 + 27 * b**2), self.m)

    def __str__(self):
        """
        Args:
            None!
        Return:
            A string form of the elliptical curve.
        """

        equation = "y² "
        if (self.m != 0):
            equation += '≡ '
        else:
            equation += '= '

        equation += 'x³ '

        if (self.a < 0):
            equation += ('- ' + str(-self.a) + 'x ')
        elif (self.a > 0):
            equation += ('+ ' + str(self.a) + 'x ')
        if (self.b < 0):
            equation += ('- ' + str(-self.b) + ' ')
        elif (self.b > 0):
            equation += ('+ ' + str(self.b) + ' ')
        if (self.m > 0):
            equation += ('mod ' + str(self.m))

        return equation

    def __eq__(self, right):
        return self.a, self.b, self.m == right.a, right.b, right.m

    def isSmooth(self):
        """
        Args:
            None!
        Returns:
            If the curve is singular or not.
        """
        return self.discriminate != 0
    
    def isOnCurve(self, point):
        """
        Args:
            point: A point to test
        Returns:
            If the point is on the curve or not.
        """
        # Case infinity
        if (point[2] == 0):
            return True
        # Case other
        delta = point[1]**2 - point[0]**3 - self.a * point[0] - self.b
        return mod(delta, self.m) == 0

    def add(self, P, Q):
        """
        Args:
            P: Point to add.
            Q: Point to add.
        Returns:
            (x, y, *): The addition of both points on the curve where '*' is
                    the denominator of the slope of the tangent.
        Raises:
            ValueError: If either point is not on the curve.
        """

        if (P[0] < 0 or P[1] < 0):
            P = (mod(P[0], self.m), mod(P[1], self.m), P[2])
        if (Q[0] < 0 or Q[1] < 0):
            Q = (mod(Q[0], self.m), mod(Q[1], self.m), P[2])

        # Make certain that both are on the curve.
        if (not self.isOnCurve(P)):
            raise ValueError("{} is not a point on the curve! (ノಠ益ಠ)ノ彡┻━┻".format(P))
        if (not self.isOnCurve(Q)):
            raise ValueError("{} is not a point on the curve! (ノಠ益ಠ)ノ彡┻━┻".format(Q))
        
        # Case P is infinity
        if (P[2] == 0):
            return Q
        # Case Q is infinity
        elif (Q[2] == 0):
            return P
        # Case P == -Q
        elif (P[0] == Q[0] and P[1] == -Q[1]):
            return (0,1,0)
        # Case P == Q
        elif (P[0] == Q[0] and P[1] == Q[1]):
            num = mod((3 * P[0]**2  + self.a), self.m)
            denom = mod(2 * P[1], self.m)
        # Case P != Q
        elif (P[0] != Q[0] or P[1] != Q[1]):
            num = mod((P[1] - Q[1]), self.m)
            denom = mod(P[0] - Q[0], self.m)
        # Fail-case denominator shares a multiple with modulus
        g = gcd(denom, self.m)
        if (g > 1):
            return (0, 0, denom)
        # If no fail-case, return the point on the curve.
        lam = mod(num * modInv(denom, self.m), self.m)
        x = mod(lam ** 2 - P[0] - Q[0], self.m)
        y = mod(lam * (P[0] - x) - P[1], self.m)
        return (x, y, 1)

    def mul(self, P, n = 1):
        """
        Agrs:
            P: a point on the curve
            n: the scalar multiplying (defaults to one)
        """

        # Reverse hack via binary.
        x = bin(n)[2:][::-1]
        T = P
        S = (0,1,0)
        for i in x:
            # Case T is infinity
            if (T[2] > 1):
                return T
            # Case S is infinity
            if (S[2] > 1):
                return S
            if (i == '1'):
                S = self.add(S, T)
            T = self.add(T, T)
        return S

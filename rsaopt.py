#!/usr/bin/env python

import sys
from Crypto.PublicKey import RSA
from fractions import gcd
from gmpy2 import mpz, popcount

def usage():
    print >> sys.stderr, "Usage: %s <RSA privatekey file>" % sys.argv[0]
    exit(2)

def lcm(a, b):
    return a * b / gcd(a, b)

def ctf(p, q):
    return lcm(p - 1, q - 1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()

    with open(sys.argv[1]) as f:
        key = RSA.importKey(f.read())

    if not key.has_private():
        print >> sys.stderr, "Private key required"
        exit(1)

    carmichael = ctf(key.p, key.q)
    reduced_d = key.d % carmichael
    minpc = popcount(mpz(key.d))

    print >> sys.stderr, "Original exponent:"
    print >> sys.stderr, key.d
    print >> sys.stderr, "Reduced exponent:"
    print >> sys.stderr, reduced_d
    print >> sys.stderr, "Original popcount:", minpc

    step = mpz(carmichael)
    a = mpz(reduced_d)
    opt_a = mpz(key.d)
    limit = mpz(key.n)
    while a < limit:
        pc = popcount(a)
        if pc < minpc:
            minpc = pc
            opt_a = a
        print >> sys.stderr, pc
        a += step

    print >> sys.stderr, "Optimized exponent:"
    print >> sys.stderr, int(opt_a)
    print >> sys.stderr, "Optimized popcount:", popcount(opt_a)
    key.d = opt_a
    print key.exportKey()

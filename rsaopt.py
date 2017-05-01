#!/usr/bin/env python

import sys
from Crypto.PublicKey import RSA
from fractions import gcd

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print >> sys.stderr, "Usage: %s <RSA privatekey file>" % sys.argv[0]
        exit(2)

    with open(sys.argv[1]) as f:
        key = RSA.importKey(f.read())

    if not key.has_private():
        print >> sys.stderr, "Private key required"
        exit(1)

    carmichael = (key.p - 1) * (key.q - 1) / gcd(key.p - 1, key.q - 1)
    key.d = key.d % carmichael
    print key.exportKey()

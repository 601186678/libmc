import os
import sys
import binascii
import hashlib
import numpy as np

FNV_32_INIT = 0x811c9dc5
FNV_32_PRIME = 0x01000193

def compute_crc_32(key):
    return np.uint32(binascii.crc32(key))


def compute_fnv1_32(key):
    hval = FNV_32_INIT
    fnv_32_prime = FNV_32_PRIME
    uint32_max = 2 ** 32
    for s in key:
        hval = (hval * fnv_32_prime) % uint32_max
        hval = hval ^ ord(s)
    return np.uint32(hval)


def compute_fnv1a_32(key):
    hval = FNV_32_INIT
    fnv_32_prime = FNV_32_PRIME
    uint32_max = 2 ** 32
    for s in key:
        hval = hval ^ ord(s)
        hval = (hval * fnv_32_prime) % uint32_max
    return np.uint32(hval)


def compute_md5(key):
    md5 = hashlib.md5()
    md5.update(key)
    digest = md5.digest()

    return ((np.uint32(ord(digest[3]) & 0xFF) << 24) |
           (np.uint32(ord(digest[2]) & 0xFF) << 16) |
           (np.uint32(ord(digest[1]) & 0xFF) << 8) |
           (ord(digest[0]) & 0xFF))


U32_HASH_FN_DICT = {
    'crc_32': (compute_crc_32, []),
    'fnv1_32': (compute_fnv1_32, []),
    'fnv1a_32': (compute_fnv1a_32, []),
    'md5': (compute_md5, []),
}

def main(argv):
    if not len(argv) == 2:
        print >> sys.stderr, "usage: python %s in.txt" % argv[0]
        return 1

    input_path = os.path.abspath(sys.argv[1])

    with open(input_path) as fhandler:
        for line in fhandler:
            key = line.strip()
            for hash_name, (hash_fn, hash_rst) in U32_HASH_FN_DICT.iteritems():
                hash_rst.append(hash_fn(key))

    for hash_name, (hash_fn, hash_rst) in U32_HASH_FN_DICT.iteritems():
        prefix, dot_ext = os.path.splitext(input_path)
        out_path = '%s_%s%s' % (prefix, hash_name, dot_ext)
        with open(out_path, 'w') as fhandler:
            fhandler.writelines(("%s\r\n" % h for h in hash_rst))
        print out_path


if __name__ == '__main__':
    sys.exit(main(sys.argv))

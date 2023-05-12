import bbhash
import Utils


def build_bbhash(keys, hashfn, N):
    hashes = hashfn(keys, N=N)
    mph = bbhash.PyMPHF(hashes, len(hashes), 1., 1)
    return mph


def query(mph, keys, N):
    hashes = Utils.hash_keys(keys, N)
    if isinstance(keys, list):
        isin = [0]*len(keys)
        for ind, hasher in enumerate(hashes):
            if mph.lookup(hasher) is None:
                isin[ind] = False
            else:
                isin[ind] = True
        return isin
    else:
        if mph.lookup(keys) is None:
            return False
        else:
            return True

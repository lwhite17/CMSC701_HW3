from array import *


class FingerprintArray:
    def __init__(self, b, N):
        # self.fa = sp.sparse.csr_matrix((b*N), [bytes])
        self.b = b
        self.N = N
        self.fa = array('b', [0]*(N*b))

    def populate(self, mph, keys, hashfn):
        hashed = hashfn(keys, N=self.N)
        for hasher in hashed:
            ind = mph.lookup(hasher)
            if ind is None:
                continue
            if len(str(hasher)) < self.b:
                hasher = str(hasher) + '0'*(self.b-len(str(ind)))
            for i in range(self.b):
                self.fa[ind*self.b + i] = int(str(hasher)[i])

    def get_size(self):
        return self.fa.itemsize * len(self.fa) + 4*2

    def get(self, start, stop):
        l = stop - start
        res = ['']*l
        for i in range(l):
            res[i] = str(self.fa[i])
        return ''.join(res)

    def query(self, keys, mph, hashfn):
        if isinstance(keys, list):
            hashed = hashfn(keys, N=self.N)
            isin = [False] * len(keys)
            for ind, hasher in enumerate(hashed):
                mph_ind = mph.lookup(hasher)
                if mph_ind is None:
                    isin[ind] = False
                else:
                    # saved_bytes = self.fa[mph_ind:mph_ind+self.b]
                    saved_bytes = self.get(mph_ind, mph_ind+self.b)
                    comp_bytes = str(hasher) + '0'*(self.b-len(str(mph_ind)))
                    if saved_bytes == comp_bytes[:self.b]:
                        isin[ind] = True
                    else:
                        isin[ind] = False
            return isin
        else:
            hashed = hashfn([keys], N=self.N)
            mph_ind = mph.lookup(hashed)
            if mph_ind is None:
                return False
            else:
                saved_bytes = self.get(mph_ind, mph_ind + self.b)
                comp_bytes = str(hashed) + '0' * (self.b - len(str(mph_ind)))
                if saved_bytes == comp_bytes:
                    return True
                else:
                    return False

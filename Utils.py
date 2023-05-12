import random
# import string
import xxhash


def read_file(filename):
    file = open(filename, 'r')
    lines = file.readlines()
    keys = []
    for line in lines:
        keys.append(line.strip())
    file.close()
    return keys


def write_keys_to_file(keys, filename):
    with open(filename, "w") as f:
        for key in keys:
            f.write(key + "\n")


def generate_keys(length, number):
    keys = ["0"]*number
    for i in range(number):
        keys[i] = ''.join((random.choice('ACGT') for _ in range(length)))
    return keys


def generate_test_keys(length, number, keys, overlap=None):
    test_keys = []
    for i in range(number*2):
        key = ''.join((random.choice('ACGT') for _ in range(length)))
        if key not in keys:
            test_keys.append(key)
        if len(test_keys) == number:
            break

    if overlap is not None:
        n_overlap = int(overlap*number)
        o_test_keys = keys[:n_overlap]
        o_test_keys.extend(test_keys[:int(number-n_overlap)])
        test_keys = o_test_keys

    return test_keys


def true_is_in(test_keys, keys):
    truth = []
    for key in test_keys:
        truth.append(key in keys)
    return truth


def check_false_neg(truth, query):
    k = 0
    for i in range(len(truth)):
        if truth[i] == query[i]:
            continue
        else:
            if truth[i] and not query[i]:
                k += 1
    print(f"{k} false negatives")
    return []


def hash_keys(keys, N):
    hashes = [0]*len(keys)
    for ind, key in enumerate(keys):
        hashes[ind] = xxhash.xxh32(bytes(key, 'utf-8')).intdigest()
    return hashes


if __name__ == '__main__':
    for N in [10000, 30000, 60000]:

        keys = generate_keys(length=31, number=N)
        write_keys_to_file(keys, filename=f"Data/K_{N}.txt")

        for o in [0, 0.1, 0.25, 0.5]:
            test_keys_ = generate_test_keys(length=31, number=N, keys=keys,
                                            overlap=o)
            write_keys_to_file(test_keys_,
                               filename=f"Data/Kp_{N}_{int(o*100)}.txt")

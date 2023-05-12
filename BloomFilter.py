from bloom_filter2 import BloomFilter


def build_bf(max_elements, error_rate):
    bloom = BloomFilter(max_elements=max_elements, error_rate=error_rate)
    return bloom


def add_to_bf(keys, bloom_filter):
    if isinstance(keys, list):
        for key in keys:
            bloom_filter.add(key)
    else:
        bloom_filter.add(keys)
    return bloom_filter


def query(bloom_filter, keys):
    if isinstance(keys, list):
        isin = [False] * len(keys)
        for ind, key in enumerate(keys):
            isin[ind] = key in bloom_filter
        return isin
    else:
        return keys in bloom_filter



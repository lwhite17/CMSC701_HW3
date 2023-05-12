# CMSC701_HW3

Evaluating bloom filter, BBHash MPHF, and MPHF with fingerprint array.  
<br/>


This code is available at https://github.com/lwhite17/CMSC701_HW3.  
<br/>


Note that none of this code was built to be called from the command line. Instead, I provide examples of function calls. 
</br>


By Leah White   
<br/><br/>

---------------------------------------------  
---------------------------------------------  
<br/>


## Task 1: Bloom Filter

</br>

The functionality to build and use the bloom filter is in *BloomFilter.py*. The file *BloomFilterScript.py* calls those functions to evaluate the filter as instructed in the assignment. This README will discuss *BloomFilter.py*.  

BloomFilter.py uses the package bloomfilter downloadable from pypi at the link https://pypi.org/project/bloom-filter2/. 

</br>

### Function: *build_bf*  

Call:  

    bf = build_bf(max_elements=10000, error_rate = 1./(2**7))

Parameters:  

    -  *max_elements*: int. The maximum number of elements that will be added to the bloom filter.  

    - *error_rate*: float. The input false positive rate.  

Returns:  

    - bloom filter object (without keys added to it).  

</br>


### Function: *add_to_bf*  

Call:  

    bf = add_to_bf(keys=['ACTGGTC', 'CGGGTAAC', ...], bloom_filter=bf)

Parameters:  

    -  *keys*: list of strings. The keys to build the bloom filter on.  

    - *bloom_filter*: bloom filter object. Must be a bloomfilter2 object (e.g. a result from *build_bf*).

Returns:  

    - bloom filter object (with keys added to it).  

</br>


### Function: *query*   

Call:  

    approx_membership = query(bloom_filter=bf, keys = ['ACTGGTC', 'CGCGTAAC', ...])

Parameters:  

    -  *bloom_filter*: bloom filter object. Must be a bloomfilter2 object (e.g. a result from *build_bf*).  

    - *keys*: list of strings. The keys (K') to test membership of.  

Returns:  

    - list of True and False values. Element at index is True if bloom filter's innate querying returned that the key at the same index was in the bloom filter, and False otherwise.  


<br/><br/>

---------------------------------------------  
<br/>

## Task 2: MPHF: BBHash  

</br></br>

The functionality to build and use the BBHash MPHF is in *BBHash.py*. The file *BBHashScript.py* calls those functions to evaluate the filter as instructed in the assignment. This README will discuss *BBHash.py*.  

BBHash.py uses the package bbhash downloadable from pypi at the link https://pypi.org/project/bbhash/. 

</br></br>

### Function: *build_bbhash*  

Call:  

    mph = build_bbhash(keys = ['ACTGGTC', 'CGCGTAAC', ...], hashfn = hash, N=1000)

Parameters:  

    - *keys*: list of strings. The keys (K) to use to build.  

    - *hashfn*: function. The hash function to use for BBHash. As used in BBHashScript, this is xxhash (see Utils section of README).  

    - *N*: int. Max number of keys to add to MPHF.  

Returns:  

    - bbhash PyMPHF object (with keys added to it).  

</br></br>

### Function: *query*

Call:  

    approx_membership = query(mph=mph, keys = ['ACTGGTC', 'CGCGTAAC', ...], N=1000)

Parameters:  

    -  *mph*: bbhash PyMPHF object. Must be a bbhash.PyMPHF object (e.g. a result from *build_bbhash*).  

    - *keys*: list of strings. The keys (K') to test membership of.  

    - *N*: int. The maximum number of keys in the MPHF.  

Returns:  

    - list of True and False values. Element at index $i$ is True if bbhash's built-in lookup method returned an integer index for the key at index $i$, and False otherwise.  

<br/><br/>

---------------------------------------------  
<br/>

## Task 3: BBHash + Fingerprint array  

The functionality to build and use the BBHash MPHF with fingerprint array is in *FingerprintArray.py*. The file *FingerprintArrayScript.py* calls those functions to evaluate the filter as instructed in the assignment. This README will discuss *FingerprintArray.py*.  

FingerprintArray.py uses the package bbhash downloadable from pypi at the link https://pypi.org/project/bbhash/, and uses the utility in *BBHash.py*. 

</br></br>

### Class: *FingerprintArray*  

Call:  

    hashfn = hash
    keys = ['ACTGGTC', 'CGCGTAAC', ...]
    mph = BBHash.build_bbhash(keys=keys, hashfn=hashfn)
    fpa = FingerprintArray(b=7, N=1000)

Parameters:  

    - *b*: int. Fingerprint array will store first $b$ bits of hashed keys.

    - *N*: int. Max number of keys to add to MPHF.  

Returns:  

    - FingerprintArray class object.  

</br></br>

### Class method: *populate* 
Call:  

    fpa.populate(mph=mph, keys=keys, hashfn=hashfn)

Parameters:  

    - *mph*: mph. bbhash PyMPHF object. Must be a bbhash.PyMPHF object (e.g. a result from *build_bbhash*).  

    - *keys*: list of strings. The keys (K) to use to build.  

    - *hashfn*: function. The hash function to use for BBHash. As used in BBHashScript, this is xxhash (see Utils section of README).  

Does not return anything; just updates **fpa**, the FingerprintArray object. 

</br></br>


### Class method: *get_size* 
Call:  

    fpa.get_size()

Returns the total size of the FingerprintArray object in bytes.

</br></br>

### Class method: *get* 
Call:  

    fpa.get(start=0, stop=b)

Parameters:  

    - *start*: int. The index at which to start reading the stored bits.  

    - *stop*: ints. The index before which to stop reading the stored bits.


Returns:  

    - array of bits.  

</br>

### Class method: *query* 
Call:  

    fpa.query(keys=keys, mph=mph, hashfn=hashfn)

Parameters:  

    - *keys*: list of strings. The keys (K') to use to get approximate membership.  

    - *mph*: mph. bbhash PyMPHF object. Must be a bbhash.PyMPHF object (e.g. a result from *build_bbhash*).  

    - *hashfn*: function. The hash function to use for BBHash. As used in BBHashScript, this is xxhash (see Utils section of README).  

Returns:  

    - list of True and False values. Element at index $i$ is True if bbhash's built-in lookup method returned an integer index for the key at index $i$, and False otherwise.  

<br/><br/>

---------------------------------------------  
<br/>

## Utils

*Utils.py* contains functions used by the other scripts and functions.  

</br></br>


### Function: *read_file*

Call:  

    filename = "keys.txt"
    keys = read_file(filename)

Parameters:  

    -  *filename*: string. Path to file containing keys. 

Returns:  

    - list keys (strings).  

<br/></br>

### Function: *write_keys_to_file*

Call:  

    write_keys_to_file(keys = ['ACTGGTC', 'CGCGTAAC', ...], filename=filename)

Parameters:  

    - *keys*: list of strings.  

    - *filename*: string. Path to file in which to save the keys.  

Does not return anything. Writes keys to file.  

<br/></br>


### Function: *generate_keys*

Call:  

    keys = generate_keys(length=31, number=1000)

Parameters:  

    - *length*: int. Length of string to generate.  

    -  *number*: int. Number of pseudorandom keys (strings containing A,C,T,G) to generate.   

Returns:  

    - list of strings of length *length*

<br/></br>


### Function: *generate_test_keys*

Call:  

    test_keys = generate_test_keys(length=31, number=1000, keys=keys, overlap=0.1)

Parameters:  

    - *length*: int. Length of string to generate.  

    -  *number*: int. Number of pseudorandom keys (strings containing A,C,T,G) to generate.   

    - *keys*: list of strings. The keys (K) used to build filter.  

    - *overlap*: float. The proportion of keys from the building set to include in the testing set. Otherwise, the test keys are distinct from the input keys.  

Returns:  

    - list of strings.  

<br/></br>




### Function: *true_is_in*

Call:  

    truth = tru_is_n(test_keys, keys)

Parameters:  

    - *test_keys*: list of strings. The keys (K') used to test filter.  

    - *keys*: list of strings. The keys (K) used to build filter.  


Returns:  

    - list of True/False values. Index $i$ contains True if the test key at index $i$ was in keys.    

<br/></br>

### Function: *hash_keys*

Call:  

    hashes = hash_keys(keys=keys, N=1000)

Parameters:  

    - *keys*: list of strings. The keys (K) used to build filter.  

    - *N*: int. Maximum number of keys the filter contains.  


Returns:  

    - list of hashed strings (digested as 32-bit integers). Uses xxhash.xxh32().  

<br/>

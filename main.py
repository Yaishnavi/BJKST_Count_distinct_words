import random
import time
import math
random.seed(100) # Choose any random seed

def read_words(filename):
    ## Read a text file and return a token representing each word in the file
    with open(filename,'r') as f:
        text = f.read()
        words = text.split()
    
    tokens = []
    for word in words:
        word = word.lower()
        # Remove all common punctuations
        for c in '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~':
            word= word.replace(c,"")
        tokens.append(hash(word))
    return tokens  

def  count_exact(words):
    count = 0
    dict = {}
    for word in words:
        if (word in dict.keys()): 
            dict[word] += 1
        else:
            dict[word] = 1
            count += 1
    return count

def algorithm(tokens, epsilon):
    ## 2 Universal Hash function
    n = len(tokens)
    def rand_prime():
        while True:
            p = random.randrange(2 ** 32, 2 ** 34, 2)
            if all(p % n != 0 for n in range(3, int((p ** 0.5) + 1), 2)):
                return p
    p = rand_prime()
    a1, a2 = random.sample(range(1, p), 2)
    b1, b2 = random.sample(range(0, p), 2)
    b = int(math.log(n) / epsilon**2)
    def hash1(x):
        return ((a1*x + b1) % p) % n
    def hash2(x):
        return ((a2*x + b2) % p) % b
    # Look up for mod37
    mod_pos = (32, 0, 1, 26, 2, 23, 27, 0, 3, 16, 24, 30, 28, 11, 0, 13, 4, 7, 17, 0, 25, 22, 31, 15, 29, 10, 12, 6, 0, 21, 14, 9, 5, 20, 8, 19, 18)
    #BJKST algorithm
    c = 0
    B = set()
    B_max = 1.0 / epsilon**2
    for x in tokens:
        h = hash1(x)
        k = mod_pos[(-h & h) % 37]
        if (k >= c):
            z = hash2(x)
            B.add((z, k))
            while (len(B) >= B_max):
                c += 1
                for z, k in B.copy():
                    if (k < c):
                        B.remove((z, k))
    return 2**c*len(B)

def Count_Distinct(words, flag, epsilon = 0.001):
    if flag == 0:
        ## Count total number of distinct words
        start_time = time.time()
        distinct_words = count_exact(words)
        total_time = time.time() - start_time
        print('Exact Number of Unique words in the file : ', distinct_words)
        print('Time taken: ', total_time)
    elif flag == 1:
        ## Sketching algorithm
        start_time = time.time()
        distinct_words = algorithm(words,epsilon)
        total_time = time.time() - start_time
        print('BJKST ALGO with epsilon ',epsilon)
        print('Number of Unique words in the file : ', distinct_words)
        print('Time taken: ', total_time)

if __name__ == "__main__":

    filename = 'wiki_small.txt' # use "test_file.txt" wiki_small.txt' 'wiki_100MB.txt"  or any other txt file
    words = read_words(filename)
    print('\nTotal number of words in the file: ', len(words))

    flag = 0
    Count_Distinct(words, flag)
    print()
    flag = 1
    Count_Distinct(words, flag, epsilon = 0.001)
    print()
    flag = 1
    Count_Distinct(words, flag, epsilon = 0.1)
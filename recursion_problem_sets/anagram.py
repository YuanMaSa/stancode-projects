"""
File: anagram.py
Name:
----------------------------------
This program recursively finds all the anagram(s)
for the word input by user and terminates when the
input string matches the EXIT constant defined
at line 19

If you correctly implement this program, you should see the
number of anagrams for each word listed below:
    * arm -> 3 anagrams
    * contains -> 5 anagrams
    * stop -> 6 anagrams
    * tesla -> 10 anagrams
    * spear -> 12 anagrams
"""

import time

# Constants
FILE = 'dictionary.txt'       # This is the filename of an English dictionary
EXIT = '-1'                   # Controls when to stop the loop
proc_queue = []
hash_map = {}


def main():
    """
    main handler of anagram producer program
    :return: None
    """
    read_dictionary(FILE)
    while True:
        print("Welcome to stanCode "'Anagram Generator'" (or -1 to quit)")
        input_word = input("Find anagrams for: ")
        input_word = input_word.lower()
        if input_word == "-1":
            break
        start_time = time.time()
        find_anagrams(input_word)
        if len(proc_queue) > 0:
            print(f"{len(proc_queue)} anagrams: {proc_queue}")
            print("======================================================================\n"
                  "total running time of the word <<%s>> : --- %s seconds ---\n"
                  "======================================================================\n"
                  % (proc_queue[0], time.time() - start_time))
        proc_queue.clear()


def read_dictionary(file):
    """
    read the data from txt and create the dictionary

    :param file:
    :return: None
    """

    with open(file, 'r') as f:
        for row in f.readlines():
            word = row.strip()
            hash_map_generator(word)

    # print(hash_map)

def hash_map_generator(word):
    """
    generate a hashmap which is way faster than list

    :param word:
    :return: None
    """
    if len(word) > 1:
        sub_str = word[:2]
    else:
        sub_str = word[0]

    if sub_str not in hash_map:
        hash_map[sub_str] = {}
        hash_map[sub_str] = [word]
    else:
        hash_map[sub_str].append(word)


def find_anagrams(s):
    """
    :param s:
    :return: None
    """
    find_anagrams_helper(s, "")

def find_anagrams_helper(s, chosen):
    """
    helper function of find_anagrams

    :param s:
    :param chosen:
    :return: None
    """
    if len(s) == 0:
        if in_dict(chosen) and chosen not in proc_queue:
            print("Searching...")
            print(f"Found:   {chosen}")
            proc_queue.append(chosen)
    else:
        for i in range(0, len(s)):
            chosen += s[i]
            find_anagrams_helper(s[:i] + s[i+1:], chosen)
            chosen = chosen[:-1]

def in_dict(word):
    """
    check if the word in dictionary

    :param word:
    :return: boolean value if word in dictionary
    """
    if len(word) > 1:
        sub_str = word[:2]
    else:
        sub_str = word[0]

    if has_prefix(sub_str) and word in hash_map[sub_str]:
        return True

    return False


def has_prefix(sub_s):
    """

    :param sub_s:
    :return: boolean value if substring in dictionary
    """

    if sub_s not in hash_map:
        return False

    return True


if __name__ == '__main__':
    main()

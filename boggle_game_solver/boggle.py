"""
File: boggle.py
Name:
----------------------------------------
TODO:
"""

import time

# This is the file name of the dictionary txt file
# we will be checking if a word exists by searching through it
FILE = 'dictionary.txt'

# set up parameters
MIN_WORD_LENGTH = 4
VALID_ROWS = 4
VALID_COLS = 4

# set up preferable data structure
hash_map = {}
prefix_map = {}
boggle_queue = []
res_queue = []

# ---test case shown as below---

# f y c l
# i o m g
# o r i l
# h j h u


def main():
    """
    TODO:
    """

    input_valid = True
    # load dictionary data
    read_dictionary(FILE)

    # handle user input
    while len(boggle_queue) != VALID_ROWS:
        usr_input = input(f"{len(boggle_queue)+1} row of letters: ")
        if not is_valid_input(usr_input.split()):
            print("Illegal input")
            input_valid = False
            break
        target = [x.lower() for x in usr_input.split()]
        boggle_queue.append(target)

    # running result
    start_time = time.time()
    if input_valid:
        find_words(boggle_queue)
        if len(res_queue) > 0:
            print("=========================================================================================\n"
                  "total running time of the <find_words> function: --- %s seconds ---\n"
                  "=========================================================================================\n"
                  % (time.time() - start_time))

def is_valid_input(row_items: list):
    """

    :param row_items: user input
    :return: if user input is valid
    """
    letter_length = sum([len(x) for x in row_items])
    if len(row_items) != VALID_ROWS or letter_length != VALID_COLS:
        return False
    return True

def find_words(queue: list):
    """

    :param queue:
    :return: None
    """

    for row_i, row_ele in enumerate(queue):
        # ["f", "y", "c", "l"] -> ["i", "o", "m", "g"]
        for char_i, char in enumerate(row_ele):
            # f -> y -> c -> l
            find_words_helper(queue, row_i, char_i, '', [])
    print(f"There are {len(res_queue)} words in total.")

def find_words_helper(queue: list, row_i: int, char_i: int, cur_word: str, visited: list):
    """

    :param queue:
    :param row_i:
    :param char_i:
    :param cur_word:
    :param visited:
    :return:
    """

    if len(cur_word) >= MIN_WORD_LENGTH:
        if is_valid_word(cur_word) and has_prefix(cur_word):
            find_neighbor(queue, row_i, char_i, cur_word, visited)
    else:
        find_neighbor(queue, row_i, char_i, cur_word, visited)

def find_neighbor(queue: list, row_i: int, char_i: int, cur_word: str, visited: list):
    """

    :param queue:
    :param row_i:
    :param char_i:
    :param cur_word:
    :param visited:
    :return: None
    """
    # using neighbor finding algorithm
    for i in range(-1, 2):
        for j in range(-1, 2):
            neighbor_x = row_i + i
            neighbor_y = char_i + j
            if 0 <= neighbor_x < len(queue) and 0 <= neighbor_y < len(boggle_queue):
                # if neighbor_x, neighbor_y in valid range -> add char
                if (neighbor_x, neighbor_y) not in visited:
                    # check if the point (x, y) has been visited
                    visited.append((neighbor_x, neighbor_y))
                    cur_word += queue[neighbor_x][neighbor_y]
                    # Recursion Case
                    find_words_helper(queue, neighbor_x, neighbor_y, cur_word, visited)
                    visited.pop()
                    cur_word = cur_word[:-1]

def is_valid_word(cur_word: str) -> bool:
    """

    :param cur_word: selected word in our job
    :return: if the word is the valid target
    """
    if in_dict(cur_word) and cur_word not in res_queue:
        res_queue.append(cur_word)
        print(f'Found "{cur_word}"')
        return True
    return False

def read_dictionary(file: str):
    """
    This function reads file "dictionary.txt" stored in FILE
    and appends words in each line into a Python list
    """
    with open(file, 'r') as f:
        for row in f.readlines():
            word = row.strip()
            hash_map_generator(word)
            prefix_map_generator(word)

def hash_map_generator(word: str):
    """
    generate a hashmap which is way faster than list

    :param word: word in dictionary
    :return: None
    """
    key = get_key_in_dict(word)
    if key not in hash_map:
        hash_map[key] = [word]
    else:
        hash_map[key].append(word)

def prefix_map_generator(word: str):
    """

    :param word: word in dictionary
    :return: None
    """
    if len(word) > 1:
        sub_str = word[:2]
    else:
        sub_str = word[0]

    if sub_str not in prefix_map:
        prefix_map[sub_str] = {}
        prefix_map[sub_str] = [word]
    else:
        prefix_map[sub_str].append(word)


def get_key_in_dict(word: str) -> tuple:
    """

    :param word: word in dictionary
    :return: key in tuple
    """
    count = [0] * 26
    # using ASCII value to set char count to its index
    for char in word:
        count[ord(char) - ord("a")] += 1
    key = tuple(count)
    return key


def in_dict(word: str) -> bool:
    """
    check if the word in dictionary

    :param word:
    :return: boolean value if word in dictionary
    """
    key = get_key_in_dict(word)
    if key in hash_map and word in hash_map[key]:
        return True
    return False


def has_prefix(sub_s: str) -> bool:
    """
    :param sub_s: (str) A substring that is constructed by neighboring letters on a 4x4 square grid
    :return: (bool) If there is any words with prefix stored in sub_s
    """

    if len(sub_s) > 1:
        sub_str = sub_s[:2]
    else:
        sub_str = sub_s[0]

    if sub_str not in prefix_map:
        return False

    for poss_word in prefix_map[sub_str]:
        if poss_word.startswith(sub_str) and len(poss_word) > len(sub_str):
            return True
    return False


if __name__ == '__main__':
    main()

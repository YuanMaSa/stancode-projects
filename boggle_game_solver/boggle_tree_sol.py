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
ROWS = 4
hash_map = {}
boggle_queue = []
res_queue = []

class Child:
    def __init__(self):
        self.child = {}
        self.last = False


class Tree:
    def __init__(self):
        self.node = Child()

    def add_node(self, word):
        node = self.node
        for c in word:
            if c not in node.child:
                node.child[c] = Child()
            node = node.child[c]
        node.last = True

    def has_prefix(self, word):
        node = self.node
        for c in word:
            if c not in node.child:
                return False
            node = node.child[c]

        return True

    def node_is_end(self, word):
        node = self.node
        for c in word:
            if c not in node.child:
                return False
            node = node.child[c]

        return node.last

def add_dict_tree(file):
    dict_tree = Tree()
    with open(file, 'r') as f:
        for row in f.readlines():
            word = row.strip()
            dict_tree.add_node(word)
    return dict_tree


def main():
    """
    TODO:
    """
    # f y c l
    # i o m g
    # o r i l
    # h j h u
    input_valid = True
    # load dictionary data
    read_dictionary(FILE)
    # handle user input
    while len(boggle_queue) != ROWS:
        usr_input = input(f"{len(boggle_queue)+1} row of letters: ")
        if not is_valid(usr_input.split()):
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
            print(
                "======================================================================\n"
                "total running time of the <find_words> function: --- %s seconds ---\n"
                "======================================================================\n"
                % (time.time() - start_time)
            )
    # print(hash_map)

def is_valid(row_items: list):
    letter_length = sum([len(x) for x in row_items])
    if len(row_items) != ROWS or letter_length != ROWS:
        return False
    return True

def find_words(queue: list):
    # f y c l
    # i o m g
    # o r i l
    # h j h u
    dict_tree = add_dict_tree(FILE)
    # generate the initial dictionary tree to check if word has prefix in dictionary

    for row_i, row_ele in enumerate(queue):
        # ["f", "y", "c", "l"] -> ["i", "o", "m", "g"]
        for char_i, char in enumerate(row_ele):
            # f -> y -> c -> l
            find_words_helper(queue, (row_i, char_i), '', [], dict_tree)

    print(f"There are {len(res_queue)} words in total.")

def find_words_helper(queue: list, xy: tuple, curr_str: str, visited: list, dict_tree: Tree):
    # f y c l
    # i o m g
    # o r i l
    # h j h u
    """

    :param queue: input data
    :param xy: row index & char index
    :param curr_str: chosen string
    :param visited: a list to store the visiting status
    :param dict_tree: dictionary tree
    :return: None
    """

    # Base Case
    if len(curr_str) != 0 and not dict_tree.has_prefix(curr_str):
        # if there is no prefix in dictionary -> break
        return
    if dict_tree.node_is_end(curr_str) and len(curr_str) >= 4:
        # the word which length >= 4 and in dictionary
        if curr_str not in res_queue:
            print(f'Found "{curr_str}"')
            res_queue.append(curr_str)

    row_i, char_i = xy

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
                    curr_str += queue[neighbor_x][neighbor_y]
                    # Recursion Case
                    find_words_helper(queue, (neighbor_x, neighbor_y), curr_str, visited, dict_tree)
                    visited.pop()
                    curr_str = curr_str[:-1]


def read_dictionary(file: str):
    """
    This function reads file "dictionary.txt" stored in FILE
    and appends words in each line into a Python list
    """
    with open(file, 'r') as f:
        for row in f.readlines():
            word = row.strip()
            hash_map_generator(word)

def hash_map_generator(word: str):
    """
    generate a hashmap which is way faster than list

    :param word:
    :return: None
    """
    key = get_key_in_dict(word)
    if key not in hash_map:
        hash_map[key] = [word]
    else:
        hash_map[key].append(word)

def get_key_in_dict(word: str) -> tuple:
    count = [0] * 26
    # using ASCII value to set char count to its index
    for c in word:
        count[ord(c) - ord("a")] += 1
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
    if sub_s not in hash_map:
        return False

    return True


if __name__ == '__main__':
    main()

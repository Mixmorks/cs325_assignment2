from timeit import timeit
from random import randint
from align import *

lengths = [500, 1000, 2000, 4000, 5000]
alphabet = ['A', 'G', 'T', 'C']


def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped

def build_sequence_pairs(num_pairs=10):
    pairs = []
    for i in range(0, num_pairs):
        sequence1 = ""
        sequence2 = ""
        for j in range(0, length):
            sequence1 += alphabet[randint(0, len(alphabet) - 1)]
            sequence2 += alphabet[randint(0, len(alphabet) - 1)]
        pairs.append(sequence1 + ',' + sequence2 + '\n')

    return pairs

def handle_line(d_cost, line):
    A, B = line.strip('\n').split(',')
    B = B[:-1]  # B will have a trailing newline, which needs to be removed

    # Generate the edit distance array and use that to build our aligned strings
    a_edit_dist, backtrace = edit_distance(d_cost, A, B)

    align(A, B, backtrace)

def calculate_runtime():
    total_time = 0

    f_cost = open("imp2cost.txt", 'r')
    f_data = open("imp2input.txt", 'r')

    d_cost = file_2_dict(f_cost)

    for line in f_data:
        wrapped = wrapper(handle_line, d_cost, line)
        total_time = timeit(wrapped, number=1)

    return total_time

if __name__ == "__main__":
    for length in lengths:
        with open("imp2input.txt", 'w') as f:
            for pair in build_sequence_pairs():
                f.write(pair)

        print calculate_runtime()
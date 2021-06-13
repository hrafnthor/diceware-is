import os
import random


def calculate(cursor, gap, increments):
    return increments + increments * ((cursor // gap) % 6)


def get_line_number(cursor):
    return calculate(cursor, 1512, 10000) \
           + calculate(cursor, 216, 1000) \
           + calculate(cursor, 36, 100) \
           + calculate(cursor, 6, 10) \
           + calculate(cursor, 1, 1)


def write_line(cursor, line, destination):
    number = get_line_number(cursor)
    destination.write(f"{number} {line}")
    return cursor + 1


def write_from_file(cursor, source, destination):
    for line in filter(lambda l: l.rstrip(), source):
        cursor = write_line(cursor, line, destination)
    return cursor


def extract_words(source):
    words = []
    for word in filter(lambda l: l.rstrip(), source):
        if 4 <= len(word) <= 8:
            words.append(word.lower())
    return words


def generate(max_size):
    destination_cursor = 0
    destination_file = open("generated", "w")

    # Read in any predefined prepend values that should be used
    # adding them to the destination file
    prepend_file = open("res/prepend")
    destination_cursor = write_from_file(destination_cursor, prepend_file, destination_file)
    prepend_file.close()

    print(f"Found {destination_cursor} valid lines to prepend")
    required_word_count = max_size - destination_cursor
    print(f"Will need {required_word_count} words from source")

    # Read in the words from the source file to memory for use later
    word_file = open("res/source")
    words = extract_words(word_file)
    word_file.close()

    number_of_valid_words = len(words)
    if number_of_valid_words < required_word_count:
        print(f"Found only {number_of_valid_words} valid words.")

        destination_file.close()
        os.remove(destination_file.name)
    else:
        print(f"Found {number_of_valid_words} valid words to use.")

        # Take random words from the list and append them to the
        # destination file until the required maximum is reached
        while destination_cursor < max_size:
            word = random.choice(words)
            words.remove(word)
            destination_cursor = write_line(destination_cursor, word, destination_file)
        destination_file.close()


generate(7776)

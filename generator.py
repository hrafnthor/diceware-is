import os
import random

total_line_count = 7776
destination_word_count = 0
destination_file = open("generated", "w")

# Read in any predefined prepend values that should be used
# adding them to the destination file
prepend_file = open("res/prepend")
for line in filter(lambda l: l.rstrip(), prepend_file):
    destination_file.write(line)
    destination_word_count += 1
prepend_file.close()

print(f"Found {destination_word_count} valid lines to prepend")
required_word_count = total_line_count - destination_word_count
print(f"Will need {required_word_count} words from source")

# Read in the words from the source file to memory for use later
word_file = open("res/source")
word_file_lines = word_file.readlines()
words = []
for word in filter(lambda l: l.rstrip(), word_file_lines):
    if 4 <= len(word) <= 8:
        words.append(word.lower())
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
    while destination_word_count < total_line_count:
        chosen_word = random.choice(words)
        words.remove(chosen_word)
        destination_file.write(chosen_word)
        destination_word_count += 1
    destination_file.close()

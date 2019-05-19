import sys
import os
from collections import defaultdict
import re
import string

########################
# Mam plik 1gram, który zawiera różne słowa - zarówno poprawne jak i niepoprawne.
# Moim zadaniem jest stworzenie nowego pliku .txt, który zawiera jedynie poprawne
# słowa. Na pewno zdarzy się, że to samo słowo wystąpi co najmniej dwa razy.
# Następnie z pliku z pliku z poprawnymi słowami tworzony jest słownik, gdzie
# kluczem jest poprawne słowo, a wartością częstość jego występowania.
########################

def create_one_gram_model(file):
    """
    given a file containing words and their counts the function creates
    a new file with these words stripped from unnecessary characters.

    The side effect of the function is a file that contains cleaned words and
    their frequencies.
    """

    # it must be noted that the input files containg weird looking strings, e.g.
    # 1 lübau., 1 lubaszu..., 1 (lubek2002@wp.pl), 1 (lubi!), 1 13-000,
    # 3 "victory",
    # The strings containing no letters will be ignored. The rest of the lines
    # will be treated as follows:
    # > any leading or trailing non-letter characters will be removed
    # > any non-letter characters within the words (other than hyphens will
    # be removed
    # treatment will be applied as the file is being read line by line
    # it is checked whether the transformed word has already been read. If so
    # the count of the existing key is increased by the count of the
    # aforementioned word


    # the target file wiil be saved in the same directory as the input file
    target_file = os.path.join(os.path.dirname(file), "output_1gram.txt")

    # The dictionary is parametrised with integer so that it can handle updating
    # a value under a key that does not yet exists. Instead of surrounding the
    # update logic with try/except I use defaultdict which handles try/except
    # under the hood
    one_gram_model_dict = defaultdict(int)

    count = 0

    with open(file, 'r') as one_gram_file, open(target_file, 'w') as target:
        for line in one_gram_file:
            # delete leading whitespaces
            line = line.lstrip()
            count_part, character_part = line.split(" ")

            if int(count_part) == 9:
                print("Less frequent words!")
                # consider only words that occured at least 30 times
                break
            transformed_character_sequence = apply_word_treatment(character_part)

            if transformed_character_sequence != "":
                # if the word treatment decided that it is the valid word
                target.write(" ".join([count_part, \
                                       transformed_character_sequence, "\n"]))
                one_gram_model_dict[transformed_character_sequence] \
                                                            += int(count_part)

    # absolute counts must be transformed into probabilies <0, 1>
    total_count = sum(one_gram_model_dict.values())
    for word, abs_count in one_gram_model_dict.items():
        one_gram_model_dict[word] = float(one_gram_model_dict[word])
        one_gram_model_dict[word] /= total_count

    return one_gram_model_dict

def apply_word_treatment(dirty_word):
    """
    Given a dirty word return its clean form according to the following criterions

    If the given sequence of characters is considered a valid one (constituting
    a word) the transformed word is returned; if not an empty string is returned.
    """

    # delete trailing new-line character ("\n")
    dirty_word = dirty_word.rstrip()


    # ignore those lines that contain more numbers than letters
    number_count = 0
    letter_count = 0
    for char in dirty_word:
        # isalpha() checks whether the character is from the unicode alphabet
        if char.isalpha():
            letter_count += 1
        elif char.isnumeric():
            # also isdigit() and isdecimal() functions of similar functionality
            # are available
            number_count += 1
    if number_count > letter_count or letter_count == 0:
        return ""

    regex = r"-?((?:[A-Za-zęóąśłżźćńĘÓĄŚŁŻŹĆŃ](\.))*[A-Za-z0-9ęóąśłżźćńĘÓĄŚŁŻŹĆŃ]+(?:-[A-Za-zęóąśłżźćńĘÓĄŚŁŻŹĆŃ]+)*)-?\.?"
    subst = "\\1\2"
    result = re.sub(regex, subst, dirty_word, 0)
    result = result.replace("\x02", "")
    # the string module does not contain leading lower quotation mark typical
    # for Polish
    custom_punctuation = string.punctuation + "„”"
    result = result.strip(custom_punctuation)
    return max("", result)

if __name__ == "__main__":
    dictionary = create_one_gram_model(sys.argv[1])
    print(dictionary)

    # unittest.main()

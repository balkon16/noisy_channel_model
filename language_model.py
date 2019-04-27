import sys
import os
from collections import defaultdict
import regex #third-party library
import re
import unittest
import operator

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
    the dict of those words as keys and their count as values
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

    # one_gram_model_dict = defaultdict(int)

    count = 0

    with open(file, 'r') as one_gram_file, open(target_file, 'w') as target:
        for line in one_gram_file:
            # delete leading whitespaces
            line = line.lstrip()
            count_part, character_part = line.split(" ")

            if int(count_part) == 29:
                print("Less frequent words!")
                # consider only words that occured at least 30 times
                break
            transformed_character_sequence = apply_word_treatment(character_part)

            if transformed_character_sequence!= "":
                # if the word treatment decided that it is the valid word
                target.write(" ".join([count_part, transformed_character_sequence, "\n"]))


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

    # at this stage a primitive version is proposed; the function looks for
    # sequences of characters and given the resulting list is not empty the
    # first sequence is returned;

    # store the result of different RegExes
    regex_outputs = dict()

    # find basic patterns that consist of letter sequences, e.g. słowo, Polska
    basic_pattern = re.compile(r'[A-Za-zęóąśłżźćńĘÓĄŚŁŻŹĆŃ]+', flags=re.UNICODE)
    found_basic = "".join(re.findall(basic_pattern, dirty_word))
    regex_outputs[found_basic] = len(found_basic)

    # find patterns that look like this: k.p.c., m.in.
    with_dot_pattern = re.compile(r'([A-Za-zęóąśłżźćńĘÓĄŚŁŻŹĆŃ]+(?:\.))', \
    flags=re.UNICODE)
    found_with_dot = "".join(re.findall(with_dot_pattern, dirty_word))
    regex_outputs[found_with_dot] = len(found_with_dot)

    # find patterns with a hyphen
    with_hyphen_pattern = re.compile(r'[A-Za-zęóąśłżźćńĘÓĄŚŁŻŹĆŃ]+-[A-Za-zęóąśłżźćńĘÓĄŚŁŻŹĆŃ]+', \
    flags=re.UNICODE)
    found_with_hyphen = "".join(re.findall(with_hyphen_pattern, dirty_word))
    regex_outputs[found_with_hyphen] = len(found_with_hyphen)

    # TODO: dodać decydowanie, który output z trzech powyższych regexów wybrać

    # the criterion upon which the resulting word will be based on is the length
    # check the length of output for each regex and choose the one that produces
    # the longest sequence

    resulting_sequence = \
    max(regex_outputs.items(), key=operator.itemgetter(1))[0]


    # print("Następujące słowo ", dirty_word, " zostało zastąpione przez ", resulting_sequence)

    # return the longer one
    return max("", resulting_sequence)
    # if found_char_sequences:
    #     if len(found_char_sequences) > 1:
    #         print("Znaleziono więcej niż jedno słowo: ", dirty_word, \
    #         " Zapisano jako ", found_char_sequences[0])
    #     return found_char_sequences[0]
    # return ""


def words_with_hypens_inside(word):
    pass

class TestStringMethods(unittest.TestCase):

    def test_apply_word_treatment(self):
        self.assertEqual(apply_word_treatment("czerwony"), "czerwony")
        self.assertEqual(apply_word_treatment("żółty"), "żółty")
        self.assertEqual(apply_word_treatment("żółty123złoty"), "żółtyzłoty")
        # self.assertEqual(apply_word_treatment("biało-czarny"), "biało-czarny")
        self.assertEqual(apply_word_treatment("123"), "")
        # self.assertEqual(apply_word_treatment("..krach-krach"), "krach-krach")
        self.assertEqual(apply_word_treatment("@abc"), "abc")



if __name__ == "__main__":
    create_one_gram_model(sys.argv[1])
    # unittest.main()

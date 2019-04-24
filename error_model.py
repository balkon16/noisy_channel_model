"""
Error model's (or channel model's) job is to to compute the intended word c
given that we have observed the word w.

Generally we don't know what errors are made at what frequency. This can be
estimated by using the Wikipedia revision data.
"""

def dlEditDistance(word1, word2):
    """
    Compute Damerau–Levenshtein distance given two strings.
    """
    d = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    for i in range(-1,lenstr1+1):
        d[(i,-1)] = i+1
    for j in range(-1,lenstr2+1):
        d[(-1,j)] = j+1

    for i in range(lenstr1):
        for j in range(lenstr2):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1
            d[(i,j)] = min(
                           d[(i-1,j)] + 1, # deletion
                           d[(i,j-1)] + 1, # insertion
                           d[(i-1,j-1)] + cost, # substitution
                          )
            if i and j and s1[i]==s2[j-1] and s1[i-1] == s2[j]:
                d[(i,j)] = min(d[(i,j)], d[i-2,j-2] + cost) # transposition

    return d[lenstr1-1,lenstr2-1]

def edits1(word):
    "All edits that are one edit away from `word`."
    latin_letters    = 'abcdefghijklmnopqrstuvwxyz'
    polish_letters = 'ęóąśłźżćń'
    letters = latin_letters + polish_letters
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    # the candidate list usually contains few duplicates so set is used in order
    # to filter them out
    return set(deletes + transposes + replaces + inserts)


if __name__ == "__main__":
    # print(dlEditDistance("actress", "acress"))
    # print(dlEditDistance("złoto", "zloto"))
    # print(dlEditDistance("abc", ""))
    # print(dlEditDistance("zdrowy", "zdrowa"))
    print(edits1('somthing'))

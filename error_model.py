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

if __name__ == "__main__":
    print(dlEditDistance("actress", "acress"))
    print(dlEditDistance("złoto", "zloto"))
    print(dlEditDistance("abc", ""))
    print(dlEditDistance("zdrowy", "zdrowa"))

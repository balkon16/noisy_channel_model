def hamming_distance(string1, string2):
    "Given two strings compute Hamming distance between them"

    assert len(string1) == len(string2)

    return sum(ch1 != ch2 for ch1, ch2 in zip(string1, string2))

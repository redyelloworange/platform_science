def is_consonant(c: str):
    return not is_vowel(c)

def is_vowel(c: str):
    assert(len(c) == 1)
    return c.lower() in ('a', 'e', 'i', 'o', 'u')

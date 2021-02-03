import math
import re


def one_char_difference(first: str, second: str):
    """
    Checks if There is maximum of one char difference between first and second
    """
    if math.fabs(len(first) - len(second)) >= 2:
        return False

    for i, (c1, c2) in enumerate(zip(first, second)):
        if c1 != c2:
            return first[i + 1:] == second[i + 1:] \
                   or first[i:] == second[i + 1:] \
                   or first[i + 1:] == second[i:]

    return True


ALPHABET_WITH_HEBREW_PATTERN = r"[^a-zA-Zא-ת0-9]"


def validate_change(url: str, old: str, new: str):
    """
    Checks if there is a maximum of 1 char difference out of only the alphabet chars in old an new or if one has '?'
    and the second doesn't
    """
    if ("?" in old and "?" not in new) or ("?" in new and "?" not in old):
        return True

    old_stripped = re.sub(ALPHABET_WITH_HEBREW_PATTERN, '', old)
    new_stripped = re.sub(ALPHABET_WITH_HEBREW_PATTERN, '', new)

    return not one_char_difference(old_stripped, new_stripped)

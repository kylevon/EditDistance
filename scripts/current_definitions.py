import functools
import itertools


@functools.lru_cache(maxsize=20000)
def lev(w1, w2):
    if len(w2) == 0:
        return len(w1)
    if len(w1) == 0:
        return len(w2)
    if w1[0] == w2[0]:
        return lev(w1[1:], w2[1:])
    edit_1 = lev(w1[1:], w2)
    edit_2 = lev(w1, w2[1:])
    edit_3 = lev(w1[1:], w2[1:])
    return 1 + min(edit_1, edit_2, edit_3)


def projection(word, alphabet):
    return "".join(char for char in word if char in alphabet)


def languagePMk(language, alphabet, variables, k):
    out = set()
    min_length = max(0, min(set(len(word) for word in language)) - k)
    max_length = max(set(len(word) for word in language)) + k
    letters = alphabet | variables
    for length in range(min_length, max_length + 1):
        candidates = set(
            "".join(i)
            for i in itertools.product(*[letters for _ in range(length)]))
        for candidate in candidates:
            if candidate in language:
                out.add(candidate)
            for word in language:
                dgamma = lev(word, candidate)
                if dgamma <= k:
                    dsigma = lev(projection(word, alphabet),
                                 projection(candidate, alphabet))
                    if dsigma == dgamma:
                        if candidate == "axbxx":
                            print(
                                f"Candidate {candidate} matches with word {word}"
                            )
                            print(f"dsigma: {dsigma}, dgamma: {dgamma}")
                            input()
                        out.add(candidate)
                        break
    return out


print(lev("av", "abcas"))

alphabet = set("abc")
vars = {"x"}
language = {"axbxc"}
ref_words = {"x"}
print(languagePMk(language, alphabet, ref_words, 2))

previous_language = language.copy()
for k in range(1, 40):
    previous_language = languagePMk(previous_language, alphabet, ref_words, 1)
    should_be = languagePMk(language, alphabet, ref_words, k)
    if (should_be != previous_language):
        print(f"Languages are not the same, k = {k}, difference is:")
        print(should_be - previous_language)
        print(previous_language - should_be)
        break

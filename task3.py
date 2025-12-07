import timeit


# ---------- KMP (Knuth–Morris–Pratt) ----------

def compute_lps(pattern: str) -> list:
    """Build LPS (longest prefix-suffix) array for KMP."""
    lps = [0] * len(pattern)
    length = 0  # current length of matched prefix
    i = 1       # we start from second char

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                # go to previous longest prefix
                length = lps[length - 1]
            else:
                # no prefix so far
                lps[i] = 0
                i += 1

    return lps


def kmp_search(text: str, pattern: str) -> int:
    """Return first index of pattern in text using KMP, or -1 if not found."""
    if not pattern:
        return 0  # empty pattern convention

    lps = compute_lps(pattern)
    i = 0  # index in text
    j = 0  # index in pattern
    n = len(text)
    m = len(pattern)

    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
        else:
            if j != 0:
                j = lps[j - 1]  # jump using lps
            else:
                i += 1

        if j == m:
            return i - j  # match found

    return -1


# ---------- Boyer–Moore (bad character heuristic) ----------

def build_shift_table(pattern: str) -> dict:
    """Build shift table for Boyer–Moore bad-character rule."""
    table = {}
    m = len(pattern)

    # set shift for all chars except last
    for idx, ch in enumerate(pattern[:-1]):
        table[ch] = m - idx - 1

    # default shift for last char if not set
    table.setdefault(pattern[-1], m)
    return table


def boyer_moore_search(text: str, pattern: str) -> int:
    """Return first index of pattern in text using Boyer–Moore, or -1."""
    m = len(pattern)
    n = len(text)

    if m == 0:
        return 0

    shift_table = build_shift_table(pattern)
    i = 0  # index in text (start of current window)

    while i <= n - m:
        j = m - 1  # start from the end of pattern

        # compare backwards
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1

        if j < 0:
            return i  # full match

        # move window using last char in current window
        last_char = text[i + m - 1]
        i += shift_table.get(last_char, m)

    return -1


# ---------- Rabin–Karp ----------

def rabin_karp_search(text: str, pattern: str, base: int = 256, modulus: int = 101) -> int:
    """Return first index of pattern in text using Rabin–Karp, or -1."""
    m = len(pattern)
    n = len(text)

    if m == 0:
        return 0
    if m > n:
        return -1

    # precompute (base^(m-1)) % modulus for rolling hash
    h_mult = pow(base, m - 1, modulus)

    # initial hashes
    pattern_hash = 0
    window_hash = 0

    for i in range(m):
        pattern_hash = (pattern_hash * base + ord(pattern[i])) % modulus
        window_hash = (window_hash * base + ord(text[i])) % modulus

    for i in range(n - m + 1):
        # if hashes match, check substring directly (to avoid collisions)
        if pattern_hash == window_hash:
            if text[i:i + m] == pattern:
                return i

        # roll hash to next window
        if i < n - m:
            window_hash = (window_hash - ord(text[i]) * h_mult) % modulus
            window_hash = (window_hash * base + ord(text[i + m])) % modulus
            window_hash %= modulus

    return -1


# ---------- Benchmark helpers ----------

def measure_time(func, text: str, pattern: str, repeats: int = 10) -> float:
    """Return average execution time in seconds for given search function."""

    def stmt():
        return func(text, pattern)

    return timeit.timeit(stmt, number=repeats) / repeats


def load_text(path: str) -> str:
    """Read whole file as string."""
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


if __name__ == "__main__":
    # file names from task (put them in same folder)
    article1_path = "article1.txt"
    article2_path = "article2.txt"

    # load texts
    text1 = load_text(article1_path)
    text2 = load_text(article2_path)

    # choose real substrings that actually exist in each article
    # (replace these with real ones from your files)
    real_pattern_1 = "алгоритм"      # pattern from article1
    real_pattern_2 = "алгоритм"     # pattern from article2

    # fake pattern 
    fake_pattern = "qwerty123!@"

    algorithms = [
        ("KMP", kmp_search),
        ("Boyer-Moore", boyer_moore_search),
        ("Rabin-Karp", rabin_karp_search),
    ]

    print("=== Article 1 ===")
    for name, func in algorithms:
        t_real = measure_time(func, text1, real_pattern_1)
        t_fake = measure_time(func, text1, fake_pattern)
        print(f"{name}: real={t_real:.6f}s, fake={t_fake:.6f}s")

    print("\n=== Article 2 ===")
    for name, func in algorithms:
        t_real = measure_time(func, text2, real_pattern_2)
        t_fake = measure_time(func, text2, fake_pattern)
        print(f"{name}: real={t_real:.6f}s, fake={t_fake:.6f}s")

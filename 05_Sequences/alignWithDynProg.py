import numpy as np
import sys


def sigma(s1, s2, i, j, cons=1):
    if s1[i] == s2[j]:
        return cons
    else:
        return 0


def Aij(matrix, trace, i=1, j=1, gap=0, sigmaScore=-1):
    choices = np.array(
        [
            matrix[i - 1, j - 1] + sigmaScore,
            matrix[i - 1, j] + gap,
            matrix[i, j - 1] + gap,
        ]
    )
    # print(f"choices {choices}")
    choice = np.argmax(choices)
    score = choices[choice]
    matrix[i, j] = score
    trace[i, j] = choice
    return choice


def traceBack(matrix, trace, s="", t="", i=1, j=1):
    (n, m) = matrix.shape
    row = n - 1
    col = m - 1
    s1 = ""
    t1 = ""
    while row > 0 and col > 0:
        print(f"\ni = {row}, j = {col}")
        choice = trace[row, col]
        #  score = matrix[row, col]
        # if choice == 2:
        if choice == 0:
            print(f"{chr(8598)} s[{row-1}]={s[row-1]}\tt[{col-1}]={t[col-1]}")
            # print(D)
            # print(s[row-1])
            # print(t[col-1])
            s1 += s[row - 1]  # in s1 there's no initial gap
            t1 += t[col - 1]  # in t1 there's no initial gap
            row -= 1
            col -= 1
        elif choice == 1:
            print(f"{chr(8593)} s[{row-1}]={s[row-1]}\t-")
            # print('U')
            # print(s[row-1])
            print("-")
            s1 += s[row - 1]  # in s1 there's no initial gap
            t1 += "-"
            row -= 1
        else:
            print(f"{chr(8592)} -\tt[{col-1}]={t[col-1]}")
            # print('L')
            # print('-')
            # print(t[col-1])
            s1 += "-"
            t1 += t[col - 1]  # in t1 there's no initial gap
            col -= 1
    return (s1, t1)


if len(sys.argv) > 1:
    s = sys.argv[1]
    t = sys.argv[2]
else:
    s = "AGTCCCAT"
    t = "AGATTCCAT"
    # s = "AGTCCCAG"
    # s = "AGTCCCAT"
    # t = "AGATTCCATGGG"

alignMatrix = np.zeros((len(s) + 1, len(t) + 1), dtype="int")
traceMatrix = np.zeros_like(alignMatrix)

print(s + "\n" + t + "\n\n")

for row in np.arange(1, len(s) + 1):
    for col in np.arange(1, len(t) + 1):
        step = Aij(
            alignMatrix, traceMatrix, row, col, sigmaScore=sigma(s, t, row - 1, col - 1)
        )
        # print(f"step = {step}")
    # print()

print("\n", alignMatrix)
print("\n", traceMatrix)
print("\n\nalignement score: ", alignMatrix[len(s), len(t)], "\n")

print("\n\nTraceback")
sAlignedR, tAlignedR = traceBack(alignMatrix, traceMatrix, s, t)
print("\nbefore reversing")
print(sAlignedR)
print(tAlignedR)

c = len(sAlignedR) - 1
sAligned = ""
tAligned = ""
while c >= 0:
    sAligned += sAlignedR[c]
    tAligned += tAlignedR[c]
    c -= 1


print("\noriginal strings:\n" + s + "\n" + t + "\n\nThe Aligned Strings:")
print(sAligned)
print(tAligned)

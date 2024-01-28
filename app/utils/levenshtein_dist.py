def levenshtein_distance(str1, str2):
    matrix = [[0] * (len(str2) + 1) for _ in range(len(str1) + 1)]

    for i in range(len(str1) + 1):
        matrix[i][0] = i
    for i in range(len(str2) + 1):
        matrix[0][i] = i

    for i in range(1, len(str1) + 1):
        for j in range(1, len(str2) + 1):
            if str1[i - 1] == str2[j - 1]:
                tmp = 0
            else:
                tmp = 1
            matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + tmp)

    return matrix[-1][-1]

def find_minimum_levenshtein_distance(str1, words):
    min_distance = None
    for word in words:
        distance = levenshtein_distance(str1, word)
        if min_distance is None or distance < min_distance:
            min_distance = distance
    return min_distance
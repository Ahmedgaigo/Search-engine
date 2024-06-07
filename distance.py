def levenshtein_distance(s1, s2, cost_schema=None):
    if cost_schema is None:
        cost_schema = {'insert': 1, 'delete': 1, 'replace': 1}

    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i * cost_schema['delete']
    for j in range(n + 1):
        dp[0][j] = j * cost_schema['insert']

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(
                    dp[i - 1][j] + cost_schema['delete'],
                    dp[i][j - 1] + cost_schema['insert'],
                    dp[i - 1][j - 1] + cost_schema['replace']
                )

    return dp[m][n]


if __name__ == "__main__":
    print(levenshtein_distance("kitten", "sitting"))

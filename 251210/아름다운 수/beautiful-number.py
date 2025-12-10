def main() :
    n = int(input())

    # Please write your code here.
    dp = [0] * 11
    dp[0] = 1

    for i in range(1, n+1) :
        for d in range(1, 5) :
            if i - d >= 0 :
                dp[i] += dp[i-d]

    print(dp[n])

if __name__ == "__main__" :
    main()
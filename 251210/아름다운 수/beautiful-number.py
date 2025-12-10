def main() :
    n = int(input())
    ans = 0
    seq = []

    def is_beautiful() :
        # 연달아 같은 숫자가 나오는 시작 위치를 잡습니다.
        i = 0
        while i < n :
            # 만약 연속하여 해당 숫자만큼 나올 수 없다면
            # 아름다운 수가 아닙니다.
            if i + seq[i] - 1 >= n :
                return False
            # 연속하여 해당 숫자만큼 같은 숫자가 있는지 확인합니다.
            # 하나라도 다른 숫자가 있다면
            # 아름다운 수가 아닙니다.
            for j in range(i, i + seq[i]) :
                if seq[j] != seq[i] :
                    return False

            i += seq[i]

        return True

    def count_beautiful_seq(cnt) :
        nonlocal ans

        if cnt == n :
            if is_beautiful() :
                ans += 1
            return

        for i in range(1, 5) :
            seq.append(i)
            count_beautiful_seq(cnt + 1)
            seq.pop()

    count_beautiful_seq(0)
    print(ans)

if __name__ == "__main__" :
    main()
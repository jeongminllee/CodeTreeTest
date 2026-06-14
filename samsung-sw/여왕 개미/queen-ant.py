
if __name__ == "__main__" :
    Q = int(input())
    for _ in range(Q) :
        cmd = list(map(int, input().split()))
        c = cmd[0]

        if c == 100 :   # 마을 초기 상태
            # 초기상태는 오름차순으로 정렬된 개미집
            N, *ant_towns = cmd[1:]
            ant_towns = [-1] + ant_towns    # 0번 인덱스는 여왕개미집
        
        elif c == 200 : # 개미집 추가 건설 (p : 해당 위치에 개미집 건설)
            p = cmd[1]
            # 모든 좌표보다 큰 값이 주어지므로 정렬 신경쓸 필요 없음.
            ant_towns.append(p)
        
        elif c == 300 : # 개미집 삭제   (q : 해당 인덱스의 개미집 파괴)
            q = cmd[1]
            ant_towns[q] = -1   # 삭제는 하지말자. 인덱스 꼬임
            # 그러면 삭제가 되었다는 처리를 어디선가는 해야되는데 흠...

        elif c == 400 : # 개미집 정찰 (r: 정찰가는 개미 수)
            r = cmd[1]
            left, right = 0, 10 ** 9 + 1

            min_time = 0

            while left <= right :
                mid = (left + right) // 2

                interval = 0

                last = -10 ** 9

                for i in range(1, len(ant_towns)) :
                    if ant_towns[i] == -1 :
                        continue

                    curr_pos = ant_towns[i]

                    if curr_pos - last > mid :
                        last = curr_pos
                        interval += 1

                if interval <= r :
                    min_time = mid
                    right = mid - 1
                else :
                    left = mid + 1

            print(min_time)

import heapq

di = [-1, 1, 0, 0]
dj = [0, 0, -1, 1]

def dijkstra(si, sj, ei, ej) :
    heap = []
    heapq.heappush(heap, (0, si, sj, 1))    # sec, si, sj, k
    v[si][sj][1] = 0

    while heap :
        sec, ci, cj, k = heapq.heappop(heap)
        if (ci, cj) == (ei, ej) :
            return min(v[ei][ej])
        
        if v[ci][cj][k] < sec :
            continue

        if (ci,cj) == (si,sj) and k > 1 :
            continue

        v[ci][cj][k] = sec

        for d in range(4) :
            CAN_JUMP = True
            # 점프력 감소
            for nk in range(1, k) :
                cost = sec + 2
                ni, nj = ci + di[d] * nk, cj + dj[d] * nk

                if not (0 <= ni < N and 0 <= nj < N) or maps[ni][nj] == '#' :
                    CAN_JUMP = False
                    break

                if maps[ni][nj] == '.' and v[ni][nj][nk] > cost :
                    v[ni][nj][nk] = cost
                    heapq.heappush(heap, (cost, ni, nj, nk))

            if not CAN_JUMP :
                continue

            # 점프
            cost = sec + 1
            ni, nj = ci + di[d] * k, cj + dj[d] * k
            if not (0<=ni<N and 0<=nj<N) or maps[ni][nj] == '#' :
                CAN_JUMP = False
                continue

            if maps[ni][nj] == '.' and v[ni][nj][k] > cost :
                v[ni][nj][k] = cost
                heapq.heappush(heap, (cost, ni, nj, k))

            # 점프력 증가
            if 1 <= k < 5 :
                if not CAN_JUMP :
                    continue

                cost = sec + 1
                for nk in range(k+1, 6) :
                    ni, nj = ci + di[d] * nk, cj + dj[d] * nk
                    cost += nk ** 2
                    if not (0<=ni<N and 0<=nj<N) or maps[ni][nj] == '#' :
                        break

                    if maps[ni][nj] == '.' and v[ni][nj][nk] > cost :
                        v[ni][nj][nk] = cost
                        heapq.heappush(heap, (cost, ni, nj, nk))

    return min(v[ei][ej])


if __name__ == "__main__" :
    # 0. 초기값 세팅
    N = int(input())
    maps = [list(input()) for _ in range(N)]
    Q = int(input())

    for _ in range(Q) :
        journey = list(map(int, input().split()))
        for i in range(len(journey)) :
            journey[i] -= 1

        v = [[[10**9] * 6 for _ in range(N)] for _ in range(N)]

        res = dijkstra(*journey)
        if res == 10**9 :
            print(-1)

        else :
            print(res)
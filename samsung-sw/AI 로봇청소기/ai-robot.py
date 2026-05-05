from collections import deque

ROBOT_DIRECTION = [[-1, 0], [0, -1], [0, 1], [1, 0]]    # 상좌우하


def robots_move(robots : deque[list[int]], idx: int) :
    """
    robots : 로봇 청소기들 좌표
    idx : 현재 로봇 청소기 번호
    
    1. 청소기 이동
    이동 거리가 가장 가까운 오염된 격자로 이동. => 가장 가까운 이동거리를 구해야함. BFS
    물건이나 청소기가 있는 격자로는 이동불가.
    상하좌우로 인접한 격자를 한 칸씩 이동하여 도달하는 데 필요한 최소 이동 횟수를 의미
    우선순위 : 가장 가까운 먼지 > 행번호 > 열번호
    """
    robot_q = deque()
    visited = [[0] * N for _ in range(N)]

    # 각 로봇의 좌표를 담아서 이동. 만약 움직였는데 자기의 범위에 먼지가 없으면 -1, -1 로 보낼까? 
    movement = N*N+1
    res_robot = []

    for robot in robots :
        visited[robot[0]][robot[1]] = 1

    robot_q.append([0] + robots[idx]) # 이렇게 되면 [이동횟수, 행, 열] 이 되니까.

    while robot_q :
        move_cnt, rr, rc = robot_q.popleft()

        # 정답처리 : 먼지를 발견했다. 더 짧은 이동거리로.
        if maps[rr][rc] > 0 and movement >= move_cnt:
            movement = move_cnt
            res_robot.append([rr, rc])

        for dr, dc in ROBOT_DIRECTION :
            nr, nc = rr + dr, rc + dc
            
            # 네방향, 범위내, 미방문, 조건(박스가 있거나, 먼지 발견)
            if 0 <= nr < N and 0 <= nc < N and visited[nr][nc] != 1:
                # if maps[nr][nc] == -1 :
                #     continue
                
                if maps[nr][nc] >= 0 :
                    robot_q.append([move_cnt + 1, nr, nc])
                    visited[nr][nc] = 1
    if len(res_robot) == 0 :
        return robots[idx]
    else :
        res_robot.sort()
        return res_robot[0]


if __name__ == "__main__" :
    N, K, L = map(int, input().split()) # 격자 크기, 청소기 개수, 테스트 횟수
    maps = [list(map(int, input().split())) for _ in range(N)]
    
    robots = deque()
    
    for _ in range(K) :
        a, b = map(int, input().split())    # 격자 구조가 1, 1 ~ N, N 이라 -1 씩 해줌
        robots.append([a-1, b-1])
    
    # 테스트 결과만큼 돌리라 했으니까.
    for _ in range(L) :
        # 1. 로봇 청소기 이동
        for k in range(K) :
            moved_robots = robots_move(robots, k)
            robots[k] = moved_robots


        for k in range(K) :
            clean_direction = [
                [[0, 0], [-1, 0], [0, 1], [1, 0]],  # 오른쪽
                [[0, 0], [0, 1], [1, 0], [0, -1]],  # 아래쪽
                [[0, 0], [1, 0], [0, -1], [-1, 0]], # 왼쪽
                [[0, 0], [0, -1], [-1, 0], [0, 1]]  # 위쪽
            ]

            dust_amount = []
            for idx_direction in range(len(clean_direction)) :
                dust_cnt = 0
                for cr, cc in clean_direction[idx_direction] :
                    nr, nc = robots[k][0] + cr, robots[k][1] + cc

                    if 0 <= nr < N and 0 <= nc < N and maps[nr][nc] != -1 :
                        dust_cnt += min(20, maps[nr][nc])

                dust_amount.append([dust_cnt, idx_direction])
            dust_amount.sort(key=lambda x: (-x[0], x[1]))
        
            # 격자마다 청소 할 수 있는 최대 먼지량은 20 이라는 말은 각 격자마다 이겠지?
            # dust_amount[robot_idx][0] 을 가져오면 [먼지량, idx_direction]
            # 그럼 또 nr, nc 부여해서 max(0, maps[nr][nc] - 20) 하면 되겠네.
            dust_direction = dust_amount[0][1]
            for cr, cc in clean_direction[dust_direction] :
                nr, nc = robots[k][0] + cr, robots[k][1] + cc
                if 0 <= nr < N and 0 <= nc < N and maps[nr][nc] != -1 :
                    maps[nr][nc] = max(0, maps[nr][nc] - 20)

        # 3. 먼지 축적
        for i in range(N) :
            for j in range(N) :
                if maps[i][j] > 0 :
                    maps[i][j] += 5

        temp = [[0] * N for _ in range(N)]
        # 4. 먼지 확산
        for i in range(N) :
            for j in range(N) :
                if maps[i][j] == 0 :
                    dust_0 = 0
                    for di, dj in ROBOT_DIRECTION :
                        ni, nj = i + di, j + dj
                        if 0 <= ni < N and 0 <= nj < N and maps[ni][nj] > 0 :
                            dust_0 += maps[ni][nj]

                    temp[i][j] = (dust_0 // 10)

        for i in range(N) :
            for j in range(N) :
                if temp[i][j] > 0 :
                    maps[i][j] += temp[i][j]

        # 5. 출력
        cnt = 0
        for i in range(N) :
            for j in range(N) :
                if maps[i][j] > 0 :
                    cnt += maps[i][j]

        print(cnt)
        if cnt == 0 :
            break
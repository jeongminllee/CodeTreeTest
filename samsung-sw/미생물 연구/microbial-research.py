# ====================
"""
미생물 연구
N*N 정사각형 크기의 배지 

1. 미생물 투입
- 좌측 하단 좌표 (r1, c1), 우측 상단 좌표 (r2, c2) 직사각형 영역에 한 무리의 미생물 투입
- 만약 영역 내에 다른 미생물이 존재한다면 새로 투입된 미생물이 그 영역 내의 미생물들을 잡아먹음.
- 기존에 있던 어떤 미생물 무리 A가 새로 투입된 미생물 무리 B에게 잡아먹히면서 A무리가 차지한 영역이
    둘 이상 나눠지게 되면 나눠진 A무리의 미생물은 배지에서 모두 사라짐.

2. 배지 이동
- 모든 미생물을 새로운 배지로 이동. 새로운 배지의 크기도 기존 용기와 동일. 
- 이 과정은 기존 배지에 미생물이 한 마리도 존재하지 않을 떄 까지 다음 작업을 반복
- 기존 배지에 있는 무리 중 가장 차지한 영역이 넓은 무리를 하나 선택, 
- 만약 이런 미생물 무리가 둘 이상이면 먼저 투입된 미생물 선택
- 우선순위 : 크기 > idx
- 선택된 미생물 무리를 새 배지로 옮김. 
- 이 때, 무리는 기존 용기에서의 형태를 유지해야 함.
- 미생물 무리가 차지한 영역이 배양 용기의 범위를 벗어나지 않고, 
- 다른 미생물의 영역과 겹치지 않도록 두어야 함.
- 이 조건 안에서 최대한 x좌표가 작은 위치로 미생물을 옮겨야 함. 
- 그런 위치가 둘 이상일 경우 최대한 y좌표가 작은 위치로 옮겨야 함.
- 우선순위 : x좌표 > y좌표
- 만약 어떤 곳에도 둘 수 없는 미생물 무리가 발견되면, 그 미생물 무리는 사라짐.

3. 실험 결과 기록
- 미생물 무리 중 상하좌우로 맞닿은 면이 있는 무리끼리는 '인접한 무리' 라고 표현함.
- 모든 '인접한 무리' 쌍을 확인. 이때 두 무리 A와 B가 맞닿은 면이 둘 이상이더라도 (A, B) 쌍은 한 번만 확인
- 확인한 두 무리가 A, B라면 (A영역) * (B영역) 만큼의 성과를 얻음.
- 확인한 모든 쌍의 성과를 더한 값이 이 실험의 결과. 이 값을 기록

"""

from collections import deque

di = [-1, 1, 0, 0]
dj = [0, 0, -1, 1]

def microoranism_insert(maps: list[list[int]], lst:list[int], num:int) :
    r1, c1, r2, c2 = lst
    for i in range(c1, c2) :
        for j in range(r1, r2) :
            maps[i][j] = num

def group() -> list[int]:
    v = [[0] * N for _ in range(N)]
    glst = []

    for si in range(N) :
        for sj in range(N) :
            # 미방문 미생물이면 그룹
            if v[si][sj] == 0 and maps[si][sj] > 0 :
                tlst = bfs(v, si, sj)
                glst.append(tlst)

    return glst

def bfs(v:list[list[int]], si:int, sj:int) -> list[list[int, int]] :
    q = deque()
    start_num = maps[si][sj]
    res_lst = []

    q.append((si, sj))
    v[si][sj] = start_num
    res_lst.append(start_num)
    res_lst.append([si, sj])

    while q :
        ci, cj = q.popleft()
        # 네 방향, 범위 내, 미방문, 조건(같은 값이면)
        for d in range(4) :
            ni, nj = ci + di[d], cj + dj[d]
            if 0<=ni<N and 0<=nj<N and v[ni][nj] == 0 and maps[ni][nj] == start_num :
                q.append((ni, nj))
                v[ni][nj] = start_num
                res_lst.append([ni, nj])

    return res_lst  # [start_num, [i, j], [i, j], ...]

def del_sort(glst:list[list[int]]) -> list[list[int]] :
    del_set = set() # 삭제할 그룹 인덱스
    for i in range(len(glst) - 1) :
        for j in range(i+1, len(glst)) :    # 가능한 2개를 선택하는 모든 조합
            if glst[i][0] == glst[j][0] :   # 가은 미생물 번호를 가진 그룹
                del_set.add(i)
                del_set.add(j)

    for i in range(len(glst)-1, -1, -1) :   # 삭제는 뒤부터
        if i in del_set :
            glst.pop(i)                     # 삭제
    # 정렬(크기가 큰 순, 번호가 작은순)
    glst.sort(key=lambda x:(-len(x), x[0]))

    # 그룹 내 좌표를 (0, 0) 기준의 상대좌표로 저장
    for lst in glst :
        # i, j 최소값 구하기 => (si, sj) => 모든 좌표에서 -si, -sj
        si, sj = N, N
        for ci, cj in lst[1:] : # lst[0] 은 미생물 번호
            si = min(si, ci)
            sj = min(sj, cj)

        for idx in range(1, len(lst)) :     # 모든 좌표를 (0, 0) 기준 상대좌표로 저장
            lst[idx][0] -= si
            lst[idx][1] -= sj

    return glst

def move(glst:list[list[int]]) -> list[list[int]]:
    new_maps = [[0] * N for _ in range(N)]

    for lst in glst :   # 한 그룹씩 배치 가능한 최소 위치(si, sj)에 배치
        start = lst[0]
        si, sj = check(new_maps, lst[1:])   # 가능한 시작 좌표 리턴, 불가능한 경우 (-1, -1) 리턴
        if (si, sj) != (-1, -1) :
            for ci, cj in lst[1:] :
                new_maps[si+ci][sj+cj] = start

    return new_maps

def check(maps:list[list[int]], lst: list[int]) :
    # 최소열/최소행 기준으로 배치가능한지 확인 체크 후 기준좌표 리턴(불가능 시 (-1,-1))
    for sj in range(N) :
        for si in range(N) :    # 가능한 모든 기준위치
            # 기준 (si, sj)에 더한 모든 좌표가 범위내이고, 0이면 성공
            for ci, cj in lst :
                if si+ci >= N or sj+cj >= N or maps[si+ci][sj+cj] != 0 :
                    break

            else :      # 모든 좌표 배치 가능
                return si, sj
    # 가능한 기준좌표 없음
    return -1, -1

# 내 그룹개수를 세고(cnt), 인접한 다른 블럭들 카운트(cnts) 구해서 곱해서 누적
def recode_res(maps:list[list[int]]) :
    v = [[0] * N for _ in range(N)]
    res = 0

    for si in range(N) :
        for sj in range(N) :
            # 미방문 세포 만나면 점수 계산
            if v[si][sj] == 0 and maps[si][sj] > 0 :
                t = bfs_score(v, si, sj)
                res += t

    return res

def bfs_score(v:list[list[int]], si:int, sj:int) :
    q = deque()
    w = [[0]* N for _ in range(N)]
    cnts = []

    q.append((si, sj))
    v[si][sj] = 1
    cnt = 1

    while q :
        ci, cj = q.popleft()
        # 네방향, 범위내, 미방문
        for d in range(4) :
            ni, nj = ci + di[d], cj+dj[d]

            if 0<=ni<N and 0<=nj<N and v[ni][nj] == 0 :
                if maps[ni][nj] == maps[si][sj] :   # 같은 미생물 cnt 세기
                    q.append((ni, nj))
                    v[ni][nj] = 1
                    cnt += 1

                # 다른 미생물이면 첫 발견시 그 세포의 개수 세기 (방문 표시 w) 
                elif maps[ni][nj] > 0 and w[ni][nj] == 0 :
                    tcnt = bfs_adj(w, ni, nj)
                    cnts.append(tcnt)

    res = 0
    for other_cnt in cnts :
        res += cnt * other_cnt

    return res

def bfs_adj(v:list[list[int]], si:int, sj:int) :
    # 같은 값일 때 그 개수 세고 리턴
    q = deque()

    q.append((si, sj))
    v[si][sj] = 1
    cnt = 1

    while q :
        ci, cj = q.popleft()
        # 네방향, 범위내, 미방문, 조건(같은 값)
        for d in range(4) :
            ni, nj = ci + di[d], cj+dj[d]

            if 0<=ni<N and 0<=nj<N and v[ni][nj] == 0 and maps[si][sj] == maps[ni][nj]:
                q.append((ni, nj))
                v[ni][nj] = 1
                cnt += 1

    return cnt

if __name__ == "__main__" :
    N, Q = map(int, input().split())
    maps = [[0] * N for _ in range(N)]

    for test_num in range(1, Q+1) :
        input_lst = list(map(int, input().split())) # r1, c1, r2, c2

        # 1. 미생물 투입
        microoranism_insert(maps, input_lst, test_num)

        # 2. 배지 이동 glst = [미생물번호, [i1,j1],[i2,j2],...]
        glst = group()

        # 3. 쪼개진 개체 삭제 및 정렬 (크기, 오래된 : 미생물 번호가 작은)
        glst = del_sort(glst)

        # 4. 넓이가 큰, 오래된 순으로 정렬된 그룹 이동 (재배치)
        maps = move(glst)

        # 5. 결과 기록
        res = recode_res(maps)

        print(res)
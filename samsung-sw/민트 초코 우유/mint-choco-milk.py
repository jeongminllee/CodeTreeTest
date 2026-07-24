from collections import deque

# 위 아래 왼쪽 오른쪽
di = [-1, 1, 0, 0]
dj = [0, 0, -1, 1]

def is_valid(i, j) :
    return 0 <= i < N and 0 <= j < N

# 점심 함수. 대표자 찾기
def noon(si, sj) -> tuple :
    q = deque()
    q.append((si, sj))
    visited[si][sj] = 1
    
    cnt = 1
    ri, rj = si, sj # 그룹의 대표자 후보 (초기값 설정)

    while q :
        ci, cj = q.popleft()

        # 우선순위에 따라 정렬
        if (n_arr[ri][rj], -ri, -rj) <= (n_arr[ci][cj], -ci, -cj) :
            ri, rj = ci, cj

        for d in range(4) :
            ni, nj = ci + di[d], cj + dj[d]

            if is_valid(ni, nj) and visited[ni][nj] == 0 and\
                  f_arr[ni][nj] == f_arr[ri][rj] :
                q.append((ni, nj))
                visited[ni][nj] = 1
                cnt += 1

    n_arr[ri][rj] += cnt

    return ri, rj

# 저녁 우선순위 정하기
def dinner_priority(meal) -> int :
    if meal in {1, 2, 4} :  # 단일 음식
        return 1
    elif meal in {3, 5, 6} :    # 이중 음식
        return 2
    else :          # 삼중음식
        return 3
    

if __name__ == "__main__" :
    N, T = map(int, input().split())

    f_arr = [list(input()) for _ in range(N)]
    n_arr = [list(map(int, input().split())) for _ in range(N)]

    dct = {'M' : 1, 'C' : 2, 'T' : 4}   # 비트 001, 010, 100

    # f_arr 을 문자 -> 숫자(bit)로 바꿈
    for i in range(N) :
        for j in range(N) :
            f_arr[i][j] = dct[f_arr[i][j]]

    for _ in range(T) :
        # 1. 아침 + 점심
        # 아침 겸 점심 
        # 인접한 학생들과 신봉 음식이 완전히 같은 경우에만 그룹을 형성.
        # 아침 : 모든 학생 신앙심 + 1
        # 점심 : 대표자 += 그룹원 수 - 1, 그룹원 -= 1
        # 아침 + 점심 => 대표자 += 그룹원 수, 그룹원은 그대로

        # 그룹 내 대표자 1명 선정
        # 우선순위 : 신앙심 > i > j
        # bfs를 돌려서 대표자 리스트에 넣자. 
        rep_list = []       # 대표자 리스트
        visited = [[0] * N for _ in range(N)]   # 방문 리스트
        for i in range(N) :
            for j in range(N) :
                if visited[i][j] == 0 :
                    ri, rj = noon(i, j)     # 대표자 좌표 BFS로 찾기
                    rep_list.append((ri, rj))   # 대표자 리스트에 대표자 좌표 입력

        # 저녁
        # 전파 = 그룹 순대로
        # 민트, 초코, 우유, 초코우유, 민트우유, 민트초코, 민트초코우유
        # [4, 2, 1], [3, 5, 6], [7]
        # 1번 우선순위 : 단일음식, 이중음식, 삼중음식
        # 2번 우선순위 : 같은 그룹 내에서는 대표자의 신앙심 > 행 > 열
        
        # 전파자는 신앙심 중 1만 남기고 간절함 = 신앙심 - 1 로 바꿔 전파에 사용
        # 전파 방향은 (변경 전 신앙심 % 4) => (간절함 + 1 % 4) 에 의해 결정. 0, 1, 2, 3
        # 전파할 방향으로 한 칸씩 이동하면서 전파를 시도. 격자 밖으로 나가거나 간절함이 0이 되면 종료
        # 같은 음식을 신봉하는 경우, 전파하지 않고 다음 진행
        # 다른 음식을 신봉하는 경우, 전파 진행.
        # 전파자 > 대상 : 강한 전파
        # 전파자는 간절함이 대상 + 1 만큼 깎이며, 전파 대상의 신앙심은 1 증가, 대상의 신봉 음식 = 전파자 음식
        # 이때 간절함이 0이 되면 더 이상 전파를 진행하지 않고 종료.
        # 전파자 <= 대상 : 약한 전파
        # 대상은 전파자의 음식에도 관심을 가짐.
        # 전파자는 간절함이 0이 되고, 대상의 신앙심은 간절함만큼 증가

        # [[], [단일 음식], [이중 음식], [삼중 음식]]
        dinner_list = [[] for _ in range(4)]

        for ri, rj in rep_list :
            priority = dinner_priority(f_arr[ri][rj])   # 대표자가 신봉하는 음식 우선순위
            dinner_list[priority].append([-n_arr[ri][rj], ri, rj])  # 음식의 우선순위에 맞게 입력
            
        for i in range(1, 4) :
            dinner_list[i].sort()   # 신앙심이 클수록, i가 작을수록, j가 작을수록

        # 만약 전파 되었다면 방어상태 돌입
        # 처음에 이게 왜 필요하냐 생각했는데 만약 대표자가 전파 되었으면 방어상태가 되어서 전파를 진행하지 않음.
        is_defend = [[0] * N for _ in range(N)]
        
        for dinner in dinner_list[1:] :
            if len(dinner) == 0 :
                continue

            for _, ri, rj in dinner :
                if is_defend[ri][rj] :
                    continue

                score = n_arr[ri][rj] - 1   # 간절함 = 신앙심 - 1
                n_arr[ri][rj] = 1           # 신앙심 = 1

                dr = (score+1) % 4          # 신앙심 % 4 이기 때문에 간절함 + 1 을 하였음.
                food = f_arr[ri][rj]        # 현재 신봉 음식

                while True :
                    ri, rj = ri + di[dr], rj + dj[dr]

                    if not is_valid(ri, rj) or score <= 0 :
                        break

                    if food == f_arr[ri][rj] :
                        continue
                    
                    # 전파 대상은 방어 상태
                    is_defend[ri][rj] = 1

                    if score > n_arr[ri][rj] :
                        f_arr[ri][rj] = food        # 강한 전파
                        n_arr[ri][rj] += 1
                        score -= n_arr[ri][rj]
                    
                    else :
                        f_arr[ri][rj] |= food       # 약한 전파 or 연산(|)을 진행.
                        n_arr[ri][rj] += score
                        break           # 요거 break 반드시 해줄것. 아니면 score = 0 처리

        food_list = [0] * 8     # 신봉 음식 리스트
        for i in range(N) :
            for j in range(N) :
                food_list[f_arr[i][j]] += n_arr[i][j]   # 맵을 돌면서 현재 신앙심 더해나가기.

        # dct = {'M' : 1, 'C' : 2, 'T' : 4}
        for i in (7, 6, 5, 3, 1, 2, 4) :    # 순서대로.
            print(food_list[i], end=' ')    # print(food_list[7], ... 해도 됨.)
        print()

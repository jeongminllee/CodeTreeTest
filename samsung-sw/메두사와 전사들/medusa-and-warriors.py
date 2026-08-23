'''
도로 위 최단경로로 움직이는 메두사와 격자 어디든 최단거리로 좁혀오는 전사들을 턴 단위로 시뮬레이션하는 문제
[1] 메두사의 이동 (도로 전용 최단경로)
- 공원에서 시작하는 BFS 한 번으로 모든 칸의 최단거리 dist를 만들고, 매 턴 거리값이 감소하는 이웃으로 
    상, 하, 좌, 우 우선순위로 1칸 이동

[2] 시야(90도) + 가림 처리
- 바라보는 방향의 "세 갈래(dr-1, dr, dr+1)" 로 시야를 퍼트리고(=1), 시야 레이 상에서 먼저 만난 전사가
    그 "뒤쪽(같은 갈래)"을 가려서 보이지 않게(=0) 만드는 방식으로 처리
- 네 방향 중 가장 많은 전사가 보이는 방향을 선택 (동률이면 상, 하, 좌, 우)

[3] 전사 이동(시야 금지 + 2칸까지)
- "석화(=1)"된 전사는 이번 턴 이동 불가
- 나머지는 메두사와의 맨해튼 거리 감소를 만족하며, 1번째 이동은 상,하,좌,우, 2번째 이동은 좌,우,상,하
- 이동 전, 후 메두사와 같은 칸인 전사는 즉시 사라짐(공격자 수 집계는 "이동 후"에 발생한 것만.)

고민거리
[1] 시야90도와 가림을 구현
- 1. 메두사 위치에서 해당 방향의 3갈래 벡터만 써서 BFS로 시야를 모두 1로 표시. 
이때 전사를 만나면 큐에 기록(갈래 표시:좌,직선,우)
- 2. 기록한 전사마다 같은 갈래로 뒤쪽을 따라가며 다시 0으로 지움. 이렇게 표시->지우기 2단계로하면
"가까운 전사가 먼 전사를 가리는" 규칙이 자연스럽게 성립
    
[2] 여러 전사가 같은 칸에 있으면
- 칸 별로 unordered_set<int> 를 둬 전사 인덱스 집합을 관리
    - 시야 집계(석화 수): set 크기만 더하면 끝
    - 동일 칸 다수 삭제/이동 : 인덱스 중심으로 안정적으로 처리
    
[3] 전사 삭제 
- 전사는 자주 사라지므로 O(1)에 가까운 삭제가 요구
- pop-back swap(배열의 마지막 원소와 스왑 후 pop) 기법으로 전사 배열을 관리하고, 
    스왑된 전사의 인덱스를 해당 칸의 집합에서 갱신하면 효율적

[4] 최단경로를 매 턴 어떻게 구할까
- 메두사의 경로는 도로 그래프 고정이므로 공원에서의 BFS 1회로 충분함
- 매 턴은 거리 감소 + 방향 우선순위만 확인해 1칸 이동
'''
from collections import deque



# 방향 우선순위
P1 = [(-1, 0), (1, 0), (0, -1), (0, 1)] # 상하좌우
P2 = [(0, -1), (0, 1), (-1, 0), (1, 0)] # 좌우상하

# 시야(90도) 3갈래: 상하좌우
VISION_DXYS = [
    [(-1,-1), (-1,0), (-1, 1)],     # 상
    [(1, -1), (1, 0), (1, 1)],      # 하
    [(-1, -1), (0, -1), (1, -1)],   # 좌
    [(-1, 1), (0, 1), (1, 1)]       # 우
]
######################################################

class WarriorMap :
    """
    전사 배열 + 칸 별 전사 인덱스 집합. pop-back swap 으로 O(1) 삭제 지향
    """
    def __init__(self, N, init_warriors):
        self.N = N
        self.warriors = list(init_warriors) # [(x, y), ...]
        self.cells = [[set() for _ in range(N)] for _ in range(N)]
        for i, (x, y) in enumerate(self.warriors) :
            self.cells[x][y].add(i)

    def _erase_index_from_cell(self, idx):
        x, y = self.warriors[idx]
        self.cells[x][y].discard(idx)

    def _add_index_to_cell(self, idx):
        x, y = self.warriors[idx]
        self.cells[x][y].add(idx)

    def remove_warrior(self, idx):
        """인덱스 전사 제거: 마지막과 스왑 후 pop"""
        self._erase_index_from_cell(idx)
        last = len(self.warriors) - 1
        if idx != last :
            # 스왑
            self.warriors[idx] = self.warriors[last]
            # 셀의 집합에서 last 인덱스를 없애고 idx로 바꿈
            x, y= self.warriors[idx]
            self.cells[x][y].discard(last)
            self.cells[x][y].add(idx)
        self.warriors.pop()
        # self.warriors.pop(idx)

    def remove_same_cell(self, mx, my):
        """메두사와 같은 칸 전사 모두 제거. 제거 수 반환"""
        removed = 0
        i = 0
        while i < len(self.warriors) :
            if self.warriors[i][0] == mx and self.warriors[i][1] == my :
                self.remove_warrior(i)
                removed += 1
            else :
                i += 1
        return removed

    def is_warrior_at(self,x,y):
        return len(self.cells[x][y]) > 0

    def move_warrior_once(self, idx, mx, my, vision_map, pri):
        """전사 idx를 pri 우선순위로 1칸 이동 시도, 성공 시 1, 아니면 0"""
        x, y= self.warriors[idx]
        d0 = manhattan(x, y, mx, my)
        N = self.N
        for dx, dy in pri :
            nx, ny = x + dx, y + dy
            if not in_range(nx, ny, N) :
                continue
            if vision_map[nx][ny] == 1 :    # 시야로는 이동 불가
                continue
            if manhattan(nx, ny, mx, my) < d0 :
                # 셀 집합에서 인덱스 이동
                self.cells[x][y].discard(idx)
                self.warriors[idx] = (nx, ny)
                self.cells[nx][ny].add(idx)
                return 1
        return 0

    def warriors_move(self, vision_map, mx, my):
        """석화되지 않은 전사들의 이동(최대 2칸); (총 이동 칸 수, 공격자 수)"""
        # 메두사와 같은 칸 전사 제거 (이들은 공격자 집계와 무관)
        self.remove_same_cell(mx, my)

        steps_sum = 0
        # 이동 가능한 전사만 이동 (현재 위치가 시야 밖)
        i = 0
        while i < len(self.warriors) :
            x, y = self.warriors[i]
            if vision_map[x][y] == 0 :
                steps_sum += self.move_warrior_once(i, mx, my, vision_map, P1)
                steps_sum += self.move_warrior_once(i, mx, my, vision_map, P2)
            i += 1

        # 이동 후 메두사와 같은 칸 전사 제거 -> 공격자
        attackers = self.remove_same_cell(mx, my)
        return steps_sum, attackers

def move_medusa_one(dist, x, y) :
    """메두사를 1칸 이동(거리 감소 + 상하좌우 우선). 이동 후 좌표 반환"""
    N = len(dist)
    for dx, dy in P1 :
        nx, ny = x + dx, y + dy
        if in_range(nx, ny, N) and dist[nx][ny] != -1 and dist[nx][ny] < dist[x][y] :
            return nx, ny
    return x, y # 이동 불가 케이스는 문제상 발생하지 않음(경로 존재 가정)

def get_vision_map(N, wmap: WarriorMap, mx, my, dxys3) :
    """해당 방향의 시야 맵(1)과 시야에 보이는 전사 수 반환"""
    vision = [[0] * N for _ in range(N)]
    seen_cnt = 0

    # 보인 전사(가림 시작점)
    # type 0(좌 대각), 1(직선), 2(우 대각)
    vis_q = deque()

    # 1) 표시 BFS : 3갈래로만 퍼트리며 시야 칠하기
    q = deque()
    q.append((mx, my))
    while q :
        x, y = q.popleft()
        for dxi, dyi in dxys3 :
            nx, ny = x + dxi, y + dyi
            if not in_range(nx, ny, N) or vision[nx][ny] == 1 :
                continue
            # 전사를 처음 만났다면 갈래 타입 분류
            if wmap.is_warrior_at(nx, ny) :
                if nx == mx or ny == my :
                    vis_q.append((nx, ny, 1))
                else :
                    # dxys3[0]과 같은 부호면 좌, 아니면 우
                    if (nx-mx) * dxys3[0][0] > 0 and (ny-my) * dxys3[0][1] > 0 :
                        t = 0
                    else :
                        t = 2
                    vis_q.append((nx, ny, t))

            vision[nx][ny] = 1
            q.append((nx, ny))

    # 2) 가림 BFS: 전사 뒤쪽(같은 갈래)을 0으로 지움
    while vis_q :
        x, y, t = vis_q.popleft()
        for d, (dxi, dyi) in enumerate(dxys3) :
            if t == 1 and d != 1 :
                continue
            if t == 0 and d == 2 :
                continue
            if t == 2 and d == 0 :
                continue
            nx, ny = x + dxi, y + dyi
            if not in_range(nx, ny, N) or vision[nx][ny] == 0 :
                continue
            vision[nx][ny] = 0
            vis_q.append((nx, ny, t))

    # 시야에 남은 칸의 전사 수 (칸 별 집합 크기 합)
    for i in range(N) :
        row_cells = wmap.cells[i]
        vrow = vision[i]
        for j in range(N) :
            if vrow[j] :
                seen_cnt += len(row_cells[j])

    return vision, seen_cnt



def bfs_dist_from_target(arr, ex, ey) :
    # 도로(0)만 통과, (ex, ey)에서 모든 칸까지 최단거리
    N = len(arr)
    dist = [[-1] * N for _ in range(N)]
    q = deque()
    q.append((ex, ey))
    dist[ex][ey] = 0

    while q :
        x, y = q.popleft()
        for dx, dy in P1 :  # 상하좌우
            nx, ny = x + dx, y + dy
            if not in_range(nx, ny, N) or arr[nx][ny] or dist[nx][ny] != -1 :
                continue
            dist[nx][ny] = dist[x][y] + 1
            q.append((nx, ny))
    return dist

def in_range(x, y, N) :
    return 0<=x<N and 0<=y<N

def manhattan(ax, ay, bx, by) :
    return abs(ax - bx) + abs(ay - by)

######################################################
def main() :
    N, M = map(int, input().split())            # 맵 크기, 전사 수
    sx, sy, ex, ey = map(int, input().split())  # 메두사집, 공원 좌표

    pos = list(map(int, input().split()))
    init_warriors = []
    for idx in range(0, M*2, 2) :
        ax, ay = pos[idx], pos[idx+1]
        init_warriors.append((ax,ay))

    arr = [list(map(int, input().split())) for _ in range(N)]

    dist = bfs_dist_from_target(arr, ex, ey)
    if dist[sx][sy] == -1 :
        print(-1)
        return

    wmap = WarriorMap(N, init_warriors)

    mx, my = sx, sy
    out_lines = []
    while not (mx == ex and my == ey) :
        # [1] 메두사 이동
        mx, my = move_medusa_one(dist, mx, my)
        if mx == ex and my == ey :
            out_lines.append("0")
            break

        # [2] 시야 방향 선택 : 전사가 많은 쪽, 상하좌우 순
        best_seen = -1
        best_vision = None

        for d in range(4) :
            vision_map, seen = get_vision_map(N, wmap, mx, my, VISION_DXYS[d])
            if seen > best_seen :
                best_seen = seen
                best_vision = vision_map

        # [3] 전사 이동
        steps_sum, attackers = wmap.warriors_move(best_vision, mx, my)

        # 출력 : 전사 총 이동칸 수, 석화 수(=best_seen), 공격자 수
        out_lines.append(f"{steps_sum} {best_seen} {attackers}")

    for lines in out_lines :
        print(lines)

if __name__ == "__main__" :
    main()

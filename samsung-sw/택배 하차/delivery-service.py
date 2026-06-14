# ====================
import heapq

# box 객체
class Box :
    def __init__(
            self,
            idx: int,
            h : int,
            w : int,
            c : int):
        self.idx = idx
        self.h = h
        self.w = w
        self.c = c
        self.sr = 0     # start row
        self.sc = c     # start col

        self.rcs = []
        for r in range(h) :
            for c in range(w) :
                self.rcs.append([r, c])

# 박스 아래로 내려감.
def draw_box(maps:list[list[int]], box : Box) :
    for r, c in box.rcs :
        nr, nc = box.sr + r, box.sc + c
        maps[nr][nc] = box.idx


# 박스가 들어가면서
def box_move(
        maps:list[list[int]], 
        box : Box, 
        N: int) :
    movable = True  # 움직일 수 있는지에 대한 flag

    for sr in range(box.sr, N+1) :
        for r, c in box.rcs :
            nr, nc = sr + r, box.sc + c
            if maps[nr][nc] != 0 :
                movable = False
                break

        if movable :
            box.sr = sr
            continue
        else :
            break

    draw_box(maps, box)

def is_left_zero(
        maps:list[list[int]], 
        box : Box, 
        N: int) -> bool:
    for r in range(box.sr, box.sr + box.h) :
        if sum(maps[r][1:box.c]) == 0 : # 박스와 맞닿는 부분이 전부 0이면
            continue
        else :
            return False
        
    return True

def is_right_zero(
        maps:list[list[int]], 
        box : Box, 
        N: int) -> bool:
    for r in range(box.sr, box.sr + box.h) :
        local_begin = box.c + box.w
        local_length = (N+1)

        if sum(maps[r][local_begin:local_length]) == 0 : # 박스와 맞닿는 부분이 전부 0이면
            continue
        else :
            return False
        
    return True

def clear_box(maps:list[list[int]], box : Box) :
    for r in range(box.sr, box.sr + box.h) :
        for c in range(box.sc, box.sc + box.w) :
            maps[r][c] = 0

if __name__ == "__main__" :
    N, M = map(int, input().split())
    maps = []       # 맵

    for _ in range(N) :
        maps.append([-1] + [0] * N + [-1])  
    maps.append([-1] * (N + 2))             # 양 옆과 바닥을 -1로 패딩
    boxes = {}                              # Box 객체 담을 딕셔너리
    orders = []                             # 순서 담을 리스트

    for _ in range(M) :
        box_idx, h, w, c = map(int, input().split())
        boxes[box_idx] = Box(box_idx, h, w, c)
        box_move(maps, boxes[box_idx], N)
        orders.append(box_idx)

    left_right = True

    while len(boxes) > 0 :
        candidates = [] # 박스 하나씩 뺄 수 있는 후보군들
        
        # 택배 하차 (좌측)
        if left_right :
            left_right = False

            for key in orders :
                if is_left_zero(maps, boxes[key], N) :
                    heapq.heappush(candidates, key) # 후보군들을 cand 에 넣음

        # 택배 하차 (우측)
        else :
            left_right = True
            
            for key in orders :
                if is_right_zero(maps, boxes[key], N) :
                    heapq.heappush(candidates, key) # 후보군들을 cand 에 넣음

        delete_idx = heapq.heappop(candidates)  # 삭제할 박스를 꺼냄
        print(delete_idx)                       # 출력
        clear_box(maps, boxes[delete_idx])      # 해당 위치를 0으로 초기화
        orders.remove(delete_idx)               # 박스 제거
        del boxes[delete_idx]                   # 박스 info 제거

        for idx in orders :                     # 제거된 박스 위치 위에 박스가 있으면
            box = boxes[idx]                    # 해당 박스일 시 
            clear_box(maps, box)                # 해당 박스 위치를 0으로 바꾸고
            box_move(maps, box, N)              # 박스를 옮긴다. (중력에 의한)

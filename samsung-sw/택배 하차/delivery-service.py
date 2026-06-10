# ====================
import heapq

# 박스 객체 생성
class Box :
    def __init__(self, idx, h, w, c):
        self.idx = idx  
        self.h = h
        self.w = w
        self.c = c
        self.sr = 0 # start row
        self.sc = c # start column

        self.rcs = []
        for r in range(h) :
            for c in range(w) :
                self.rcs.append([r, c])

def clear_box(maps: list[list[int]], block: Box) :
    for r in range(block.sr, block.sr + block.h) :
        for c in range(block.sc, block.sc + block.w) :
            maps[r][c] = 0

def draw_box(maps:list[list[int]], block: Box) :
    for r, c in block.rcs :
        nr, nc = block.sr + r, block.sc + c
        maps[nr][nc] = block.idx

# 택배가 중력에 영향을 받는 함수.
def box_move(maps:list[list[int]], block:Box, N: int) :
    movable = True

    for sr in range(block.sr, N + 1) :
        for r, c in block.rcs :
            nr, nc = sr + r, block.sc + c
            if maps[nr][nc] != 0 :
                movable = False
                break

        if movable :
            block.sr = sr
            continue
        else :
            break

    draw_box(maps, block)

def is_left_zero(maps: list[list[int]], box : Box, N: int) -> bool :
    for r in range(box.sr, box.sr + box.h) :
        if sum(maps[r][1:box.c]) == 0 :
            continue
        else :
            return False
        
    return True

def is_right_zero(maps: list[list[int]], box : Box, N: int) -> bool :
    for r in range(box.sr, box.sr + box.h) :
        local_begin = box.c + box.w
        local_length = (N + 1)

        if sum(maps[r][local_begin : local_length]) == 0 :
            continue
        else :
            return False
        
    return True


if __name__ == "__main__" :
    N, M = map(int, input().split())
    maps = []
    
    for _ in range(N) :
        maps.append([-1] + [0]*N + [-1])
    maps.append([-1] * (N+2))
    boxes = {}
    orders = []

    for _ in range(M) :
        box_idx, h, w, c = map(int, input().split())
        boxes[box_idx] = Box(box_idx, h, w, c)
        box_move(maps, boxes[box_idx], N)
        orders.append(box_idx)

    left_right = True

    while len(boxes) > 0 :
        candidates = []
        # 택배 하차 (좌측)
        if left_right :
            left_right = False

            for key in orders :
                if is_left_zero(maps, boxes[key], N) :
                    # candidates.append(key)
                    heapq.heappush(candidates, key)

        else :
            left_right = True

            for key in orders :
                if is_right_zero(maps, boxes[key], N) :
                    # candidates.append(key)
                    heapq.heappush(candidates, key)

        # candidates.sort()
        # delete_idx = cadidates[0]
        delete_idx = heapq.heappop(candidates)
        print(delete_idx)
        clear_box(maps, boxes[delete_idx])
        orders.remove(delete_idx)

        del boxes[delete_idx]

        for idx in orders :
            box = boxes[idx]
            clear_box(maps, box)
            box_move(maps, box, N)
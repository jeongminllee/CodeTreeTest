H_MAX = 1_000_000

class SegmentTree :
    def __init__(self, max_size):
        # base : max_size 이상인 2의 거듭제곱
        self.base = 1
        while self.base < max_size :
            self.base *= 2

        self.tree = [(0, 0) for _ in range(self.base * 2)]

    def get(self, left ,right) :
        """
        구간 [left, right]의 (최대 dp, 그 dp를 만든 최대 높이) 반환
        내부적으로 리프 인덱스는 base를 더해 접근합니다
        """
        res = (0, 0)
        left += self.base
        right += self.base

        while left <= right :
            if left % 2 :
                res = max(res, self.tree[left])
                left = (left + 1) // 2
            else :
                left //= 2

            if right % 2 :
                right //= 2
            else :
                res = max(res, self.tree[right])
                right = (right - 1) // 2

        return res

    def update(self, idx, value) :
        ti = idx + self.base
        self.tree[ti] = (value, idx)

        while (ti := ti // 2) > 0 :
            self.tree[ti] = max(self.tree[ti * 2], self.tree[ti * 2 + 1])

def add_func(h) :
    dp, _ = seg.get(0, h - 1)
    dp += 1
    A.append(h)
    dp_idx.append(dp)
    dp_val[h].append(dp)
    seg.update(h, dp)

def remove_func() :
    h = A.pop()
    dp_idx.pop()
    dp_val[h].pop()
    dp = 0

    if dp_val[h] :
        dp = dp_val[h][-1]
    seg.update(h, dp)

def get_score(m_idx) :
    dp, idx = seg.get(0, H_MAX)
    return (dp_idx[m_idx] + dp - 1) * int(1e6) + idx

if __name__ == "__main__" :
    Q = int(input())    # 쿼리

    A = []  # 현재 지도
    dp_idx = [] # 위치별 "그 위치 산으로 끝나는 LIS 길이"
    dp_val = [[] for _ in range(H_MAX + 1)] # 높이별 dp 히스토리 스택
    seg = SegmentTree(H_MAX + 1)        # 인덱스 = 높이, [0...H_MAX] 사용


    for _ in range(Q) :
        query = list(map(int, input().split()))
        cmd = query[0]

        if cmd == 100 :
            _, n, *mount = query
            for h in mount :
                add_func(h)
            
        elif cmd == 200 :
            _, v = query
            add_func(v)

        elif cmd == 300 :
            remove_func()

        elif cmd == 400 :
            _, v = query
            print(get_score(v - 1))
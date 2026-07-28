h_max = 10**6

class SegmentTree :
    def __init__(self, max_size):
        self.base = 1
        while self.base < max_size :
            self.base <<= 1

        self.tree = [(0, 0) for _ in range(self.base << 1)]

    def get(self, left, right) :
        res = (0, 0)
        left += self.base
        right += self.base

        while left <= right :
            if left & 1 :
                res = max(res, self.tree[left])
                left = (left + 1) >> 1
            else :
                left >>= 1

            if right & 1 :
                right >>= 1
            else :
                res = max(res, self.tree[right])
                right = (right - 1) >> 1

        return res
    
    def update(self, idx, value) :
        ti = idx + self.base
        self.tree[ti] = (value, idx)

        while (ti := ti >> 1) > 0 :
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
    dp, idx = seg.get(0, h_max)
    return (dp_idx[m_idx] + dp - 1) * 10 ** 6 + idx

A = []
dp_idx = []
dp_val = [[] for _ in range(h_max + 1)]
seg = SegmentTree(h_max + 1)

if __name__ == "__main__" :
    Q = int(input())
    for _ in range(Q) :
        query = list(map(int, input().split()))
        cmd, *v = query

        if cmd == 100 :
            n, *mountain = v
            for h in mountain :
                add_func(h)

        elif cmd == 200 :
            add_func(v[0])

        elif cmd == 300 :
            remove_func() 

        elif cmd == 400 :
            print(get_score(v[0] - 1))
MAX = 1_000_000


class Tree : 
    def __init__(self, size):
        self.base = 1
        while self.base < size :
            self.base <<= 1

        self.tree = [(0, 0)] * (self.base * 2)

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

    def update(self, idx, val) :
        ti = idx + self.base
        self.tree[ti] = (val, idx)

        while (ti := ti>>1) > 0 :
            self.tree[ti] = max(self.tree[ti * 2], self.tree[ti * 2 + 1])
        # while ti > 0 :
        #     ti >>= 1
        #     self.tree[ti] = max(self.tree[ti * 2], self.tree[ti * 2 + 1])

def add_func(h) :
    dp, _ = tree.get(0, h-1)
    dp += 1
    A.append(h)
    dp_idx.append(dp)
    dp_val[h].append(dp)
    tree.update(h, dp)

def remove_func() :
    h = A.pop()
    dp_idx.pop()
    dp_val[h].pop()
    dp = 0

    if dp_val[h] :
        dp = dp_val[h][-1]

    tree.update(h, dp)

def get_score(m_idx) :
    dp, idx = tree.get(0, MAX)
    return (dp_idx[m_idx] + dp - 1) * 10**6 + idx


if __name__ == '__main__' :
    Q = int(input())
    A = []
    dp_idx = []
    dp_val = [[] for _ in range(MAX + 1)]
    tree = Tree(MAX + 1)

    for _ in range(Q) :
        query = list(map(int, input().split()))
        cmd = query[0]

        if cmd == 100 :
            _, n, *lst = query
            for h in lst :
                add_func(h)

        elif cmd == 200 :
            _, h = query
            add_func(h)

        elif cmd == 300 :
            remove_func()

        elif cmd == 400 :
            _, m_idx = query
            res = get_score(m_idx - 1)
            print(res)
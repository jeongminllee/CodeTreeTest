MAX_HEIGHT = 1_000_000

class SegmentTree :
    def __init__(self, max_size) :
        # base : max_size 이상인 2의 거듭제곱
        self.base = 1
        while self.base < max_size :
            self.base <<= 1

        # 트리 노드는 (value, idx) 형태로 저장
        # - value : 구간의 최대 dp
        # - idx : 그 최대 dp를 만든 '가장 큰 높이'
        # 파이썬의 튜플 비교는 (value, idx) 의 순서대로 진행하기 떄문에
        # tie-break 규칙을 자연스럽게 만족
        self.tree = [(0, 0) for _ in range(self.base << 1)]

    def get(self, left, right) :
        """
        구간 [left, right]의 (최대 dp, 그 dp를 만든 최대 높이) 반환
        내부적으로 리프 인덱스는 base를 더해 접근
        """
        res = (0, 0)
        left += self.base
        right += self.base

        # left가 홀수면 현재 노드를 포함하고 부모로 이동
        # right가 짝수면 현재 노드를 포함하고 부모로 이동
        # 아니라면 부모로만 이동
        while left <= right :
            if left & 1 :
                res = max(res, self.tree[left]) # 튜플 비교로 최대값/높이 선택
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
        """
        리프 idx 값을 (value, idx)로 설정한 뒤, 위로 올라가며 부모 값 갱신
        - value = 0 이면 (0, idx)보다 (0, 0)이 더 작지 않으므로, 
          같은 높이의 '현재 최대 dp'를 정확히 반영하려면
          idx 대신 0을 써주는 구현도 가능하지만,
          이 코드에서는 질의 결합에서 항상 더 큰 (value, idx)가 남으므로 문제 없음.
        """
        ti = idx + self.base
        self.tree[ti] = (value, idx)

        # 바다코끼리(윌러스) 연산자 (:=) 를 사용한 상향 갱신
        while (ti := ti >> 1) > 0 :
            # 왼/오 자식의 최대 튜플을 그대로 취함 
            self.tree[ti] = max(self.tree[ti * 2], self.tree[ti * 2 + 1])

def add_func(h) :
    """
    오른쪽 끝에 높이 h 추가
    - dp = 1 + max(D[0..h-1])   (세그트리 질의)
    - 위치/높이별 구조 갱신
    - 세그트리에 높이 h의 '현재 최대 dp' 반영
    """
    dp, _ = seg.get(0, h - 1)   # (최대 dp, idx) 중 dp만 사용
    dp += 1
    A.append(h)
    D_by_idx.append(dp)
    D_by_value[h].append(dp)
    seg.update(h, dp)

def remove_func() :
    """
    오른쪽 끝 산을 제거
    - 해당 높이으이 dp 히스토리 pop
    - 세그트리에는 그 높이의 새 top(없으면 0)을 반영
    """
    h = A.pop()
    D_by_idx.pop()
    D_by_value[h].pop()
    dp = 0
    if D_by_value[h] :
        dp = D_by_value[h][-1]  # 해당 높이의 '현재 최대 dp'
    seg.update(h, dp)

def get_score(m_idx) :
    """
    등산 시뮬레이션 점수 계산
    - L1 = m_idx 위치에서 끝나는 LIS 길이
    - (L2, H_best) = 세그트리의 전체 최대 (dp, 높이)
    - 점수 = (L1 + L2 - 1) * 1e6 + H_best
    """
    dp, idx = seg.get(0, MAX_HEIGHT)
    return (D_by_idx[m_idx] + dp - 1) * 1_000_000 + idx

if __name__ == "__main__" :
    A = []  # 현재 지도 높이 배열
    D_by_idx = []   # 위치별 "그 위치 산으로 끝나는 LIS 길이"
    D_by_value = [[] for _ in range(MAX_HEIGHT + 1)]    # 높이별 dp 히스토리 스텍
    seg = SegmentTree(MAX_HEIGHT + 1)   # 인덱스 = 높이, [0..MAX_HEIGHT]사용

    Q = int(input())

    for _ in range(Q) :
        cmd, *v = map(int, input().split())

        if cmd == 100 :
            n, *H = v
            for h in H :
                add_func(h)

        elif cmd == 200 :
            add_func(v[0])
        
        elif cmd == 300 :
            remove_func() 

        else :
            print(get_score(v[0] - 1))
"""
등산가의 이동조건
- 오른쪽으로만 이동 가능
- 등산으로는 더 높은 산으로만 이동 가능

케이블 카
- 특정 산에서만 탈 수 있음
- 현재 위치를 포함한 임의의 산을로 이동 가능. 높낮이 상관 X
- 케이블카를 탄 이후에도 등산을 이어가며 이 또한 오른쪽에 위치한 더 높은 산으로만 이동 가능

등산 시뮬레이션
- 현재위치보다 오른쪽에 위치한 산으로 오르막 이동에 성공할 때 마다 1_000_000 점 획득
- 케이블 카를 탈 수 있는 산에 도착해서, 케이블 카를 이용한다면 1_000_000 점 획득
- 케이블 카 이용 후 다시 등산에 성공하면 1_000_000점 획득
- 최종적으로 위치한 산의 높이만큼 점수 획득.

명령
- 빅뱅 : 100 n h1 h2 ... hn 
- 우공이산 : 200 h = 지도에 존재하는 기존 산들 오른쪽 끝에 높이 h 를 갖는 산 1개 추가
- 지진 : 300 = 지도에 존재하는 산 중 가장 오른쪽 위치의 산 제거
- 등산 시뮬레이션 : 400 m_idx = 케이블 카를 이용할 수 있는 산이 왼쪽에서 m_idx 번째 산이라고 가정했을 때, 
    등산 시뮬레이션 중 얻을 수 있는 최대 점수를 출력
"""
# 전역 변수 설정
MAX_HEIGHT = 1_000_000
TREE_SIZE = 4 * MAX_HEIGHT + 5

tree = [0] * TREE_SIZE
seg_index = [0] * TREE_SIZE
dpBuckets = [[] for _ in range(MAX_HEIGHT + 1)]

# 현재 지도 상태를 저장하는 리스트
mountainHeights = []
mountainDP = []

# 세그멘트 트리 업데이트
def updateSegmentTree(node, left, right, height, dpValue) :
    if height < left or height > right :
        return

    if left == right :
        tree[node] = dpValue
        seg_index[node] = height
        return

    mid = (left + right) // 2
    updateSegmentTree(node * 2, left, mid, height, dpValue)
    updateSegmentTree(node * 2 + 1, mid + 1, right, height, dpValue)

    if tree[node*2] <= tree[node*2+1] :
        tree[node] = tree[node*2+1]
        seg_index[node] = seg_index[node*2+1]
    else :
        tree[node] = tree[node*2]
        seg_index[node] = seg_index[node*2]

# 세그멘트 트리 쿼리 함수 (최대 DP 값 구하기)
def querySegmentTree(node, left, right, start, end) :
    if left > end or right < start :
        return 0

    if start <= left and end >= right :
        return tree[node]

    mid = (left + right) // 2
    leftQuery = querySegmentTree(node * 2, left, mid, start, end) 
    rightQuery = querySegmentTree(node * 2 + 1, mid + 1, right, start ,end)

    return max(leftQuery, rightQuery)

# 초기 트리 생성 함수
def tree_init(n:int, heights:list[int]) -> None :
    for h in range(1, MAX_HEIGHT + 1) :
        dpBuckets[h].append(0)

    for height in heights :
        maxPrevDP = querySegmentTree(1, 1, MAX_HEIGHT, 1, height - 1)
        dpValue = maxPrevDP + 1

        dpBuckets[height].append(dpValue)
        mountainHeights.append(height)
        mountainDP.append(dpValue)
        updateSegmentTree(1, 1, MAX_HEIGHT, height, dpValue)

# 가장 오른쪽에 산 하나 추가 
def add_tree(height) :
    maxPrevDP = querySegmentTree(1, 1, MAX_HEIGHT, 1, height - 1)
    dpValue = maxPrevDP + 1

    dpBuckets[height].append(dpValue)
    mountainHeights.append(height)
    mountainDP.append(dpValue)

    updateSegmentTree(1, 1, MAX_HEIGHT, height, dpValue)

# 가장 오른쪽 산 제거
def pop_tree() :
    height = mountainHeights.pop()
    mountainDP.pop()
    dpBuckets[height].pop()
    newDpValue = dpBuckets[height][-1]
    updateSegmentTree(1, 1, MAX_HEIGHT, height, newDpValue)

def simulate_hiking(m_idx) :
    beforeCableCarDP = mountainDP[m_idx-1] - 1
    afterCableCarDP = tree[1]
    highestMountain = seg_index[1]

    score = (beforeCableCarDP + afterCableCarDP) * 1_000_000 + highestMountain
    print(score)

if __name__ == "__main__" :

    Q = int(input())
    for _ in range(Q) :
        query = list(map(int, input().split()))
        cmd = query[0]

        if cmd == 100 : # 초기값 입력
            _, n, *lst = query 
            tree_init(n, lst)

        elif cmd == 200 :   # 산 1개 추가
            _, h = query
            add_tree(h)

        elif cmd == 300 :   # 산 1개 삭제
            pop_tree()

        else :  # cmd == 400 # 실행
            _, m_idx = query
            simulate_hiking(m_idx)
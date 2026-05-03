# 마을의 거리 : 1 ~ N
# 소비 전력 r => 가로등은 [x-r, x+r] 만큼 거리를 밝힘
# cmd == 100 : 마을 상태 확인
    # N : 거리의 크기
    # M : 초기에 존재하는 가로등 개수
    # L1, L2, ... Lm : 초기에 존재하는 가로등의 위치 정보(1,2,3... 은 고유 번호)

# cmd == 200 : 가로등 추가
    # M+1, M+2, ... 순서대로 채워짐.
    # 인접한 가로등 사이의 거리가 가장 먼 곳의 가운데에 새로운 가로등 설치
    # 만약 거리가 같은 거리가 여러 개라면 좌표값이 가장 작은 가로등 쌍을 선택함.
    # 가운데는 (Li + Lj) // 2를 의미하는듯? => 저 표시가 올림 표시라 처리는 (Li + Lj + 1) // 2 하면 될듯

# cmd == 300 : 가로등 제거
    # D번 가로등 제거

# cmd == 400 : 최적 위치 계산
    # 마을 거리 [1, N]을 전부 밝힐 수 있는 최소 소비 전력 r 을 계산.
# 최소 소비 전력 r의 2를 곱해 출력하는 프로그램을 작성
# ====================================================
from typing import Optional
import heapq
# 전역변수
N, M = None, None   # 초기 값
lamp_pos = []       # idx : 램프 ID, val : 램프 위치

left_lamp = []      # idx : 램프 ID, val : 왼쪽의 램프 ID     왼쪽으로 바라보는 링크드 리스트
right_lamp = []     # idx : 램프 ID, val : 오른쪽의 램프 ID    오른쪽으로 바라보는 링크드 리스트

left_heap = []      # idx : 램프 ID, val : 좌표값이 작은 순으로 정렬
right_heap = []     # idx : 램프 ID, val : 좌표값이 큰 순으로 정렬(음수)
distance_heap = []  # Road 담을거   (거리가 큰 순으로 정렬, 음수)


class Road :
    def __init__(self,
                 left_id:int,
                 right_id:int,
                 length:int,
                 st_pos:int):
        """
        left_id:왼쪽 가로등\n
        right_id:오른쪽 가로등\n
        length:거리\n
        st_pos:시작 위치\n
        """
        self.left_id = left_id
        self.right_id = right_id
        self.length = length
        self.st_pos = st_pos

    def __lt__(self, other):
        """
        lt = less than 비교 연산자
        """
        if self.length == other.length :
            return self.st_pos < other.st_pos
        return self.length > other.length
    
def get_max_distance() :
    max_distance : Optional[Road] = None    # 가장 긴 거리를 가지고 있는 애를 여기에 담아 return
    
    while distance_heap :
        road = distance_heap[0]
        if lamp_pos[road.left_id] == road.st_pos and \
            lamp_pos[road.right_id] == road.length + road.st_pos :
            max_distance = road
            break

        heapq.heappop(distance_heap)

    return max_distance



Q = int(input())
for _ in range(Q) :
    query = list(map(int, input().split()))
    cmd = query[0]

    if cmd == 100 :
        _, N, M, *lamp_pos = query
        lamp_pos = [-1] + lamp_pos

        # 좌우를 빠르게 살피기 위해서는 링크드 리스트를 써야 할거 같음.
        left_lamp = [-1] + [-1] + [idx for idx in range(1, M)]
        right_lamp = [-1] + [idx + 1 for idx in range(1, M)] + [-1]

        # 거리도 담아야 되는데, 거리를 담을 힙도 필요.
        for idx in range(1, len(lamp_pos)) :
            heapq.heappush(left_heap, (lamp_pos[idx], idx))     # 왼쪽 힙
            heapq.heappush(right_heap, (-lamp_pos[idx], idx))   # 오른쪽 힙

            if idx > 1 :    # 왼쪽 기준 1부터 시작. 가로등 M 에서 끊김.
                heapq.heappush(distance_heap,                   # 거리
                               Road(left_id=idx-1,
                                    right_id=idx,
                                    length=lamp_pos[idx] - lamp_pos[idx-1],
                                    st_pos=lamp_pos[idx-1]))
        
    elif cmd == 200 :
        # 두 가로등 사이 거리가 가장 먼 곳을 찾자.
        max_distance = get_max_distance() 
        heapq.heappop(distance_heap)

        left_id = max_distance.left_id
        right_id = max_distance.right_id
        length = max_distance.length
        st_pos = max_distance.st_pos

        # 새로운 좌표를 구해야 함.
        # (left_pos + right_pos + 1) // 2 로 하면 되지 않을까?
        new_lamp_id = len(lamp_pos)
        new_lamp_pos = st_pos + (length + 1) // 2
        lamp_pos.append(new_lamp_pos)

        # left, right lamp 에도 넣어줍시다.
        left_lamp[right_id] = new_lamp_id
        right_lamp[left_id] = new_lamp_id

        left_lamp.append(left_id)
        right_lamp.append(right_id)
        # 왼쪽 오른쪽 힙에도 넣어주자. 넣어주는건 좋은데 기존에 있는것들 중에 바꿔야 되는거 있지 않나?
        # 10 90 사이 50에 들어간다 치자. 그러면 10 50 50 90 으로 나뉠텐데. 이걸 우째 넣을까
        heapq.heappush(left_heap, (new_lamp_pos, new_lamp_id))
        heapq.heappush(right_heap, (-new_lamp_pos, new_lamp_id))

        # distance 힙에도 넣어줄껀데 
        # 왼쪽
        heapq.heappush(distance_heap, 
                       Road(left_id=left_id,
                            right_id=new_lamp_id,
                            length= new_lamp_pos - lamp_pos[left_id],
                            st_pos=lamp_pos[left_id]))
        
        # 오른쪽
        heapq.heappush(distance_heap, 
                       Road(left_id=new_lamp_id,
                            right_id=right_id,
                            length= lamp_pos[right_id] - new_lamp_pos,
                            st_pos=new_lamp_pos))


    elif cmd == 300 :
        cmd, D = query
        lamp_pos[D] = -1            # 가로등 삭제
        left_id = left_lamp[D]      # 삭제된 가로등 왼쪽 링크
        right_id = right_lamp[D]    # 삭제된 가로등 오른쪽 링크

        if left_id != -1 :          # 벽이 아니라면
            right_lamp[left_id] = right_id
        if right_id != -1 :         # 벽이 아니라면
            left_lamp[right_id] = left_id

        if left_id != -1 and right_id != -1 :   # 새로운 가로등 사이 거리 추가.
            heapq.heappush(distance_heap, Road(left_id=left_id,
                                            right_id=right_id,
                                            length=lamp_pos[right_id] - lamp_pos[left_id],
                                            st_pos=lamp_pos[left_id]))
        
    elif cmd == 400 :
        min_pos = 0
        max_pos = N + 1

        while left_heap :           # 삭제 되지 않은 가장 왼쪽 가로등 찾기 
            pos, id = left_heap[0]
            if lamp_pos[id] == pos :
                min_pos = pos
                break

            heapq.heappop(left_heap)
        
        while right_heap :          # 삭제 되지 않은 가장 오른쪽 가로등 찾기
            pos, id = right_heap[0]
            if lamp_pos[id] == -pos :
                max_pos = -pos
                break

            heapq.heappop(right_heap)

        max_distance = get_max_distance()   # 두 가로등 사이 가장 긴 거리 찾기
        mx_r = max(2 * (min_pos - 1), 2 * (N - max_pos), max_distance.length)
        print(mx_r)
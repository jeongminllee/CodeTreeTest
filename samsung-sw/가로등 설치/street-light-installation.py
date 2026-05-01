"""
1. 거리의 시작점 밝히기 : 가장 왼쪽에 있는 가로등이 1번 위치까지 밝혀야 함. 즉, L_min - r <= 1
r >= L_min - 1
2. 거리의 끝점 밝히기 : 가장 오른쪽에 있는 가로등이 N번 위치까지 밝혀야 함. L_max + r >= N
r >= N - L_max
3. 가로등 사이의 빈틈 채우기 : 인접한 두 가로등 L_i, L_j 사이의 모든 공간이 밝혀져야 함. 왼쪽가로등은 
L_i + r, 오른쪽 가로등은 L_j - r 까지 밝힐 수 있음. L_i + r >= L_j - r
2r >= L_j - L_i를 의미함. => r >= max(L_j - L_i) / 2 를 의미.
r = max(2 * (L_min - 1), 2 * (N - L_max), max_dist)값을 찾아야 함.

2. 어떻게 이 값들을 빠르게 찾을 것인가?
'최대/최소'값을 반복적으로 찾아야 하는 문제에서는 우선순위 큐(힙)가 가장 효과적인 자료구조
- 인접 가로등 간 최대 거리 : 두 가로등 사이의 거리를 '도로'라고 생각하고, 이 도로들을 최대 힙에 저장하면,
인접한 가로등 간 최대 거리를 빠르게 찾을 수 있습니다.
- 가장 왼쪽/오른쪽 가로등 위치: 가로등 위치들을 각각 최소힙과 최대힙에 저장하면, 각 힙의 최상단에서
가장 왼쪽, 가장 오른쪽 가로등의 위치를 빠르게 찾을 수 있습니다.

3. 가로등 추가/제거는?
- 가로등 추가 : 가장 긴 도로의 중간에 새 가로등을 설치. 이는 최대 힙에서 가장 긴 도로를 꺼내고,
그 도로를 두 개의 짧은 도로로 나누어 다시 힙에 넣는 과정으로 구현 가능
- 가로등 제거 : 특정 가로등을 제거하면, 그 가로등을 기준으로 양쪽에 있던 두개의 도로가 사라지고, 
대신 두 도로가 합쳐진 하나의 더 긴 도로가 생김. 이를 위해서 제거될 가로등의 양옆(이전,다음) 가로등이 
무엇인지 알아야 함. 이 정보는 이중 연결 리스트와 유사한 방식으로, 각 가로등의 prev, next 정보를 
배열에 저장하여 효율적으로 관리할 수 있음.
"""

import heapq

# 가로등 정보
lamp_pos = None       # idx : 각 가로등의 ID, val: 위치
prev_lamp_id = None   # idx : 각 가로등의 ID, val: 이전 가로등
next_lamp_id = None   # idx : 각 가로등의 ID, val: 다음 가로등

# 거리 관리
roads = []          # 최대 힙, 두 가로등 사이의 거리가 가장 긴 도로

class Road :
    def __init__(self, 
    left_lamp_id: int, 
    right_lamp_id: int, 
    length: int, 
    st_pos: int) :
        """
        left_lamp_id: 도로의 왼쪽 가로등 ID
        right_lamp_id: 도로의 오른쪽 가로등 ID
        length: 도로의 길이
        st_pos: 도로의 시작 위치(왼쪽 가로등 위치)
        """
        self.left_lamp_id = left_lamp_id
        self.right_lamp_id = right_lamp_id
        self.length = length
        self.st_pos = st_pos

    # 최대힙으로 사용하기 위한 비교 연산자 정의
    def __lt__(self, other) :
        # 길이가 같으면 시작 위치가 작은 도로를 우선
        if self.length == other.length :
            return self.st_pos < other.st_pos
        # 길이가 긴 도로를 우선
        return self.length > other.length

# 양 끝 가로등 위치 관리
lamp_pos_min_heap = []  # 최소힙, (pos, id) 튜플을 저장하여 위치가 가장 작은 가로등을 찾음
lamp_pos_max_heap = []  # 최대힙, (-pos, id) 튜플을 저장하여 위치가 가장 큰 가로등을 찾음

N, M = None, None

# lazy deletion을 적용하여 가장 오른쪽에 있는 유효한 가로등 위치를 찾는 함수
def get_max_pos_lamp() :
    while lamp_pos_max_heap :
        neg_pos, lamp_id = lamp_pos_max_heap[0]
        # 힙에서 꺼낸 위치가 현재 lamp_pos에 저장된 실제 위치와 일치하는지 확인
        # 일치하지 않으면, 이미 제거된 가로등의 오래된 정보이므로 힙에서 제거
        if lamp_pos[lamp_id] == -neg_pos :
            break
        heapq.heappop(lamp_pos_max_heap)
    return -lamp_pos_max_heap[0][0]

# lazy deletion을 적용하여 가장 왼쪽에 있는 유효한 가로등 위치 찾는 함수
def get_min_pos_lamp() :
    while lamp_pos_min_heap :
        pos, lamp_id = lamp_pos_min_heap[0]
        # 힙에서 꺼낸 위치가 현재 lamp_pos에 저장된 실제 위치와 일치하는지 확인
        if lamp_pos[lamp_id] == pos :
            break
        heapq.heappop(lamp_pos_min_heap)
    return lamp_pos_min_heap[0][0]

# lazy deletion을 적용하여 가장 긴 유효한 도로를 찾는 함수
def get_max_road() :
    while roads :
        road = roads[0]
        left_lamp_id = road.left_lamp_id
        right_lamp_id = road.right_lamp_id
        length = road.length
        st_pos = road.st_pos

        # 힙에서 꺼낸 도로 정보가 현재 가로등 위치와 일치하는지 확인
        # 즉, 이 도로를 구성하는 두 가로등이 여전히 인접해 있는지 검사
        if lamp_pos[left_lamp_id] == st_pos and\
        lamp_pos[right_lamp_id] == st_pos + length :
            break
        heapq.heappop(roads)

    return roads[0]

# 메인
Q = int(input())
for _ in range(Q) :
    query = list(map(int, input().split()))
    cmd = query[0]

    if cmd == 100 : # 마을 상태 확인(초기화)
        _, N, M, *lamp_pos = query

        # 가로등 위치 및 연결 리스트 정보 초기화
        lamp_pos = [-1] + lamp_pos
        next_lamp_id = [-1] + [i+1 for i in range(1, M)] + [-1]
        prev_lamp_id = [-1] + [-1] + [i-1 for i in range(2, M+1)]

        # 초기 가로등 정보를 각 힙에 추가
        for i in range(1, M+1) :
            pos = lamp_pos[i]
            heapq.heappush(lamp_pos_min_heap, (pos, i))
            heapq.heappush(lamp_pos_max_heap, (-pos, i))

            # 인접한 가로등 사이의 도로 정보를 roads 힙에 추가
            if i > 1 :
                length = pos - lamp_pos[i-1]
                heapq.heappush(roads, Road(i-1, i, length, lamp_pos[i-1]))
    
    elif cmd == 200 :   # 가로등 추가
        # 가장 긴 도로를 찾아 그 중간에 가로등 추가
        road = get_max_road()
        heapq.heappop(roads)

        # 새 가로등 위치 계산 (중간, 올림 처리)
        new_pos = road.st_pos + (road.length + 1) // 2
        new_lamp_id = len(lamp_pos)

        # 이중 연결 리스트 정보 갱신
        next_lamp_id[road.left_lamp_id] = new_lamp_id
        prev_lamp_id[road.right_lamp_id] = new_lamp_id
        next_lamp_id.append(road.right_lamp_id)
        prev_lamp_id.append(road.left_lamp_id)

        # 새 가로등 정보를 자료구조에 추가
        lamp_pos.append(new_pos)
        heapq.heappush(lamp_pos_min_heap, (new_pos, new_lamp_id))
        heapq.heappush(lamp_pos_max_heap, (-new_pos, new_lamp_id))

        # 기존 도로가 2개의 새로운 도로로 나뉘었으므로, roade 힙에 추가
        length1 = new_pos - road.st_pos
        length2 = road.st_pos + road.length - new_pos
        heapq.heappush(roads, Road(road.left_lamp_id, new_lamp_id, length1, road.st_pos))
        heapq.heappush(roads, Road(new_lamp_id, road.right_lamp_id, length2, new_pos))

    elif cmd == 300 :   # 가로등 제거
        target_id = query[1]
        # lamp_pos를 -1로 설정하여 제거되었음을 표시
        lamp_pos[target_id] = -1

        left_lamp_id = prev_lamp_id[target_id]
        right_lamp_id = next_lamp_id[target_id]

        # 이중 연결 리스트에서 제거된 가로등의 연결을 끊음
        if left_lamp_id != -1 :
            next_lamp_id[left_lamp_id] = right_lamp_id
        if right_lamp_id != -1 :
            prev_lamp_id[right_lamp_id] = left_lamp_id

        # 제거된 가로등의 양옆 가로등이 모두 존재하면, 두 가로등을 잇는 새로운 도로가 생김
        if left_lamp_id != -1 and right_lamp_id != -1 :
            length = lamp_pos[right_lamp_id] - lamp_pos[left_lamp_id]
            heapq.heappush(roads, Road(left_lamp_id, right_lamp_id, length, lamp_pos[left_lamp_id]))

    elif cmd == 400 :   # 최소 전력 계산
        # 각 힙에서 필요한 값들을 가져옴
        max_pos = get_max_pos_lamp()
        min_pos = get_min_pos_lamp()
        road = get_max_road()

        # 최소 전력 * 2 를 계산하여 출력
        # max(가장 왼쪽 빈 공간 * 2, 가장 오른쪽 빈 공간 * 2, 가장 긴 도로 길이)
        res = max(2 * (min_pos - 1), 2 * (N - max_pos), road.length)
        print(res)
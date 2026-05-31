import sys
# sys.stdin = open('input.txt', 'r')
from typing import *

# ====================
"""
공격 준비 : 100 N [ids, p, r] * N
    최초 1번, 선언된 선박들은 바로 사격 대기로 들어감
지원요청 : 200 id p r
    사격 대기열로 바로 추가
함포 교체 : 300 id pw
    함포 공격력을 pw로 갱신
공격 명령 : 400
    사격 대기 상태 중 공격력이 가장 높은 선박 최대 5척에 일제 사격 명령
    우선순위 : 공격력 => ID 작은순
    사격한 선박은 즉시 재장전 돌입, 사격 시간을 포함해 r 시간이 지나면 사격대기
각 명령은 1시간 단위, i 명령 후 1시간이 지나면 i+1 시간임.
"""


import heapq
from collections import deque

boat_info = {}  # 배 정보 {ids : [p, r]}
atk_queue = []  # 사격 대기열
reload = deque()     # 재장전 중인 포 [id, r]

def main() :
    T = int(input())
    for _ in range(T) :
        cmds = list(map(int, input().split()))
        if cmds[0] == 100 :                         # 초기 입력
            _, N, *boats = cmds                     # N척의 배, 배 정보들
            for idx in range(0, len(boats), 3) :    
                ids, p, r = boats[idx:idx+3]           
                boat_info[ids] = [p, r]         
                heapq.heappush(atk_queue, [-p, ids])    # 재장전이 된 포, 공격력이 높은순, ids가 낮은 순

        elif cmds[0] == 200 :                       # 지원 요청
            _, ids, p, r = cmds
            boat_info[ids] = [p, r]
            heapq.heappush(atk_queue, [-p, ids])

        elif cmds[0] == 300 :                       # 함포 교체
            _, ids, pw = cmds
            boat_info[ids][0] = pw                  # 함포 교체
            heapq.heappush(atk_queue, [-pw, ids])
            

        elif cmds[0] == 400 :
            cnt = 0
            atk_power = 0
            atk_boat = []

            while atk_queue and cnt < 5 :
                p, ids = heapq.heappop(atk_queue)
                if -p != boat_info[ids][0] :
                    continue
                atk_power += -p                     
                cnt += 1
                atk_boat.append(ids)
                reload.append([ids, boat_info[ids][1]])

            print(atk_power, len(atk_boat), *atk_boat)

        for _ in range(len(reload)) :
            ids, r = reload.popleft()
            p = boat_info[ids][0]
            r -= 1
            if r <= 0 :
                heapq.heappush(atk_queue, [-p, ids])
            else :
                reload.append([ids, r])


if __name__ == "__main__" :
    main()
    
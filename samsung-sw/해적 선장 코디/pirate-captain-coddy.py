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
boat_states = {} # 배 준비 상태 {ids : True or False}
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
                boat_states[ids] = True      
                heapq.heappush(atk_queue, [-p, ids])    # 재장전이 된 포, 공격력이 높은순, ids가 낮은 순
                
        elif cmds[0] == 200 :                       # 지원 요청
            _, ids, p, r = cmds
            boat_info[ids] = [p, r]                 # 지원 함대 정보 입력
            boat_states[ids] = True                 # 사격 대기 상태
            heapq.heappush(atk_queue, [-p, ids])    # 사격 대기열 기입

        elif cmds[0] == 300 :                       # 함포 교체
            _, ids, pw = cmds
            boat_info[ids][0] = pw                  # 함포 교체
            if boat_states[ids] == True :           # 사격 대기 상태면
                # 사격 대기열에 새로 입력 (발포 시 기존 입력값은 lazy deletion에 의해 제거됨.)
                heapq.heappush(atk_queue, [-pw, ids])   

        elif cmds[0] == 400 :
            atk_power = 0       # 공격력 총합
            atk_boat = []       # 공격한 함박 ids, 공격력 높은 순대로 기입됨.

            while atk_queue and len(atk_boat) < 5 :
                p, ids = heapq.heappop(atk_queue)   # 공격력이 높은 순, ids 가 낮은 순으로 heappop
                if -p != boat_info[ids][0] :        # 만약 변경 전 공격력이면 deletion
                    continue
                atk_power += -p                     # 공격력 더해줌
                atk_boat.append(ids)                # 공격 함박 수 + 1 (cnt 했었는데 길이로 처리해도 됨.)
                reload.append([ids, boat_info[ids][1]]) # 재장전 진입
                boat_states[ids] = False            # 현재 이 함박는 공격할 수 없음.

            print(atk_power, len(atk_boat), *atk_boat)  # 결과 값 print (데미지 총합, 공격한 함대 수, 공격한 함대 ids)

        for _ in range(len(reload)) :   # 명령을 시행한 후 시간 처리
            ids, r = reload.popleft()   # 앞쪽에 있는 애들을 꺼내옴
            r -= 1                      # 시간이 1시간 지났음을 의미
            if r <= 0 :                 # 재장전이 모두 종료되었으면
                heapq.heappush(atk_queue, [-boat_info[ids][0], ids])    # 현재 공격력, ids 를 공격 대기열로 입력
                boat_states[ids] = True     # 이 ids 함박은 공격 준비가 완료됨을 의미
            else :
                reload.append([ids, r])     # 장전 완료가 되지 않았으면 다시 입력.


if __name__ == "__main__" :
    main()
    
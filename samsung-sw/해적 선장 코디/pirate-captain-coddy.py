# ====
"""
사격 대기(힙) : 힙으로 해서 애들을 담는다. 정렬은 (-공격력, id) 순으로 해서
오리지널 : 주어진 대로 다 저장함 id, p, r 그대로 => {id:[p, r]} 로 저장?
선박 관리 : 재장전 시간에 맞춰서 어떻게 관리를 할 것인가, 여기는 for 문 돌면서 r - 1 씩 함.
    if r <= 0 이 되면 사격 대기 힙에 추가. 근데 이거 빨리 빼내려면 heappop 해야할듯?
사격 : 사격대기(힙)에 있는 선박 최대 5개만 선발하여 사격 (-공격력, id) 로 해서.
    그 다음에 재장전이 끝나는 애들을 다시 넣는다. 

"""
import heapq
from collections import deque

fire_wait = []          # 사격 대기
reload_wait = deque()   # 사격하고 여기서 대기할거임.
ori_boat = {}           # 선박 관리할 딕셔너리 {id:[p, r]}

def plus_boat(ids:int, p:int, r:int) :
    r"""
    ids : 선박 id
    p : 공격력
    r : 재장전 시간
    """
    heapq.heappush(fire_wait, [-p, ids])
    ori_boat[ids] = [p, r]


if __name__ == "__main__" :
    T = int(input())
    for t in range(T) : 
        query = list(map(int, input().split()))
        cmd = query[0]

        if cmd == 100 :
            # N : 선박 개수
            # lst(list[list[ids, p, r]]) : 고유 선박 번호, 공격력, 재장전 시간
            # 모두 [사격 대기]
            _, N, *lst = query
            for idx in range(0,len(lst),3) :
                ids, p, r = lst[idx:idx+3]
                plus_boat(ids, p, r)

        elif cmd == 200 :
            # ids, p, r 를 가지는 선박이 [사격 대기] 상태로 추가됨.
            _, ids, p, r = query
            plus_boat(ids, p, r)

        elif cmd == 300 : 
            # ids, pw : 선박의 함포를 교체 => 공격력 pw
            _, ids, pw = query
            ori_boat[ids][0] = pw
            heapq.heappush(fire_wait, [-pw, ids])
 
        elif cmd == 400 :
            # 총 피해량, 사격 선박 수, 사격한 선박들의 선박 번호를 공백으로 구분
            # 사격 대기인 선박 중 공격력 가장 높은 선박 최대 5척을 일제 사격 명령
            # 공격력이 같다면 선박 번호ids가 작은 선박을 우선 선택
            # 우선순위 : 사격 대기 > 공격력 > 선박 번호
            # 사격한 선박은 사격 시점을 포함해 r 시간 경과 후 다시 사격 대기 상태 
            total_attack = 0
            attack_ids = []
            cnt = 0
            while fire_wait and cnt < 5 :
                
                # 사격 실시
                now_fire = heapq.heappop(fire_wait)
                
                attack_p, attack_id = now_fire
                if attack_p == -ori_boat[attack_id][0] :
                    cnt += 1
                    total_attack += -attack_p
                    attack_ids.append(attack_id)

                # 사격 종료했을 때 자동으로 장전 장소로 이동
                    reload_wait.append([now_fire[1], ori_boat[now_fire[1]][0], ori_boat[now_fire[1]][1]])

            print(total_attack, len(attack_ids), *attack_ids)

        # 모든 명령이 끝난 후 사격 대기 리스트 재장전 시간 계산(0일시 사격대기로 이동)
        for idx in range(len(reload_wait)) :
            curr_boat = reload_wait.popleft()
            ids, p, r = curr_boat
            r -= 1
            
            if r <= 0 :
                heapq.heappush(fire_wait, [-p, ids])

            else :
                reload_wait.append([ids, p, r])

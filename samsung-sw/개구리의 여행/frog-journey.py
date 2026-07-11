"""
안전한 돌       : .
미끄러운 돌      :  S
천적이 사는 돌   : #

각 위치의 돌은 항상 안전한 돌이다. 

구상 : 

1. 점프
현재 위치에서 상하좌우 방향 중 하나를 골라 현재 점프력 만큼 칸을 이동
이거는 bfs로 해야되나? 근데 bfs 로 하는건 좋은데 아 그럼 ij 둘 다 증가 하는건 좀 견제해야겠네

2. 점프력 증가
점프력 증가를 언제 사용할 것인가. 
증가는 무조건 1만 가능.
1,2,3,4,5 까지만 점프력 증가 가능. 그러니까 1, 2, 3, 4 일때만 증가 가능

3. 점프력 감소
k 에서 1~(k-1) 까지 변화 가능
감소할 때는 1만큼의 시간이 소요됨.

=> 증가핳때는 2:4, 3:9, ... 제곱으로 되고
=> 감소할때는 무조건 1 
=> 점프 시 무조건 1

큐에 담을때 무조건 시간이 제일 짧은거 위주로 담아야겠네 => 힙을 쓴다? 아니면 계속 sort한다?

"""
import heapq 
INF = 1 << 32 
di = [-1, 1, 0, 0] 
dj = [0, 0, -1, 1] 
def is_valid(i, j) : 
    return 0 <= i < N and 0 <= j < N 
    
def dijkstra(si, sj, ei, ej) : 
    heap = [] 
    heapq.heappush(heap, (0, si, sj, 1)) # sec, si, sj, k 
    dist[si][sj][1] = 0 
    while heap : 
        sec, ci, cj, k = heapq.heappop(heap) 
        if (ci, cj) == (ei, ej) : 
            return min(dist[ei][ej]) 
            
        if dist[ci][cj][k] < sec : 
            continue
             
        if (ci, cj) == (si, sj) and k > 1 : 
            continue 
        
        dist[ci][cj][k] = sec 
        for d in range(4) : 
            flag = True 
            # 점프력 감소 
            
            for nk in range(1, k) : 
                cost = sec + 2 
                ni, nj = ci + di[d] * nk, cj + dj[d] * nk 
                
                if not is_valid(ni, nj) or maps[ni][nj] == '#' : 
                    flag = False 
                    break 
                    
                if maps[ni][nj] == '.' and dist[ni][nj][nk] > cost : 
                    dist[ni][nj][nk] = cost
                    heapq.heappush(heap,(cost, ni, nj, nk)) 
                    
            if flag == False : 
                continue 
                    
            # 점프 
            cost = sec + 1 
            ni, nj = ci + di[d] * k, cj + dj[d] * k 
            if not is_valid(ni, nj) or maps[ni][nj] == '#' : 
                flag = False 
                continue 
                
            if maps[ni][nj] == '.' and dist[ni][nj][k] > cost : 
                dist[ni][nj][k] = cost 
                heapq.heappush(heap,(cost, ni, nj, k)) 
                
            # 점프력 증가 
            if 0 < k < 5 : 
                if not flag : 
                    continue 
                    
                cost = sec + 1 
                for nk in range(k+1, 6) : 
                    cost += nk**2 
                    ni, nj = ci + di[d] * nk, cj + dj[d] * nk 
                    
                    if not is_valid(ni, nj) or maps[ni][nj] == '#' : 
                        break 
                        
                    if maps[ni][nj] == '.' and dist[ni][nj][nk] > cost : 
                        dist[ni][nj][nk] = cost 
                        heapq.heappush(heap,(cost, ni, nj, nk)) 
                        
    return min(dist[ei][ej]) 
    
N = int(input()) 
maps = [list(input()) for _ in range(N)] 
Q = int(input()) 
for _ in range(Q) : 
    query = list(map(int, input().split())) 
    for i in range(len(query)) : 
        query[i] -= 1 

    dist = [[[INF] * 6 for _ in range(N)] for _ in range(N)] 
        
    res = dijkstra(*query) 

    if res == INF : 
        print(-1) 
        
    else : 
        print(res)
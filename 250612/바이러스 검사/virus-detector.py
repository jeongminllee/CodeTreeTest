n = int(input())
customer = list(map(int, input().split()))
arr = list(map(int, input().split()))

'''
n : 식당의 수
customer : 각 식당에 있는 고객의 수
arr : [검사팀장이 검사할 수 있는 최대 고객의 수 / 검사팀원이 검사할 수 있는 최대 고객 수]
'''
res = [n, 0]    # 팀장 / 팀원
for i in range(n) :
    customer[i] -= arr[0]

for cus in customer :
    if cus <= 0 :
        break
    res[1] += cus // arr[1]

    if cus % arr[1] != 0 :
        res[1] += 1

print(sum(res))
K, N = map(int, input().split())

# Please write your code here.
def combine(nums, k) :
    visited = [0] * len(nums)
    res = []
    combinations(bgn=0, end=k, visited=visited, nums=nums, buildings=[], depth=0, res=res)

    return res

def combinations(bgn, end, visited, nums, buildings, depth, res) :
    if depth == end :
        res.append(buildings[:])
        return

    for idx in range(bgn, len(nums)) :
        combinations(0, end, visited, nums, buildings + [nums[idx]], depth+1, res)




nums = [i for i in range(1, K+1)]
res = combine(nums, N)
for ans in res :
    print(*ans)
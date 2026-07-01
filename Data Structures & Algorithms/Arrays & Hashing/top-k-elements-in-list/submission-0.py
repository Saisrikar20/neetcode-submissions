class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        n=set(nums)
        d={}
        l=[]
        f=0
        for i in n:
            d[str(i)]=nums.count(i)
        for i in range(k):
            max=0
            for k,v in d.items():
                if v>max and int(k) not in l:
                    max=v
                    f=int(k)
            l.append(f)
        return l

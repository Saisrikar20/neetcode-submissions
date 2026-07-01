class Solution:
    def hasDuplicate(self, nums: List[int]) -> bool:
        l=[]
        for i in nums:
            if i not in l:
                l.append(i)
            else:
                return True
        else:
            return False
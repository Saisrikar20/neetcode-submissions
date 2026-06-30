class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        result=[]
        for i in range(len(nums) - 2):
            if i > 0 and nums[i] == nums[i-1]:
                continue
            lo,hi=i+1,len(nums)-1
            while lo<hi:
                a=[nums[i],nums[lo],nums[hi]]
                if sum(a) == 0:
                    result.append(a)
                    lo += 1
                    hi -= 1
                    while lo < hi and nums[lo] == nums[lo - 1]:
                        lo += 1
                    while lo < hi and nums[hi] == nums[hi + 1]:
                        hi -= 1
                elif sum(a) > 0:
                    hi -= 1
                else:
                    lo += 1
        return result
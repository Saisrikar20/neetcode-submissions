class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        l=len(nums)
        pre=[]
        post=[]
        output=[]
        for i in range(l):
            if i==0:
                pre.append(1)
            else:
                pre.append(pre[i-1] * nums[i-1])
            
            y=1
            for j in range(i+1, l):
                y*=nums[j]
            post.append(y)
            output.append(pre[i]*post[i])
        return output
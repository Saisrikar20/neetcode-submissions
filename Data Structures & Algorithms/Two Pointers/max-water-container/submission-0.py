class Solution:
    def maxArea(self, heights: List[int]) -> int:
        area=0
        s,e=0,len(heights)-1
        while s<e:
            m=min(heights[s],heights[e])
            if area<m*(e-s):
                area=m*(e-s)
            if heights[s]==m:
                s+=1
            if heights[e]==m:
                e-=1
        return area

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        start,end = 0,0
        longestLen = 0
        charMap = {} #{char:position}
        while end<len(s):
            if s[end] in charMap and charMap[s[end]]>=start:
                start = charMap[s[end]]+1
            else:
                longestLen=max(longestLen, end-start+1)
            charMap[s[end]]=end
            end+=1
        return longestLen

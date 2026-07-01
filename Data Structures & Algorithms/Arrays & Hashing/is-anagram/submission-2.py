class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s)!=len(t):
            return False
        else:
            d={}
            for i in s:
                if i not in d.keys():
                    d[i]=1
                else:
                    d[i]+=1
            for i in t:
                if i not in d.keys() or d[i] == 0:
                    return False
                else:
                    d[i]-=1
            return True
            
        
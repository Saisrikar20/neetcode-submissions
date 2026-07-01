class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        l=[]
        l1=[]
        for word in strs:
            d={}
            for ch in word:
                if ch not in d:
                    d[ch]=1
                else:
                    d[ch]+=1
            if d not in l1:
                l1.append(d)
                l.append([word])
            else:
                idx=l1.index(d)
                l[idx].append(word)
        return l


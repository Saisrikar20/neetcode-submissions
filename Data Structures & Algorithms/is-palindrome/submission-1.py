class Solution:
    def isPalindrome(self, s: str) -> bool:
        f,r=0,len(s)-1
        while f<r:
            while f<r and not s[f].isalnum():
                f+=1
            while f<r and not s[r].isalnum():
                r-=1
            if s[f].lower()!=s[r].lower():
                return False
            f+=1
            r-=1
        return True
class Solution:
    def isValid(self, s: str) -> bool:
        stack = []

        for b in s:
            if b in "([{":
                stack.append(b)

            elif b in ")]}":
                if not stack:
                    return False

                x = stack.pop()

                if x == "(" and b != ")":
                    return False
                elif x == "[" and b != "]":
                    return False
                elif x == "{" and b != "}":
                    return False

        return len(stack) == 0
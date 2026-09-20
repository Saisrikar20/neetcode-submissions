#!/usr/bin/env python3
"""
update_readme.py
Automated tracker and catalog generator for NeetCode / Blind 75 practice.
Scans 'Data Structures & Algorithms/', indexes problems & all submission attempts,
computes progress metrics, dynamically updates README.md, and maintains SOLUTIONS.md.
"""

import os
import re
import urllib.parse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DSA_DIR = REPO_ROOT / "Data Structures & Algorithms"
README_PATH = REPO_ROOT / "README.md"
SOLUTIONS_PATH = REPO_ROOT / "SOLUTIONS.md"

LEETCODE_USERNAME = "saisrikar07"
LEETCODE_PROFILE_URL = f"https://leetcode.com/u/{LEETCODE_USERNAME}/"
GITHUB_USER = "Saisrikar20"
REPO_NAME = "neetcode-submissions"
REPO_URL = f"https://github.com/{GITHUB_USER}/{REPO_NAME}"
LINKEDIN_URL = "https://linkedin.com/in/sai-srikar-b-54b1b8359"

TARGET_BLIND75_TOTAL = 75

TOPIC_TARGETS = {
    "Arrays & Hashing": 9,
    "Two Pointers": 5,
    "Sliding Window": 6,
    "Stack": 7,
    "Binary Search": 7,
    "Linked List": 6,
    "Trees": 14,
    "Tries": 3,
    "Heap / Priority Queue": 3,
    "Backtracking": 2,
    "Graphs": 6,
    "Advanced Graphs": 1,
    "1-D DP": 8,
    "2-D DP": 2,
    "Greedy": 3,
    "Intervals": 6,
    "Math & Geometry": 2,
    "Bit Manipulation": 7,
}

TOPIC_ORDER = [
    "Arrays & Hashing",
    "Two Pointers",
    "Sliding Window",
    "Stack",
    "Binary Search",
    "Linked List",
    "Trees",
    "Tries",
    "Heap / Priority Queue",
    "Backtracking",
    "Graphs",
    "Advanced Graphs",
    "1-D DP",
    "2-D DP",
    "Greedy",
    "Intervals",
    "Math & Geometry",
    "Bit Manipulation",
]

DIFFICULTY_COLORS = {
    "Easy": "22C55E",
    "Medium": "F59E0B",
    "Hard": "EF4444",
}

DIFFICULTY_ICONS = {
    "Easy": "🟢",
    "Medium": "🟡",
    "Hard": "🔴",
}

# Rich problem database for NeetCode & Blind 75
PROBLEM_METADATA = {
    # Arrays & Hashing
    "duplicate-integer": {"id": 217, "title": "Contains Duplicate", "topic": "Arrays & Hashing", "difficulty": "Easy", "lc_slug": "contains-duplicate", "tags": "Hash Set, Lookup"},
    "is-anagram": {"id": 242, "title": "Valid Anagram", "topic": "Arrays & Hashing", "difficulty": "Easy", "lc_slug": "valid-anagram", "tags": "Hash Map, Frequency Count"},
    "two-integer-sum": {"id": 1, "title": "Two Sum", "topic": "Arrays & Hashing", "difficulty": "Easy", "lc_slug": "two-sum", "tags": "Hash Map, Complement Check"},
    "anagram-groups": {"id": 49, "title": "Group Anagrams", "topic": "Arrays & Hashing", "difficulty": "Medium", "lc_slug": "group-anagrams", "tags": "Hash Map, Frequency Tuple"},
    "top-k-elements-in-list": {"id": 347, "title": "Top K Frequent Elements", "topic": "Arrays & Hashing", "difficulty": "Medium", "lc_slug": "top-k-frequent-elements", "tags": "Bucket Sort, Min-Heap"},
    "products-of-array-discluding-self": {"id": 238, "title": "Product of Array Except Self", "topic": "Arrays & Hashing", "difficulty": "Medium", "lc_slug": "product-of-array-except-self", "tags": "Prefix & Suffix Products"},
    "string-encode-and-decode": {"id": 271, "title": "Encode and Decode Strings", "topic": "Arrays & Hashing", "difficulty": "Medium", "lc_slug": "encode-and-decode-strings", "tags": "Length Delimiter, Parsing"},
    "longest-consecutive-sequence": {"id": 128, "title": "Longest Consecutive Sequence", "topic": "Arrays & Hashing", "difficulty": "Medium", "lc_slug": "longest-consecutive-sequence", "tags": "Hash Set, Sequence Start"},
    "valid-sudoku": {"id": 36, "title": "Valid Sudoku", "topic": "Arrays & Hashing", "difficulty": "Medium", "lc_slug": "valid-sudoku", "tags": "Hash Set, Grid Coordinate Hashing"},

    # Two Pointers
    "is-palindrome": {"id": 125, "title": "Valid Palindrome", "topic": "Two Pointers", "difficulty": "Easy", "lc_slug": "valid-palindrome", "tags": "Two Pointers, String Cleansing"},
    "two-integer-sum-ii": {"id": 167, "title": "Two Sum II - Input Array Is Sorted", "topic": "Two Pointers", "difficulty": "Medium", "lc_slug": "two-sum-ii-input-array-is-sorted", "tags": "Two Pointers, Sorted Array Shrink"},
    "three-integer-sum": {"id": 15, "title": "3Sum", "topic": "Two Pointers", "difficulty": "Medium", "lc_slug": "3sum", "tags": "Two Pointers, Sorting, Duplicate Elimination"},
    "max-water-container": {"id": 11, "title": "Container With Most Water", "topic": "Two Pointers", "difficulty": "Medium", "lc_slug": "container-with-most-water", "tags": "Two Pointers, Greedy Height Boundary"},
    "trapping-rain-water": {"id": 42, "title": "Trapping Rain Water", "topic": "Two Pointers", "difficulty": "Hard", "lc_slug": "trapping-rain-water", "tags": "Two Pointers, Monotonic Boundary"},

    # Sliding Window
    "buy-and-sell-crypto": {"id": 121, "title": "Best Time to Buy and Sell Stock", "topic": "Sliding Window", "difficulty": "Easy", "lc_slug": "best-time-to-buy-and-sell-stock", "tags": "Sliding Window, Min Tracking"},
    "longest-substring-without-duplicates": {"id": 3, "title": "Longest Substring Without Repeating Characters", "topic": "Sliding Window", "difficulty": "Medium", "lc_slug": "longest-substring-without-repeating-characters", "tags": "Sliding Window, Set / Last Seen Map"},
    "longest-repeating-substring-with-replacement": {"id": 424, "title": "Longest Repeating Character Replacement", "topic": "Sliding Window", "difficulty": "Medium", "lc_slug": "longest-repeating-character-replacement", "tags": "Sliding Window, Max Frequency"},
    "permutation-string": {"id": 567, "title": "Permutation in String", "topic": "Sliding Window", "difficulty": "Medium", "lc_slug": "permutation-in-string", "tags": "Fixed Sliding Window, Char Count Match"},
    "minimum-window-with-characters": {"id": 76, "title": "Minimum Window Substring", "topic": "Sliding Window", "difficulty": "Hard", "lc_slug": "minimum-window-substring", "tags": "Sliding Window, Frequency Tracking"},
    "minimum-window-substring": {"id": 76, "title": "Minimum Window Substring", "topic": "Sliding Window", "difficulty": "Hard", "lc_slug": "minimum-window-substring", "tags": "Sliding Window, Frequency Tracking"},
    "sliding-window-maximum": {"id": 239, "title": "Sliding Window Maximum", "topic": "Sliding Window", "difficulty": "Hard", "lc_slug": "sliding-window-maximum", "tags": "Monotonic Deque"},

    # Stack
    "validate-parentheses": {"id": 20, "title": "Valid Parentheses", "topic": "Stack", "difficulty": "Easy", "lc_slug": "valid-parentheses", "tags": "Stack, LIFO Matching"},
    "minimum-stack": {"id": 155, "title": "Min Stack", "topic": "Stack", "difficulty": "Medium", "lc_slug": "min-stack", "tags": "Stack, Min Tracking Pair"},
    "evaluate-reverse-polish-notation": {"id": 150, "title": "Evaluate Reverse Polish Notation", "topic": "Stack", "difficulty": "Medium", "lc_slug": "evaluate-reverse-polish-notation", "tags": "Stack, Postfix Evaluation"},
    "generate-parentheses": {"id": 22, "title": "Generate Parentheses", "topic": "Stack", "difficulty": "Medium", "lc_slug": "generate-parentheses", "tags": "Backtracking, Stack Recursion"},
    "daily-temperatures": {"id": 739, "title": "Daily Temperatures", "topic": "Stack", "difficulty": "Medium", "lc_slug": "daily-temperatures", "tags": "Monotonic Stack"},
    "car-fleet": {"id": 853, "title": "Car Fleet", "topic": "Stack", "difficulty": "Medium", "lc_slug": "car-fleet", "tags": "Stack, Monotonic Arrival Times"},
    "largest-rectangle-in-histogram": {"id": 84, "title": "Largest Rectangle in Histogram", "topic": "Stack", "difficulty": "Hard", "lc_slug": "largest-rectangle-in-histogram", "tags": "Monotonic Stack, Area Calculation"},

    # Binary Search
    "binary-search": {"id": 704, "title": "Binary Search", "topic": "Binary Search", "difficulty": "Easy", "lc_slug": "binary-search", "tags": "Binary Search"},
    "search-2d-matrix": {"id": 74, "title": "Search a 2D Matrix", "topic": "Binary Search", "difficulty": "Medium", "lc_slug": "search-a-2d-matrix", "tags": "Binary Search, Virtual 1D Flattening"},
    "eating-bananas": {"id": 875, "title": "Koko Eating Bananas", "topic": "Binary Search", "difficulty": "Medium", "lc_slug": "koko-eating-bananas", "tags": "Binary Search on Answer Space"},
    "koko-eating-bananas": {"id": 875, "title": "Koko Eating Bananas", "topic": "Binary Search", "difficulty": "Medium", "lc_slug": "koko-eating-bananas", "tags": "Binary Search on Answer Space"},
    "find-minimum-in-rotated-sorted-array": {"id": 153, "title": "Find Minimum in Rotated Sorted Array", "topic": "Binary Search", "difficulty": "Medium", "lc_slug": "find-minimum-in-rotated-sorted-array", "tags": "Binary Search, Pivot Detection"},
    "find-target-in-rotated-sorted-array": {"id": 33, "title": "Search in Rotated Sorted Array", "topic": "Binary Search", "difficulty": "Medium", "lc_slug": "search-in-rotated-sorted-array", "tags": "Binary Search, Halves Discrimination"},
    "search-in-rotated-sorted-array": {"id": 33, "title": "Search in Rotated Sorted Array", "topic": "Binary Search", "difficulty": "Medium", "lc_slug": "search-in-rotated-sorted-array", "tags": "Binary Search, Halves Discrimination"},
    "time-based-key-value-store": {"id": 981, "title": "Time Based Key-Value Store", "topic": "Binary Search", "difficulty": "Medium", "lc_slug": "time-based-key-value-store", "tags": "Binary Search, Hash Map + Array"},
    "median-of-two-sorted-arrays": {"id": 4, "title": "Median of Two Sorted Arrays", "topic": "Binary Search", "difficulty": "Hard", "lc_slug": "median-of-two-sorted-arrays", "tags": "Binary Search, Array Partitioning"},

    # Linked List
    "reverse-a-linked-list": {"id": 206, "title": "Reverse Linked List", "topic": "Linked List", "difficulty": "Easy", "lc_slug": "reverse-linked-list", "tags": "Two Pointers, Pointer Manipulation"},
    "merge-two-sorted-linked-lists": {"id": 21, "title": "Merge Two Sorted Lists", "topic": "Linked List", "difficulty": "Easy", "lc_slug": "merge-two-sorted-lists", "tags": "Two Pointers, Dummy Head"},
    "reorder-linked-list": {"id": 143, "title": "Reorder List", "topic": "Linked List", "difficulty": "Medium", "lc_slug": "reorder-list", "tags": "Fast & Slow Pointers, In-place Reversal"},
    "remove-node-from-end-of-linked-list": {"id": 19, "title": "Remove Nth Node From End of List", "topic": "Linked List", "difficulty": "Medium", "lc_slug": "remove-nth-node-from-end-of-list", "tags": "Fast & Slow Pointers, Dummy Node"},
    "linked-list-cycle-detection": {"id": 141, "title": "Linked List Cycle", "topic": "Linked List", "difficulty": "Easy", "lc_slug": "linked-list-cycle", "tags": "Floyd's Tortoise and Hare"},
    "merge-k-sorted-linked-lists": {"id": 23, "title": "Merge K Sorted Lists", "topic": "Linked List", "difficulty": "Hard", "lc_slug": "merge-k-sorted-lists", "tags": "Divide and Conquer / Min-Heap"},

    # Trees
    "invert-a-binary-tree": {"id": 226, "title": "Invert Binary Tree", "topic": "Trees", "difficulty": "Easy", "lc_slug": "invert-binary-tree", "tags": "DFS Recursion / BFS"},
    "maximum-depth-of-binary-tree": {"id": 104, "title": "Maximum Depth of Binary Tree", "topic": "Trees", "difficulty": "Easy", "lc_slug": "maximum-depth-of-binary-tree", "tags": "DFS / BFS Level Order"},
    "same-binary-tree": {"id": 100, "title": "Same Tree", "topic": "Trees", "difficulty": "Easy", "lc_slug": "same-tree", "tags": "DFS Tree Comparison"},
    "subtree-of-a-binary-tree": {"id": 572, "title": "Subtree of Another Tree", "topic": "Trees", "difficulty": "Easy", "lc_slug": "subtree-of-another-tree", "tags": "DFS Tree Matching"},
    "lowest-common-ancestor-in-binary-search-tree": {"id": 235, "title": "Lowest Common Ancestor of a BST", "topic": "Trees", "difficulty": "Medium", "lc_slug": "lowest-common-ancestor-of-a-binary-search-tree", "tags": "BST Properties, Value Splitting"},
    "level-order-traversal-of-binary-tree": {"id": 102, "title": "Binary Tree Level Order Traversal", "topic": "Trees", "difficulty": "Medium", "lc_slug": "binary-tree-level-order-traversal", "tags": "BFS, Queue Level Batching"},
    "validate-binary-search-tree": {"id": 98, "title": "Validate Binary Search Tree", "topic": "Trees", "difficulty": "Medium", "lc_slug": "validate-binary-search-tree", "tags": "DFS In-order / Bounds Verification"},
    "kth-smallest-integer-in-bst": {"id": 230, "title": "Kth Smallest Element in a BST", "topic": "Trees", "difficulty": "Medium", "lc_slug": "kth-smallest-element-in-a-bst", "tags": "BST In-order Traversal"},
    "construct-binary-tree-from-preorder-and-inorder-traversal": {"id": 105, "title": "Construct Binary Tree from Preorder and Inorder Traversal", "topic": "Trees", "difficulty": "Medium", "lc_slug": "construct-binary-tree-from-preorder-and-inorder-traversal", "tags": "Divide & Conquer, Hash Map"},
    "binary-tree-maximum-path-sum": {"id": 124, "title": "Binary Tree Maximum Path Sum", "topic": "Trees", "difficulty": "Hard", "lc_slug": "binary-tree-maximum-path-sum", "tags": "DFS Post-order, Global Max"},
    "serialize-and-deserialize-binary-tree": {"id": 297, "title": "Serialize and Deserialize Binary Tree", "topic": "Trees", "difficulty": "Hard", "lc_slug": "serialize-and-deserialize-binary-tree", "tags": "Preorder DFS / BFS String Encoding"},

    # Tries
    "implement-prefix-tree": {"id": 208, "title": "Implement Trie (Prefix Tree)", "topic": "Tries", "difficulty": "Medium", "lc_slug": "implement-trie-prefix-tree", "tags": "Trie Node, Hash Map / Array"},
    "design-add-and-search-words-data-structure": {"id": 211, "title": "Design Add and Search Words Data Structure", "topic": "Tries", "difficulty": "Medium", "lc_slug": "design-add-and-search-words-data-structure", "tags": "Trie, Backtracking DFS"},
    "word-search-ii": {"id": 212, "title": "Word Search II", "topic": "Tries", "difficulty": "Hard", "lc_slug": "word-search-ii", "tags": "Trie + 2D Backtracking Grid DFS"},

    # Heap
    "find-median-from-data-stream": {"id": 295, "title": "Find Median from Data Stream", "topic": "Heap / Priority Queue", "difficulty": "Hard", "lc_slug": "find-median-from-data-stream", "tags": "Two Heaps (Max-Heap & Min-Heap)"},

    # Backtracking
    "combination-target-sum": {"id": 39, "title": "Combination Sum", "topic": "Backtracking", "difficulty": "Medium", "lc_slug": "combination-sum", "tags": "Backtracking, Decision Tree"},
    "word-search": {"id": 79, "title": "Word Search", "topic": "Backtracking", "difficulty": "Medium", "lc_slug": "word-search", "tags": "Backtracking, 2D Grid DFS"},

    # Graphs
    "count-number-of-islands": {"id": 200, "title": "Number of Islands", "topic": "Graphs", "difficulty": "Medium", "lc_slug": "number-of-islands", "tags": "Matrix BFS / DFS"},
    "number-of-islands": {"id": 200, "title": "Number of Islands", "topic": "Graphs", "difficulty": "Medium", "lc_slug": "number-of-islands", "tags": "Matrix BFS / DFS"},
    "clone-graph": {"id": 133, "title": "Clone Graph", "topic": "Graphs", "difficulty": "Medium", "lc_slug": "clone-graph", "tags": "Graph DFS / BFS + Hash Map"},
    "pacific-atlantic-water-flow": {"id": 417, "title": "Pacific Atlantic Water Flow", "topic": "Graphs", "difficulty": "Medium", "lc_slug": "pacific-atlantic-water-flow", "tags": "Multi-source Reverse BFS / DFS"},
    "course-schedule": {"id": 207, "title": "Course Schedule", "topic": "Graphs", "difficulty": "Medium", "lc_slug": "course-schedule", "tags": "Topological Sort (Kahn's / DFS)"},
    "count-connected-components": {"id": 323, "title": "Number of Connected Components in an Undirected Graph", "topic": "Graphs", "difficulty": "Medium", "lc_slug": "number-of-connected-components-in-an-undirected-graph", "tags": "Disjoint Set Union (DSU) / DFS"},
    "valid-tree": {"id": 261, "title": "Graph Valid Tree", "topic": "Graphs", "difficulty": "Medium", "lc_slug": "graph-valid-tree", "tags": "DSU / Cycle Detection BFS"},

    # Advanced Graphs
    "foreign-dictionary": {"id": 269, "title": "Alien Dictionary", "topic": "Advanced Graphs", "difficulty": "Hard", "lc_slug": "alien-dictionary", "tags": "Topological Sort, DAG Cycle Detection"},
    "alien-dictionary": {"id": 269, "title": "Alien Dictionary", "topic": "Advanced Graphs", "difficulty": "Hard", "lc_slug": "alien-dictionary", "tags": "Topological Sort, DAG Cycle Detection"},

    # 1-D DP
    "climbing-stairs": {"id": 70, "title": "Climbing Stairs", "topic": "1-D DP", "difficulty": "Easy", "lc_slug": "climbing-stairs", "tags": "1-D Dynamic Programming, Fibonacci"},
    "cost-of-climbing-stairs": {"id": 746, "title": "Min Cost Climbing Stairs", "topic": "1-D DP", "difficulty": "Easy", "lc_slug": "min-cost-climbing-stairs", "tags": "1-D DP, State Reduction"},
    "house-robber": {"id": 198, "title": "House Robber", "topic": "1-D DP", "difficulty": "Medium", "lc_slug": "house-robber", "tags": "1-D DP, Include / Exclude"},
    "house-robber-ii": {"id": 213, "title": "House Robber II", "topic": "1-D DP", "difficulty": "Medium", "lc_slug": "house-robber-ii", "tags": "1-D DP, Circular Boundary Splitting"},
    "longest-palindromic-substring": {"id": 5, "title": "Longest Palindromic Substring", "topic": "1-D DP", "difficulty": "Medium", "lc_slug": "longest-palindromic-substring", "tags": "Expand Around Center / 2D DP"},
    "palindromic-substrings": {"id": 647, "title": "Palindromic Substrings", "topic": "1-D DP", "difficulty": "Medium", "lc_slug": "palindromic-substrings", "tags": "Expand Around Center / DP"},
    "decode-ways": {"id": 91, "title": "Decode Ways", "topic": "1-D DP", "difficulty": "Medium", "lc_slug": "decode-ways", "tags": "1-D DP, String Parsing"},
    "coin-change": {"id": 322, "title": "Coin Change", "topic": "1-D DP", "difficulty": "Medium", "lc_slug": "coin-change", "tags": "1-D DP, Unbounded Knapsack"},
    "maximum-product-subarray": {"id": 152, "title": "Maximum Product Subarray", "topic": "1-D DP", "difficulty": "Medium", "lc_slug": "maximum-product-subarray", "tags": "DP, Min / Max Product State"},
    "word-break": {"id": 139, "title": "Word Break", "topic": "1-D DP", "difficulty": "Medium", "lc_slug": "word-break", "tags": "1-D DP + Hash Set / Trie"},
    "longest-increasing-subsequence": {"id": 300, "title": "Longest Increasing Subsequence", "topic": "1-D DP", "difficulty": "Medium", "lc_slug": "longest-increasing-subsequence", "tags": "DP / Binary Search Patience Sort"},

    # 2-D DP
    "unique-paths": {"id": 62, "title": "Unique Paths", "topic": "2-D DP", "difficulty": "Medium", "lc_slug": "unique-paths", "tags": "2-D DP, Grid State Reduction"},
    "longest-common-subsequence": {"id": 1143, "title": "Longest Common Subsequence", "topic": "2-D DP", "difficulty": "Medium", "lc_slug": "longest-common-subsequence", "tags": "2-D DP Matrix Matching"},

    # Greedy
    "maximum-subarray": {"id": 53, "title": "Maximum Subarray", "topic": "Greedy", "difficulty": "Medium", "lc_slug": "maximum-subarray", "tags": "Kadane's Algorithm, Greedy"},
    "jump-game": {"id": 55, "title": "Jump Game", "topic": "Greedy", "difficulty": "Medium", "lc_slug": "jump-game", "tags": "Greedy Max Reachable Index"},

    # Intervals
    "insert-interval": {"id": 57, "title": "Insert Interval", "topic": "Intervals", "difficulty": "Medium", "lc_slug": "insert-interval", "tags": "Intervals, In-order Merging"},
    "merge-intervals": {"id": 56, "title": "Merge Intervals", "topic": "Intervals", "difficulty": "Medium", "lc_slug": "merge-intervals", "tags": "Sorting + Interval Overlap Merge"},
    "non-overlapping-intervals": {"id": 435, "title": "Non-overlapping Intervals", "topic": "Intervals", "difficulty": "Medium", "lc_slug": "non-overlapping-intervals", "tags": "Greedy Interval Scheduling"},
    "meeting-rooms": {"id": 252, "title": "Meeting Rooms", "topic": "Intervals", "difficulty": "Easy", "lc_slug": "meeting-rooms", "tags": "Intervals, Sort & Check Overlap"},
    "meeting-rooms-ii": {"id": 253, "title": "Meeting Rooms II", "topic": "Intervals", "difficulty": "Medium", "lc_slug": "meeting-rooms-ii", "tags": "Min-Heap / Chronological Two Pointers"},

    # Math & Geometry
    "rotate-image": {"id": 48, "title": "Rotate Image", "topic": "Math & Geometry", "difficulty": "Medium", "lc_slug": "rotate-image", "tags": "Matrix Transpose & Reverse"},
    "spiral-matrix": {"id": 54, "title": "Spiral Matrix", "topic": "Math & Geometry", "difficulty": "Medium", "lc_slug": "spiral-matrix", "tags": "Boundary Simulation"},
    "set-matrix-zeroes": {"id": 73, "title": "Set Matrix Zeroes", "topic": "Math & Geometry", "difficulty": "Medium", "lc_slug": "set-matrix-zeroes", "tags": "In-place Array Marking"},

    # Bit Manipulation
    "number-of-one-bits": {"id": 191, "title": "Number of 1 Bits", "topic": "Bit Manipulation", "difficulty": "Easy", "lc_slug": "number-of-1-bits", "tags": "Brian Kernighan's Algorithm, Bitwise"},
    "counting-bits": {"id": 338, "title": "Counting Bits", "topic": "Bit Manipulation", "difficulty": "Easy", "lc_slug": "counting-bits", "tags": "DP + Bit Shifting"},
    "reverse-bits": {"id": 190, "title": "Reverse Bits", "topic": "Bit Manipulation", "difficulty": "Easy", "lc_slug": "reverse-bits", "tags": "Bit Manipulation, 32-bit Shift"},
    "missing-number": {"id": 268, "title": "Missing Number", "topic": "Bit Manipulation", "difficulty": "Easy", "lc_slug": "missing-number", "tags": "XOR Accumulation / Gauss Sum"},
    "sum-of-two-integers": {"id": 371, "title": "Sum of Two Integers", "topic": "Bit Manipulation", "difficulty": "Medium", "lc_slug": "sum-of-two-integers", "tags": "Bitwise XOR & AND Carry Shift"},
}


def url_encode_path(*parts) -> str:
    """Properly encode relative path components for valid GitHub markdown links."""
    return "./" + "/".join(urllib.parse.quote(str(part)) for part in parts)


def parse_problem_folder(prob_dir: Path, topic_name: str, slug: str):
    """Parse a problem directory and return structured metadata and submission count."""
    submissions = list(prob_dir.glob("submission-*.py"))
    if not submissions:
        submissions = list(prob_dir.glob("*.py"))
    if not submissions:
        return None, 0

    def parse_submission_num(p: Path):
        m = re.search(r"submission-(\d+)", p.name)
        return int(m.group(1)) if m else 999

    submissions.sort(key=parse_submission_num)

    meta = PROBLEM_METADATA.get(slug)
    if meta:
        prob_id = meta["id"]
        title = meta["title"]
        difficulty = meta["difficulty"]
        lc_slug = meta.get("lc_slug", slug)
        lc_url = f"https://leetcode.com/problems/{lc_slug}/"
        neetcode_url = f"https://neetcode.io/problems/{slug}"
        tags = meta["tags"]
        # Use canonical topic from metadata if available
        final_topic = meta.get("topic", topic_name)
    else:
        prob_id = 9999
        title = slug.replace("-", " ").title()
        difficulty = "Medium"
        lc_url = f"https://leetcode.com/problems/{slug}/"
        neetcode_url = f"https://neetcode.io/problems/{slug}"
        tags = "General Algorithm"
        final_topic = topic_name

    submission_links = []
    # Relative path from repository root
    rel_folder_parts = prob_dir.relative_to(REPO_ROOT).parts

    for sub in submissions:
        sub_name = sub.stem.replace("submission-", "v")
        sub_rel_path = url_encode_path(*rel_folder_parts, sub.name)
        submission_links.append({"label": sub_name, "path": sub_rel_path, "filename": sub.name})

    latest_sub = submission_links[-1]

    prob_data = {
        "id": prob_id,
        "slug": slug,
        "title": title,
        "topic": final_topic,
        "difficulty": difficulty,
        "lc_url": lc_url,
        "neetcode_url": neetcode_url,
        "tags": tags,
        "submission_count": len(submissions),
        "submissions": submission_links,
        "latest_sub": latest_sub,
        "rel_dir": url_encode_path(*rel_folder_parts)
    }

    return prob_data, len(submissions)


def scan_repository():
    """
    Recursively scan 'Data Structures & Algorithms'.
    Handles both nested topic directories and direct problem directories.
    """
    problems_by_topic = {}
    all_problems = []
    total_submissions_count = 0

    if not DSA_DIR.exists():
        print(f"Directory {DSA_DIR} does not exist.")
        return problems_by_topic, all_problems, 0

    for entry in sorted(DSA_DIR.iterdir()):
        if not entry.is_dir() or entry.name.startswith("."):
            continue

        direct_py = list(entry.glob("submission-*.py")) or list(entry.glob("*.py"))
        if direct_py:
            # Direct problem folder
            slug = entry.name
            meta = PROBLEM_METADATA.get(slug, {})
            topic_name = meta.get("topic", "General")
            prob_data, subs_cnt = parse_problem_folder(entry, topic_name, slug)
            if prob_data:
                problems_by_topic.setdefault(prob_data["topic"], []).append(prob_data)
                all_problems.append(prob_data)
                total_submissions_count += subs_cnt
        else:
            # Topic directory containing problem folders
            topic_name = entry.name
            for prob_dir in sorted(entry.iterdir()):
                if not prob_dir.is_dir() or prob_dir.name.startswith("."):
                    continue
                slug = prob_dir.name
                prob_data, subs_cnt = parse_problem_folder(prob_dir, topic_name, slug)
                if prob_data:
                    problems_by_topic.setdefault(prob_data["topic"], []).append(prob_data)
                    all_problems.append(prob_data)
                    total_submissions_count += subs_cnt

    # Sort problems within each topic by ID
    for topic_name in problems_by_topic:
        problems_by_topic[topic_name].sort(key=lambda x: x["id"])

    return problems_by_topic, all_problems, total_submissions_count


def generate_badges(total_solved: int, target_total: int, easy_cnt: int, med_cnt: int, hard_cnt: int, total_attempts: int) -> str:
    """Generate professional badges cluster."""
    pct = round((total_solved / target_total) * 100, 1) if target_total else 0
    badges = [
        f"[![LeetCode Profile](https://img.shields.io/badge/LeetCode-@{LEETCODE_USERNAME}-FFA116?style=for-the-badge&logo=leetcode&logoColor=white)]({LEETCODE_PROFILE_URL})",
        f"[![Blind 75 Progress](https://img.shields.io/badge/Blind_75-{total_solved}%2F{target_total}_({pct}%25)-2563EB?style=for-the-badge&logo=target&logoColor=white)](#-live-metrics-dashboard)",
        f"[![Easy Solved](https://img.shields.io/badge/Easy-{easy_cnt}-22C55E?style=for-the-badge)](#-complete-solutions-directory)",
        f"[![Medium Solved](https://img.shields.io/badge/Medium-{med_cnt}-F59E0B?style=for-the-badge)](#-complete-solutions-directory)",
        f"[![Hard Solved](https://img.shields.io/badge/Hard-{hard_cnt}-EF4444?style=for-the-badge)](#-complete-solutions-directory)",
        f"[![Total Attempts](https://img.shields.io/badge/Iterations-{total_attempts}_attempts-8B5CF6?style=for-the-badge&logo=git&logoColor=white)](#-iterative-refinement-framework)",
        f"[![Language](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)",
        f"[![CI/CD Automated](https://img.shields.io/badge/CI%2FCD-Auto--Catalog-06B6D4?style=for-the-badge&logo=githubactions&logoColor=white)]({REPO_URL}/actions)",
        f"[![LinkedIn](https://img.shields.io/badge/LinkedIn-Sai_Srikar-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)]({LINKEDIN_URL})",
        f"[![Views](https://komarev.com/ghpvc/?username=Saisrikar20-neetcode-submissions&label=REPO+VIEWS&color=0e75b6&style=for-the-badge)]({REPO_URL})"
    ]
    return " ".join(badges)


def generate_metrics_card(total_solved: int, target_total: int, easy: int, medium: int, hard: int, total_attempts: int) -> str:
    """Generate high-aesthetic markdown executive metrics dashboard."""
    def progress_bar(count, total_count, length=12):
        if total_count == 0:
            pct = 0.0
        else:
            pct = (count / total_count) * 100
        filled = int(round((pct / 100) * length))
        bar = "█" * filled + "░" * (length - filled)
        return f"`{bar}` **{pct:.1f}%**"

    overall_bar = progress_bar(total_solved, target_total, 15)
    easy_bar = progress_bar(easy, total_solved, 12) if total_solved else "`░░░░░░░░░░░░` 0.0%"
    med_bar = progress_bar(medium, total_solved, 12) if total_solved else "`░░░░░░░░░░░░` 0.0%"
    hard_bar = progress_bar(hard, total_solved, 12) if total_solved else "`░░░░░░░░░░░░` 0.0%"

    avg_attempts = f"{(total_attempts / total_solved):.1f}" if total_solved else "0"

    card = [
        "| Metric | Count | Visual Distribution / Goal | Status |",
        "|:---|:---:|:---|:---:|",
        f"| 🎯 **Blind 75 Benchmark** | **{total_solved} / {target_total}** | {overall_bar} | ⚡ **In Flight** |",
        f"| {DIFFICULTY_ICONS['Easy']} **Easy Problems** | **{easy}** | {easy_bar} of solved | 🟢 Stable |",
        f"| {DIFFICULTY_ICONS['Medium']} **Medium Problems** | **{medium}** | {med_bar} of solved | 🟡 Core Focus |",
        f"| {DIFFICULTY_ICONS['Hard']} **Hard Problems** | **{hard}** | {hard_bar} of solved | 🔴 Frontier |",
        f"| 🔁 **Submissions Tracked** | **{total_attempts}** | Avg **{avg_attempts}** iterations / problem | 🚀 Iterative |",
    ]
    return "\n".join(card)


def generate_topic_matrix(problems_by_topic: dict) -> str:
    """Generate comprehensive progress matrix across all 18 DSA categories."""
    lines = [
        "| # | Topic | Status | Solved / Target | Completion Bar | Key Patterns Explored |",
        "|:---:|:---|:---:|:---:|:---|:---|"
    ]

    def topic_bar(solved, target, length=8):
        pct = (solved / target) * 100 if target else 0
        filled = min(length, int(round((pct / 100) * length)))
        bar = "█" * filled + "░" * (length - filled)
        return f"`{bar}` {pct:.0f}%"

    for idx, topic in enumerate(TOPIC_ORDER, 1):
        solved_list = problems_by_topic.get(topic, [])
        solved_cnt = len(solved_list)
        target_cnt = TOPIC_TARGETS.get(topic, 0)

        if solved_cnt >= target_cnt and target_cnt > 0:
            status = "🟢 Done"
        elif solved_cnt > 0:
            status = "🟡 In Progress"
        else:
            status = "⚪ Queued"

        bar = topic_bar(solved_cnt, target_cnt)

        if solved_list:
            patterns = ", ".join(sorted(list(set(p["tags"].split(", ")[0] for p in solved_list))))
            topic_cell = f"**[{topic}](#{topic.lower().replace(' ', '-').replace('&', '').replace('/', '')})**"
        else:
            patterns = "—"
            topic_cell = f"**{topic}**"

        lines.append(f"| {idx:02d} | {topic_cell} | {status} | **{solved_cnt}** / {target_cnt} | {bar} | {patterns} |")

    return "\n".join(lines)


def generate_solutions_drawers(problems_by_topic: dict) -> str:
    """Generate rich collapsible accordion cards for each topic containing solved problems."""
    sections = [
        "> 💡 **Pro Tip:** Click any category drawer below to expand solutions and iterations. Multiple versions (`v0`, `v1`, `v2`) reflect progressive optimization from initial working brute-force to optimal time/space complexity.\n"
    ]

    for topic in TOPIC_ORDER:
        probs = problems_by_topic.get(topic, [])
        if not probs:
            continue

        topic_anchor = topic.lower().replace(' ', '-').replace('&', '').replace('/', '')
        open_attr = " open"

        target = TOPIC_TARGETS.get(topic, len(probs))
        pct = int((len(probs) / target) * 100) if target else 100

        drawer_header = f"<summary><b id=\"{topic_anchor}\">📁 {topic} ({len(probs)}/{target} solved — {pct}%)</b> — <i>Click to expand/collapse</i></summary>\n"

        rows = [
            "| # | Problem Title | LeetCode | Difficulty | Iterations | Latest Code | Algorithmic Pattern |",
            "|:---:|:---|:---:|:---:|:---:|:---:|:---|"
        ]

        for p in probs:
            diff_icon = DIFFICULTY_ICONS.get(p["difficulty"], "⚪")
            diff_badge = f"{diff_icon} **{p['difficulty']}**"

            v_links = " · ".join([f"[{sub['label']}]({sub['path']})" for sub in p["submissions"]])
            latest_link = f"[💻 **{p['latest_sub']['label']}**]({p['latest_sub']['path']})"
            lc_link = f"[#{p['id']} LC]({p['lc_url']})"
            title_link = f"**[{p['title']}]({p['neetcode_url']})**"

            rows.append(
                f"| {p['id']} | {title_link} | {lc_link} | {diff_badge} | {v_links} | {latest_link} | `{p['tags']}` |"
            )

        sections.append(f"<details{open_attr}>\n{drawer_header}\n" + "\n".join(rows) + "\n\n</details>\n")

    return "\n".join(sections)


def generate_solutions_catalog_md(all_problems: list, total_solved: int, target_total: int, easy: int, medium: int, hard: int, total_attempts: int):
    """Generate comprehensive dedicated SOLUTIONS.md master catalog."""
    lines = [
        "# 📑 Master DSA Solutions & Iterations Catalog",
        "",
        f"A comprehensive indexing of all **{total_solved}** solved problems and **{total_attempts}** solution iterations from the Blind 75 / NeetCode curriculum.",
        "",
        f"- **Curriculum Progress:** {total_solved} / {target_total} ({(total_solved/target_total)*100:.1f}%)",
        f"- **Difficulty Distribution:** 🟢 Easy: {easy} | 🟡 Medium: {medium} | 🔴 Hard: {hard}",
        f"- **Total Solution Iterations:** {total_attempts} attempts",
        f"- **Author Profile:** [@{LEETCODE_USERNAME}]({LEETCODE_PROFILE_URL})",
        "",
        "[⬅️ Return to Main README](./README.md)",
        "",
        "---",
        "",
        "| # | Topic | Problem Title | LeetCode | NeetCode | Difficulty | Iterations | Latest Solution | Algorithmic Strategy |",
        "|:---:|:---|:---|:---:|:---:|:---:|:---:|:---:|:---|"
    ]

    all_problems_sorted = sorted(all_problems, key=lambda x: (x["topic"], x["id"]))

    for p in all_problems_sorted:
        diff_color = DIFFICULTY_COLORS.get(p["difficulty"], "888888")
        diff_badge = f'<img src="https://img.shields.io/badge/-{p["difficulty"]}-{diff_color}?style=flat-square" alt="{p["difficulty"]}">'
        v_links = " · ".join([f"[`{sub['label']}`]({sub['path']})" for sub in p["submissions"]])
        latest_link = f"[💻 Code]({p['latest_sub']['path']})"
        lc_badge = f"[LC #{p['id']}]({p['lc_url']})"
        nc_link = f"[NeetCode]({p['neetcode_url']})"

        lines.append(
            f"| {p['id']} | **{p['topic']}** | **{p['title']}** | {lc_badge} | {nc_link} | {diff_badge} | {v_links} | {latest_link} | `{p['tags']}` |"
        )

    lines.append("")
    lines.append("---")
    lines.append(f"<sub>Generated automatically by `scripts/update_readme.py` • Synced for [{GITHUB_USER}]({REPO_URL})</sub>")

    SOLUTIONS_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Generated {SOLUTIONS_PATH}")


def update_readme():
    """Main routine to scan codebase and update README.md and SOLUTIONS.md."""
    problems_by_topic, all_problems, total_attempts = scan_repository()
    total_solved = len(all_problems)
    easy_cnt = sum(1 for p in all_problems if p["difficulty"] == "Easy")
    med_cnt = sum(1 for p in all_problems if p["difficulty"] == "Medium")
    hard_cnt = sum(1 for p in all_problems if p["difficulty"] == "Hard")

    badges_md = generate_badges(total_solved, TARGET_BLIND75_TOTAL, easy_cnt, med_cnt, hard_cnt, total_attempts)
    metrics_md = generate_metrics_card(total_solved, TARGET_BLIND75_TOTAL, easy_cnt, med_cnt, hard_cnt, total_attempts)
    topics_md = generate_topic_matrix(problems_by_topic)
    drawers_md = generate_solutions_drawers(problems_by_topic)

    # Maintain SOLUTIONS.md
    generate_solutions_catalog_md(all_problems, total_solved, TARGET_BLIND75_TOTAL, easy_cnt, med_cnt, hard_cnt, total_attempts)

    if not README_PATH.exists():
        print(f"Error: {README_PATH} not found.")
        return

    content = README_PATH.read_text(encoding="utf-8")

    # Replace Badges
    if "<!-- BADGES:START -->" in content and "<!-- BADGES:END -->" in content:
        content = re.sub(
            r"<!-- BADGES:START -->.*?<!-- BADGES:END -->",
            f"<!-- BADGES:START -->\n{badges_md}\n<!-- BADGES:END -->",
            content,
            flags=re.DOTALL
        )

    # Replace Metrics
    if "<!-- METRICS:START -->" in content and "<!-- METRICS:END -->" in content:
        content = re.sub(
            r"<!-- METRICS:START -->.*?<!-- METRICS:END -->",
            f"<!-- METRICS:START -->\n{metrics_md}\n<!-- METRICS:END -->",
            content,
            flags=re.DOTALL
        )

    # Replace Topics Table
    if "<!-- TOPICS_TABLE:START -->" in content and "<!-- TOPICS_TABLE:END -->" in content:
        content = re.sub(
            r"<!-- TOPICS_TABLE:START -->.*?<!-- TOPICS_TABLE:END -->",
            f"<!-- TOPICS_TABLE:START -->\n{topics_md}\n<!-- TOPICS_TABLE:END -->",
            content,
            flags=re.DOTALL
        )

    # Replace Problems Accordion
    if "<!-- SOLUTIONS_TABLE:START -->" in content and "<!-- SOLUTIONS_TABLE:END -->" in content:
        content = re.sub(
            r"<!-- SOLUTIONS_TABLE:START -->.*?<!-- SOLUTIONS_TABLE:END -->",
            f"<!-- SOLUTIONS_TABLE:START -->\n{drawers_md}\n<!-- SOLUTIONS_TABLE:END -->",
            content,
            flags=re.DOTALL
        )

    README_PATH.write_text(content, encoding="utf-8")
    print(f"Successfully updated README.md: {total_solved} solved ({easy_cnt} Easy, {med_cnt} Med, {hard_cnt} Hard) across {total_attempts} attempts.")


if __name__ == "__main__":
    update_readme()

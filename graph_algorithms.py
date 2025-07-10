# Graph and Dynamic Programming Algorithms Analysis

# Problem 1: All Paths in a DAG
# Find all paths from node 0 to node n-1 in a directed acyclic graph

def allPathsDisplay(graph):
    """
    Find all paths from source (0) to destination (n-1) in a DAG.
    
    Time Complexity: O(2^n) in worst case, but typically much better for DAGs
    Space Complexity: O(n) for recursion stack + O(2^n) for result storage
    """
    n = len(graph) - 1
    result = []

    def dfs(node, path):
        if node == n:
            result.append(path[:])  # Make a copy of the path
            return
        
        for neighbor in graph[node]:
            path.append(neighbor)
            dfs(neighbor, path)
            path.pop()  # Backtrack
    
    dfs(0, [0])
    return result

# Test cases for allPathsDisplay
test_cases = [
    ([[1,2],[3],[3],[]], [[0,1,3],[0,2,3]]),
    ([[1, 2],[3],[3],[4],[]], [[0,1,3,4],[0,2,3,4]]),
    ([[1],[2],[3],[]], [[0,1,2,3]]),
    ([[1,2,3],[4],[4],[4],[]], [[0,1,4],[0,2,4],[0,3,4]])
]

print("Testing allPathsDisplay:")
for graph, expected in test_cases:
    result = allPathsDisplay(graph)
    print(f"Graph: {graph}")
    print(f"Result: {result}")
    print(f"Expected: {expected}")
    print(f"Correct: {result == expected}")
    print()

# Problem 2: Partition Equal Subset Sum
# Check if array can be partitioned into two subsets with equal sums

def isSubsetPossible(nums):
    """
    Check if array can be partitioned into two subsets with equal sums.
    
    Time Complexity: O(n * target) where target = sum(nums) // 2
    Space Complexity: O(target)
    """
    total_sum = sum(nums)
    
    # If total sum is odd, no partition possible
    if total_sum % 2 != 0:
        return False
    
    target = total_sum // 2
    
    # dp[i] = True if we can form sum i using some subset of nums
    dp = [False] * (target + 1)
    dp[0] = True  # Base case: empty subset has sum 0
    
    # For each number, try to form all possible sums
    for num in nums:
        # Iterate backwards to avoid using same element multiple times
        for j in range(target, num - 1, -1):
            dp[j] = dp[j] or dp[j - num]
    
    return dp[target]

# Test cases for isSubsetPossible
subset_test_cases = [
    ([10, 4, 6, 3], False),
    ([10, 4, 6], True),
    ([1, 5, 11, 5], True),
    ([1, 5, 3], False),
    ([2, 2, 2, 2], True),
    ([1, 2, 3, 4, 5, 6, 7], True),  # Sum = 28, target = 14
    ([1, 2, 5], False)  # Sum = 8, odd
]

print("Testing isSubsetPossible:")
for nums, expected in subset_test_cases:
    result = isSubsetPossible(nums)
    print(f"Array: {nums}, Sum: {sum(nums)}")
    print(f"Result: {result}")
    print(f"Expected: {expected}")
    print(f"Correct: {result == expected}")
    print()

# Alternative implementation with memoization for better understanding
def isSubsetPossibleMemo(nums):
    """
    Alternative implementation using memoization for clarity.
    """
    total_sum = sum(nums)
    if total_sum % 2 != 0:
        return False
    
    target = total_sum // 2
    memo = {}
    
    def can_form_sum(index, current_sum):
        if current_sum == target:
            return True
        if current_sum > target or index >= len(nums):
            return False
        
        state = (index, current_sum)
        if state in memo:
            return memo[state]
        
        # Try including or excluding current number
        result = (can_form_sum(index + 1, current_sum + nums[index]) or 
                 can_form_sum(index + 1, current_sum))
        
        memo[state] = result
        return result
    
    return can_form_sum(0, 0)

print("Testing memoization version:")
for nums, expected in subset_test_cases[:3]:  # Test first 3 cases
    result = isSubsetPossibleMemo(nums)
    print(f"Array: {nums}")
    print(f"Result: {result}")
    print(f"Expected: {expected}")
    print(f"Correct: {result == expected}")
    print() 
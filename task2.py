def binary_search_with_bound(arr, target):
    """
    Binary search on a sorted list of floats.
    Returns: (steps, upper_bound)
    upper_bound = smallest value >= target, or None.
    """
    if not arr:  # empty list case
        return 0, None

    left = 0
    right = len(arr) - 1
    steps = 0
    upper_bound = None

    while left <= right:
        steps += 1
        mid = (left + right) // 2
        mid_val = arr[mid]

        if mid_val == target:
            # found exact value -> it's also a valid upper bound
            return steps, mid_val

        if mid_val > target:
            # candidate for upper bound, try to find smaller one on the left
            upper_bound = mid_val
            right = mid - 1
        else:
            # mid_val < target -> go right
            left = mid + 1

    return steps, upper_bound


# demo test
arr = [0.5, 1.2, 2.8, 3.3, 4.7, 5.0, 7.1]

print(binary_search_with_bound(arr, 3.0))  # -> (steps, 3.3)
print(binary_search_with_bound(arr, 4.7))  # -> (steps, 4.7) exact match
print(binary_search_with_bound(arr, 7.5))  # -> (steps, None)
print(binary_search_with_bound(arr, 0.1))  # -> (steps, 0.5)
print(binary_search_with_bound([], 5))     # -> (0, None)

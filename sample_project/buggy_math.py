def average(nums):
    # BUG: 当 nums 为空会报错；并且这里的除法可能不是你想要的行为
    total = 0
    for n in nums:
        total += n
    return total / len(nums)


def parse_int_list(s: str):
    # BUG: 有空格或空字符串时会异常
    return [int(x) for x in s.split(",")]


if __name__ == "__main__":
    data = "1, 2, 3, 4"
    nums = parse_int_list(data)
    print("avg:", average(nums))
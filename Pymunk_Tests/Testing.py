import re


def reformatNumber(number: str) -> str:
    number_split = re.split("[ -]", number)
    num_join = "".join(number_split)
    number_array = [i for i in num_join]
    size = len(number_array)
    divisible_by_3 = int(size / 3) * 3
    if size - divisible_by_3 == 1:
        divisible_by_3 -= 3
    triplets = number_array[:divisible_by_3]
    doubles = number_array[divisible_by_3:]

    delim_indices = [i for i in range(3, len(triplets) - 1, 3)]
    for ind in reversed(delim_indices):
        triplets.insert(ind, '-')
    if len(doubles) == 0:
        return "".join(triplets)

    delim_indices = [i for i in range(2, len(doubles) - 1, 2)]
    for ind in reversed(delim_indices):
        doubles.insert(ind, '-')

    return "".join(("".join(triplets), "-", "".join(doubles)))

if __name__ == "__main__":
    num = "1-23-45 6899"
    print(reformatNumber(num))

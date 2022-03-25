from itertools import cycle

MAX_PER_MIN = 120

groups = [[] for i in range(10)]


def make_distribution(
        ids_to_distribute,
        group: list,
        parsed: bool = False
) -> list:
    if not group:
        group = [[] for _ in range(10)]
    if parsed:
        for i in cycle(group):
            if not ids_to_distribute:
                return group
            num = ids_to_distribute.pop(0)
            i.append(num)

    for g in cycle(group):
        while len(g) < MAX_PER_MIN:
            if not ids_to_distribute:
                break
            num = ids_to_distribute.pop(0)
            g.append(num)
        if ids_to_distribute and sum([len(i) for i in group]) == len(group) * MAX_PER_MIN or not ids_to_distribute:
            return make_distribution(ids_to_distribute, group, True)
    else:
        return group


def iter_distribution(values_to_distribute, group, parsed=False):
    for i in make_distribution(values_to_distribute, group, parsed):
        yield i


def test_iter_distribution():
    responses = [
        [1, 11, 21, 31],
        [2, 12, 22, 32],
        [3, 13, 23],
        [4, 14, 24],
        [5, 15, 25],
        [6, 16, 26],
        [7, 17, 27],
        [8, 18, 28],
        [9, 19, 29],
        [10, 20, 30]
    ]
    for i, res in zip(iter_distribution([11, 12, 13, 14, 15], groups), responses):
        assert i == res


# test_iter_distribution()

# for dis in iter_distribution([i for i in range(11, 15)], groups, parsed=True):
#     print(dis)

# for dis in iter_distribution([i for i in range(11, 35)], groups):
#     print(dis)

# m = make_distribution([11, 12, 13, 14, 15, 16])
# print(m)

import math


def get_coords(i, delta, dist=20):
    x = dist * math.cos(i * delta)
    y = dist * math.sin(i * delta)
    return x, y


def get_unique_keys(param):
    temp_set = set()
    for node in param:
        temp_set.add(node)
        for adjacent_node in param[node]:
            temp_set.add(adjacent_node)
    return list(temp_set)


def parse_dict(param):
    keys = get_unique_keys(param)
    temp_dict = dict()
    for node in param:
        temp_list = list()
        for adjacent_node in param[node]:
            list.append(keys.index(adjacent_node))
        temp_dict[keys.index(node)] = temp_list
    return temp_dict


def memoize(f):
    memo = {}

    def helper(x):
        if x not in memo:
            memo[x] = f(x)
        else:
            print('memoized')
        return memo[x]

    return helper


def relax(x):
    return x


if __name__ == "__main__":
    mem = memoize(relax)
    mem(1)
    print(mem(1))
    print(mem(1))

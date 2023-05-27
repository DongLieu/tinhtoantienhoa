from random import randint, choice
from math import floor, log2, pow

DIMS = 2
N = 15
ITERATION = 1000


def weakly_dominate(x, y):
    for i in range(DIMS):
        if x[i] > y[i]:
            return False
    return True


def dominate(x, y):
    for i in range(DIMS):
        if x[i] >= y[i]:
            return False
    return True


def box_index(x):
    res = 0
    for i in range(DIMS):
        res = max(res, floor(log2(x[i]))+1)
    return res


def min_set(set_points):
    result = []
    exist = []
    for x in set_points:
        if x in exist:
            continue
        fl = True
        for y in set_points:
            if x == y:
                exist.append(y)
            if x != y and dominate(y, x):
                fl = False
                break
        if fl:
            result.append(x)
    return result


def box_b(x, b):
    res = [0 for i in range(DIMS)]
    for i in range(DIMS):
        res[i] = floor(x[i]*pow(2, -b))
    return res


for id_iter in range(ITERATION):
    archive_set = []
    solutions = []
    for i in range(100):
        tmp = []
        for id in range(DIMS):
            f = randint(10, 100)
            tmp.append(f)
        solutions.append(tmp)

    for solution in solutions:
        fl = True
        for a in archive_set:
            if dominate(a, solution):
                fl = False
                break
        if not fl:
            continue
        archive_set.append(solution)
        A = min_set(archive_set)
        if len(A) <= N:
            archive_set = A
            continue
        # print(len(A))
        Z = []
        B = 0
        for a in A:
            B = max(B, box_index(a))
        for b in range(B+1):
            fl = True
            for a in A:
                if not fl:
                    break
                for a_ in A:
                    if not fl:
                        break
                    if a != a_ and weakly_dominate(box_b(a, b), box_b(a_, b)):
                        fl = False
                        Z.append(b)
        # print('z'+str(Z))
        if len(Z) == 0:
            archive_set.remove(solution)
            continue
        beta = Z[0]
        D = []
        for a in A:
            for a_ in A:
                if a != a_ and weakly_dominate(box_b(a, beta), box_b(a_, beta)):
                    D.append(a)
                    break
        # print(solution)
        # print(D)
        if solution in D:
            archive_set.remove(solution)
            continue
        else:
            A.remove(choice(A))
            archive_set = A

    # print(len(archive_set))
    # print([point for point in archive_set])
    # print('ok')

    # TEST
    if len(archive_set)>N:
        print('size fail')
    for a in archive_set:
        for a_ in archive_set:
            if a != a_ and dominate(a, a_) and dominate(a_, a):
                print('archive_set fail')

    for a in archive_set:
        for solution in solutions:
            if dominate(solution, a):
                print('fail')
                # print(solution)
                # print(a)
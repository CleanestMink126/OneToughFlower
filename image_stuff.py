import numpy as np


def get_dir_dict():
    l = {str(np.array([0, 0, 0, 0])): 0,
         str(np.array([0, 0, 1, 0])): 2,
         str(np.array([1, 0, 0, 1])): 9,
         str(np.array([0, 1, 0, 1])): 5,
         str(np.array([1, 0, 1, 1])): 11,
         str(np.array([1, 1, 1, 1])): 15}
    d = {}
    for i in range(16):
        e = [int(digit) for digit in bin(i)[2:]]
        if len(e) < 4:
            e = ((4 - len(e)) * [0]) + e
        # print(e)
        arr = np.array(e)
        rot = 0
        while (str(arr) not in l):
            arr = np.roll(arr, 1)
            rot += 90
        d[i] = (l[str(arr)], rot)
    return d

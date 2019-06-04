import numpy as np
import pandas as pd
selling = pd.read_csv("../datafile/sellnum.csv", header=None, encoding='CP949')

def rank(input_data,id_data,arr):
    point = np.zeros(len(arr))
    location = np.zeros(len(input_data))

    for i in range(len(input_data)):
        for j in range(len(id_data[0])):
            if input_data[i] == id_data[0][j]:
                location[i] = j
                break

    for i in range(len(input_data)):
        for j in range(len(arr)):
            point[j] += arr[int(location[i])][j]

    best = np.zeros(10)
    m = 0
    min = 10000000

    point[4858] = 0
    point[167] = 0
    point[9847] = 0

    for i in location:
        point[int(i)] = 0

    for i in range(len(point)):
        if i < 10:
            if point[m] > point[i]:
                m = i
            best[i] = i

        else:
            if point[m] < point[i]:
                best[m] = i

                for j in range(len(best)):
                    if point[int(best[m])] > point[int(best[j])]:
                        m = j
            elif point[m] == point[i]:
                if selling[0][m] < selling[0][i]:
                    best[m] = i

    return best
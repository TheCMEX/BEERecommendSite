import pickle as pk
import numpy as np

with open('main/rec_sys/all_data_compressed', 'rb') as f:
    all_data_compressed = pk.load(f)

categories = list(all_data_compressed[0])
poses = list(all_data_compressed[5])
def pred_by_dists(good_beers, n_nearest = 2, metric = 'sum_sq'):
    out = []
    for i in range(len(good_beers)):
        n = 0
        if n_nearest[i] <= 5:
            continue
        elif n_nearest[i] > 5:
            n += 1
            if n_nearest[i] > 7:
                n += 1
            if n_nearest[i] == 10:
                n += 1
        out += dists_calc(all_data_compressed[0][good_beers[i]-1],n_nearest = n, metric = metric)
    return list(np.unique(out))


def dists_calc(category, n_nearest = 3, metric='sum_sq', position = [0,0]):
    if position == [0,0]:
        position = poses[categories.index(category)]
    cat = categories[0:categories.index(category)]+categories[categories.index(category)+1:]
    pos = poses[0:categories.index(category)]+poses[categories.index(category)+1:]
    res = []
    for i in range(len(pos)):
        if metric == "sum_sq": 
            dist = (sum([(pos[i][x]-position[x])**2 for x in range(len(pos[i]))]))**0.5
        if metric == 'max_dist':
            dist = (max([abs(pos[i][x]-position[x]) for x in range(len(pos[i]))]))
        if metric == 'city_dist':
            dist = (sum([abs(pos[i][x]-position[x]) for x in range(len(pos[i]))]))
        res.append([cat[i], dist])
    res = np.array(res)
    out = []
    for n in range(n_nearest):
        sub = res[res[:,1].argmin()][0]
        out.append(sub)
        res[res[:,1].argmin()] = ['kek','kek']
    return out

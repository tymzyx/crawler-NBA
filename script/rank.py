# -*- coding:utf-8
from db import db


def sohu_rank():
    mongo = db.connect_db()
    collection_player = mongo.sohu_players
    res_all = collection_player.find({})
    res_filters = {}
    for res in res_all:
        if '2017-2018' in res['career']['avg']:
            res_filters[res['playerId']] = res['career']['avg']['2017-2018']
    res_maps = {
        'score': [],
        'assist': [],
        'rebound': [],
        'steal': [],
        'block': []
    }
    rank_data = []
    for key in res_filters:
        for rank_type in res_maps:
            res_maps[rank_type].append(key + '|' + str(res_filters[key][rank_type]))
    for rank_type in res_maps:
        quick_sort(res_maps[rank_type], 0, len(res_maps[rank_type]) - 1)
        for i in range(100):
            player_id, data = res_maps[rank_type][i].split('|')
            rank_data.append({
                'playerId': player_id,
                'type': rank_type,
                'data': float(data)
            })
    collection_rank = mongo.rank
    collection_rank.insert_many(rank_data)
    print 'complete insert rank info'


def quick_sort(data, left, right):
    if left > right:
        return
    temp = float(data[left].split('|')[1])  # temp表示基准数
    i = left
    j = right
    while i != j:
        # 基准数位于最左边，从右边开始找
        while float(data[j].split('|')[1]) <= temp and i < j:
            j -= 1
        # 再找左边的
        while float(data[i].split('|')[1]) >= temp and i < j:
            i += 1
        # 交换两个数在列表中的位置
        if i < j:
            t = data[i]
            data[i] = data[j]
            data[j] = t
    # 最后归为基准数
    t = data[left]
    data[left] = data[i]
    data[i] = t

    quick_sort(data, left, i - 1)  # 通过递归急需处理左边的
    quick_sort(data, i + 1, right)  # 通过递归急需处理右边的


if __name__ == '__main__':
    sohu_rank()

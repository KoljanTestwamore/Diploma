from enum import Enum

import matplotlib.pyplot as plt
import math
from copy import deepcopy
import sys
import random
from xml.etree.ElementTree import Element, SubElement, Comment, tostring

from Network import Network
from visualization import prerender, visualize_n, save_plot

sys.setrecursionlimit(10000)


class Rule:
    def __init__(self, rule, param={}):
        self.rule = rule
        self.params = param


if __name__ == '__main__':
    nw = Network(12).fill_in_gaps().symmetrize().get_adjacent_stable_networks()
    # nodes[2] = [1,5,8]
    # nodes[4] = [5,9,12]
    # nodes[6] = [5,4,8,7,9,10,11]
    # nodes[11] = [12]
    adj = Network(5).get_adjacent_stable_networks()
    print(adj)
    while True:
        t_adj = []
        for network in adj:
            t_adj.extend(network.get_adjacent_stable_networks())
        if len(t_adj) == 0:
            break
        else:
            adj = t_adj

    # st_indices, hm, bl= nw.set_dict(nodes).fill_in_gaps().symmetrize()._get_stable_networks()
    # Network(st_indices['network']).visualize()
    # print(st_indices,'\n',hm,'\n',bl, Network.improving_path[20])

    ax = prerender(len(Network.stable_networks_non_dict[60].improving_path))
    for i in range(len(Network.stable_networks_non_dict[60].improving_path)):
        visualize_n(ax[i], Network.stable_networks_non_dict[60].improving_path[i]['network'],
                    filename="network" + str(i),
                    special_edge=Network.stable_networks_non_dict[60].improving_path[i]['edge']
                    )
    save_plot()

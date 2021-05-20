import math

import matplotlib.pyplot as plt

# contains everything needed for visualization
from utils import get_coords


def prerender(subplots):
    fig, ax = plt.subplots(subplots, figsize=(40, 40))
    plt.xscale('linear')
    plt.yscale('linear')
    return ax


def visualize_n(ax, network, filename="network", special_edge=()):
    dist = 20
    total_items = len(network)
    items = network.items()
    delta = 2 * math.pi / total_items

    temp = {}
    i = 0
    for node, _ in items:
        temp[node] = i
        i = i + 1
    i = 0
    drawn = []
    ax.axis('off')
    ax.set_box_aspect(1)
    special_edge_off = False
    # if (special_edge):
    #     network[special_edge[0]].append(special_edge[1])
    #     special_edge_off = True
    for node, connectors in items:
        x, y = get_coords(i, delta)
        for connector in connectors:
            spec = False
            if special_edge:
                if ((node == special_edge[0]) and (connector == special_edge[1])) or (
                        (node == special_edge[1]) and (connector == special_edge[0])):
                    spec = True
            if not (temp[connector] in drawn):
                xc, yc = get_coords(temp[connector], delta)
                if spec:
                    if special_edge_off:
                        ax.plot([x, xc], [y, yc], zorder=1, linewidth=4, dash_capstyle='round', color="#FFC0CB")
                    else:
                        ax.plot([x, xc], [y, yc], zorder=1, linewidth=4, dash_capstyle='round')
                else:
                    ax.plot([x, xc], [y, yc], linewidth=1, zorder=1)
        i = i + 1
    i = 0
    for node, connectors in items:
        x, y = get_coords(i, delta)
        circ = plt.Circle((x, y), 1.5, color='black', zorder=2)
        ax.add_patch(circ)
        ax.text(x - 0.5, y - 0.5, node, color='w', zorder=3)
        i = i + 1


def save_plot(filename="network"):
    plt.savefig(filename)


def visualize(network, filename="network", special_edge=()):
    dist = 20
    total_items = len(network)
    items = network.items()
    delta = 2 * math.pi / total_items

    temp = {}
    i = 0
    for node, _ in items:
        temp[node] = i
        i = i + 1
    i = 0
    drawn = []
    plt.cla()
    plt.axis('off')
    for node, connectors in items:
        x, y = get_coords(i, delta)
        for connector in connectors:
            spec = False
            if len(special_edge) > 0:
                if ((node == special_edge[0]) and (connector == special_edge[1])) or (
                        (node == special_edge[1]) and (connector == special_edge[0])):
                    spec = True
            if not (temp[connector] in drawn):
                xc, yc = get_coords(temp[connector], delta)
                if spec:
                    plt.plot([x, xc], [y, yc], zorder=1, linewidth=4, dash_capstyle='round')
                else:
                    plt.plot([x, xc], [y, yc], linewidth=1, zorder=1)
        circ = plt.Circle((x, y), 1.5, color='black', zorder=2)
        plt.gca().add_patch(circ)
        plt.text(x - 0.5, y - 0.5, node, color='w', zorder=3)
        drawn.append(node)
        i = i + 1
    plt.savefig(filename)

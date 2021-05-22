import math
from copy import deepcopy
from random import random
import matplotlib.pyplot as plt

from utils import get_coords, get_unique_keys, parse_dict


class Network:
    history = []
    stable_networks = []
    stable_networks_non_dict = []
    # stores data as dicts with
    # {
    #     network: dict,
    #     edge: [node1, node2]
    # }
    improving_path = []
    dead_end_networks = []
    inspected_networks = []

    def __init__(self, param, symmetrize=False, improving_path=[], **args):
        self.current_plot = 0
        if isinstance(param, dict):
            players = get_unique_keys(param)
            self.network = parse_dict(param)
        elif isinstance(param, int):
            players = list(range(0, param))
            self.network = {i: [] for i in [*range(0, param)]}
        else:
            self.network = {}
        if symmetrize:
            self.symmetrize()
        self.players_amount = len(players)
        # decoder is used for output. inner indexes are always integer but
        # since we may want to store actual string names for players
        # we can decode indexes into strings (and back if we really want to)
        self.decoder = lambda x: players[x]
        self.improving_path = deepcopy(improving_path)
        self.rule = args.get('rule', lambda x: 0)

    def set_improving_path(self, improving_path):
        self.improving_path = improving_path

    def set_stable(self):
        self.stable = True

    def get_dict(self):
        return self, deepcopy(self.network)

    def print_dict(self):
        print(self.network)
        return self

    def set_dict(self, param):
        if isinstance(param, dict):
            self.network = param
        elif isinstance(param, int):
            self.network = {i: [] for i in [*range(0, param)]}
        else:
            self.network = {}
        print(self.network, type(param))
        return self

    def add_node(self, x, y):
        _, nodes = self.get_dict()
        nodes[x].append(y)
        nodes[y].append(x)
        return Network(nodes)

    def remove_node(self, x, y):
        _, nodes = self.get_dict()
        nodes[x].remove(y)
        nodes[y].remove(x)
        nw = Network(nodes)
        _, deca = nw.get_dict()
        return Network(nodes)

    def symmetrize(self):
        network = self.network
        temp = {}
        items = network.items()
        for key, connectors in items:
            temp[key] = set(connectors)
        for key, connectors in items:
            for connector in connectors:
                if connector in temp:
                    temp[connector].add(key)
                else:
                    temp[connector] = set()
        for key, item in temp.items():
            temp[key] = list(item)
        self.network = temp
        return self

    def fill_in_gaps(self):
        temp = {}
        network = self.network
        items = network.items()
        for key, connectors in items:
            temp[key] = connectors
            for connector in connectors:
                if connector in temp:
                    continue
                else:
                    temp[connector] = []
        self.network = temp
        return self

    def next_plot(self, title="", activate_axis=False):
        self.fig = plt.figure(self.current_plot)
        if not activate_axis:
            plt.axis("off")
        plt.xlim(-25., 25.)
        plt.ylim(-25., 25.)
        self.current_plot = self.current_plot + 1
        return self

    def _connection_exists(self, x, y):
        if y in self.network[x]:
            return True
        if x in self.network[y]:
            return True
        return False

    def visualize(self, filename="network"):
        dist = 20
        total_items = len(self.network)
        items = self.network.items()
        delta = 2 * math.pi / total_items

        temp = {}
        i = 0
        for node, _ in items:
            temp[node] = i
            i = i + 1
        i = 0
        drawn = []
        for node, connectors in items:
            print(node)
            x, y = get_coords(i, delta)
            for connector in connectors:
                if not (temp[connector] in drawn):
                    xc, yc = get_coords(temp[connector], delta)
                    plt.plot([x, xc], [y, yc], zorder=1)
            circ = plt.Circle((x, y), 1.5, color='black', zorder=2)
            plt.gca().add_patch(circ)
            plt.text(x - 0.5, y - 0.5, node, color='w', zorder=3)
            drawn.append(node)
            i = i + 1
        plt.savefig(filename)
        return self

    # generates XML file based on network graph
    def generate_xml(self):
        return self

    def get_adjacent_stable_networks(self):
        items = self.network.items()
        temp = {}
        for node, _ in items:
            temp[node] = list(self.network.keys())
            temp[node].remove(node)

        checked = []
        adjacent_improved = []
        stable = True
        better_network_exists = False

        if self.network not in Network.inspected_networks:
            Network.inspected_networks.append(self.network)
        else:
            return []

        for node1, connectors in temp.items():
            old_node1_value = self._node_yield(node1)
            for node2 in connectors:
                if node2 in checked:
                    continue
                old_node2_value = self._node_yield(node2)

                # check whether edge (node1, node2) exists.
                # if it exists, we check condition 1,
                #     that is we can not remove that edge
                #     without lowering any of expected nodes value.
                # else we check condition 2,
                #     that is we can not add that edge
                #     without lowering any of expected nodes value.
                new_network = None
                if (node1 in self.network[node2]) or (node2 in self.network[node1]):
                    # condition 1
                    new_network = self.remove_node(node1, node2)
                else:
                    # condition 2
                    new_network = self.add_node(node1, node2)
                new_network.symmetrize()
                new_node1_value = new_network._node_yield(node1)
                new_node2_value = new_network._node_yield(node2)

                if (new_node1_value > old_node2_value) and (new_node2_value > old_node2_value):
                    stable = False

                    cycled = False
                    for i in range(len(self.improving_path)):
                        if new_network.network in Network.inspected_networks:
                            cycled = True
                            break

                    if not cycled:
                        new_network.set_improving_path([*self.improving_path, {
                            'network': self.network,
                            'edge': (node1, node2)
                        }])
                        adjacent_improved.append(new_network)
                        better_network_exists = False
                    else:
                        continue
            checked.append(node1)
        if (len(adjacent_improved) == 0) and not stable:
            Network.dead_end_networks.append(self.network)
        if stable:
            Network.stable_networks.append(self.network)
            Network.stable_networks_non_dict.append(self)
            return []
        return adjacent_improved

    def _get_stable_networks(self):
        items = self.network.items()
        temp = {}
        for node, _ in items:
            temp[node] = list(self.network.keys())
            temp[node].remove(node)

        checked = []
        indices_similar = []

        stable = True

        better_network = None

        if self.network in Network.dead_end_networks:
            return Network(self.improving_path[-1], improving_path=self.improving_path[0:-1])._get_stable_networks()

        for node1, connectors in temp.items():
            old_node1_value = self._node_yield(node1)
            for node2 in connectors:
                if node2 in checked:
                    continue
                old_node2_value = self._node_yield(node2)

                # check whether edge (node1, node2) exists.
                # if it exists, we check condition 1,
                #     that is we can not remove that edge
                #     without lowering any of expected nodes value.
                # else we check condition 2,
                #     that is we can not add that edge
                #     without lowering any of expected nodes value.
                new_network = None
                if (node1 in self.network[node2]) or (node2 in self.network[node1]):
                    # condition 1
                    new_network = self.remove_node(node1, node2)
                else:
                    # condition 2
                    new_network = self.add_node(node1, node2)

                new_node1_value = new_network._node_yield(node1)
                new_node2_value = new_network._node_yield(node2)

                if (new_node1_value > old_node2_value) and (new_node2_value > old_node2_value):
                    stable = False

                    cycled = False
                    for i in range(len(self.improving_path)):
                        if new_network.network == self.improving_path[i]['network']:
                            cycled = True
                            break
                        elif new_network.network in Network.dead_end_networks:
                            cycled = True
                            break
                    if not cycled:
                        better_network = new_network
                        print((node1, node2))
                        self.improving_path.append({
                            'network': better_network.network,
                            'edge': (node1, node2)
                        })
                        break
            if not stable:
                break
            checked.append(node1)

        if not stable:
            if better_network:
                return better_network._get_stable_networks()
            else:
                Network.dead_end_networks.append(self.network)
                return Network(self.improving_path[-1]['network'],
                               improving_path=self.improving_path())._get_stable_networks()
        else:
            res = []
            for item in indices_similar:
                res.append(Network.improving_path[i])
            return Network.improving_path[-1], res, indices_similar

    def _efficiency(self):
        result = 0
        for node, _ in self.network.items():
            result = result + self._node_yield(node)
        return result

    def _node_yield(self, x):
        ni = len(self.network[x])
        if ni == 0:
            return 0
        result = 1 / ni
        for connector in self.network[x]:
            nj = len(self.network[connector])
            if nj == 0:
                continue
            result = result + 1 / nj + 1 / (ni * nj)
        return result

    # changes network's nodes order
    def generate_mixer(self, seed):
        network_keys = self.network.keys()
        mixed_indexes = random.sample(network_keys, k=network_keys)
        return lambda index: mixed_indexes[index]


class Configuration:
    def __int__(self, graph, parent_network):
        self.network = parent_network
        self.graph = graph

    def __eq__(self, other):
        return self.network == other.network and self.graph == other.graph

    def value(self):
        result = 0
        for node in range(0, self.network.players_amount):
            result = result + self.network.rule(node, self.graph)
        return result

    def xml(self, title=""):
        # generates xml file. used for gephi
        # TODO: implementation
        return

import os
import time

import networkx as nx
import matplotlib.pyplot as plt


MAX_NODES = None
MAX_PERIMETER = 19
MAX_PENTAGONS = 5


class Graph:
    def __init__(self, G=None, border=[], borderDeg2=0, penta=[], penta_n=0):
        self.G = G.copy() if G else nx.Graph()
        self.border = border[:]
        self.borderDeg2 = borderDeg2
        self.penta = penta[:]
        self.penta_n = penta_n

    def copy(self):
        return Graph(self.G, self.border, self.borderDeg2,
                     self.penta, self.penta_n)

    def add_pentagon(self, border):
        self.penta += border
        self.penta_n += 1

    def add_path(self, start, end, length, penta=False):
        n = len(self.G.nodes())
        newBorder = [self.border[start]]
        newBorder += list(range(n, n + length - 1))
        newBorder.append(self.border[end])
        self.G.add_path(newBorder)
        if end > start:
            self.border = self.border[:start] + newBorder[:-1] + self.border[end:]
        else:
            self.border = self.border[end:start] + newBorder[:-1]
        self.borderDeg2 += len(newBorder) - 4
        if penta:
            self.add_pentagon(newBorder)

    def is_isomorphic(self, lst):
        if type(lst) != list: lst = [lst]

        for g in lst:
            if len(self.border) == len(g.border) and \
               len(self.G.nodes()) == len(g.G.nodes()) and \
               self.penta_n == g.penta_n and \
               self.borderDeg2 == g.borderDeg2 and \
               nx.is_isomorphic(self.G, g.G):
                   return True

        return False

    def free_pairs(self):
        degs = self.G.degree(self.border)
        b_len = len(self.border)
        border2 = [x for x in range(b_len) if degs[self.border[x]] == 2]
        b2_len = len(border2)
        return [(border2[x], border2[(x+1) % b2_len]) for x in range(b2_len)]

    def plot(self, path):
        nx.draw_spectral(self.G)
        plt.savefig(path)
        plt.clf()

    def __str__(self):
        return str(self.G.edges())


def hexagon():
    g = Graph(border=[0, 1, 2, 3, 4, 5], borderDeg2=6)
    g.G.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)])
    return g


def process_graph(graph):
    res = []

    for start, end in graph.free_pairs():
        dist = end - start
        if dist < 0:
            dist += len(graph.border)

        if dist < 6:
            new = graph.copy()
            new.add_path(start, end, 6 - dist)
            res.append(new)

        if dist < 5 and graph.penta_n < MAX_PENTAGONS:
            if start < end:
                penta_check = graph.border[start:end+1]
            else:
                penta_check = graph.border[end:] + graph.border[:start+1]

            if len(set(penta_check) & set(graph.penta)) == 0:
                new = graph.copy()
                new.add_path(start, end, 5 - dist, penta=True)
                res.append(new)

    return res


def generate_graphs():
    print("Generating graphs...")
    queue, res = [hexagon()], [hexagon()]

    while len(queue):
        graph = queue.pop(0)

        for g in process_graph(graph):
            if MAX_PERIMETER and len(g.border) > MAX_PERIMETER: continue
            if MAX_NODES and len(g.G.nodes()) > MAX_NODES: continue
            if g.is_isomorphic(res): continue

            queue.append(g)
            res.append(g)

        print("Queue length: {} Total: {}  \r".format(len(queue), len(res)), end="")

    return res


start_time = time.time()
graphs = generate_graphs()
print("Graphs found: {}".format(len(graphs)))
i = 0
for graph in graphs:
    print("Plotting... {}\r".format(i+1), end="")
    graph.plot(os.path.join('results', 'graph_{}.png'.format(i)))
    i += 1
duration = round(time.time()-start_time)
print("\nTime: {}min {}s".format(round(duration//60), duration%60))

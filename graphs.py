import networkx as nx
from concurrent import futures


N_OF_WORKERS = 8
MAX_NODES = 78
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

    def add_path(self, start, end, length):
        n = len(self.G.nodes())
        newBorder = [self.border[start]]
        newBorder += list(range(n, n + length - 1))
        newBorder.append(self.border[end])
        self.G.add_path(newBorder)
        self.border = self.border[:start] + newBorder[:-1] + \
            self.border[end:] if end > start else []
        self.borderDeg2 += len(newBorder) - 4


def hexagon():
    g = Graph(border=[0, 1, 2, 3, 4, 5], borderDeg2=6)
    g.G.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)])
    return g


def process_graph(graph):
    res = []

    border = graph.border
    borderDeg = graph.G.degree(border)
    border2 = [x for x in range(len(border)) if borderDeg[border[x]] == 2]
    b_len = len(border)
    b2_len = len(border2)
    pairs = [(border2[x], border2[(x+1) % b2_len]) for x in range(b2_len)]

    for pair in pairs:
        dist = pair[1] - pair[0]
        if dist < 0:
            dist += b_len

        if dist < 6:
            new = graph.copy()
            new.add_path(pair[0], pair[1], 6 - dist)
            res.append(new)

        if dist < 5:
            new = graph.copy()
            new.add_path(pair[0], pair[1], 5 - dist)
            res.append(new)

    return res


def generate_graphs():
    queue = [hexagon()]
    res = []

    while len(queue):
        graph = queue.pop(0)

        for g in process_graph(graph):
            if len(g.G.nodes()) == MAX_NODES:
                res.append(g)
            if len(g.G.nodes()) < MAX_NODES:
                queue.append(g)

    print(len(res))

    with futures.ProcessPoolExecutor(max_workers=N_OF_WORKERS) as executor:
        pass


generate_graphs()

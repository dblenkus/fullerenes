import networkx as nx
import matplotlib.pyplot as plt

class graf:
    def __init__(self):
        self.G = nx.Graph()
        self.border = []
        self.penta = []
        self.penta_n = 0
        self.bodredDeg2 = 0

def iso():
    for i in lst[:-1]:
        if (len(i.border) == len(lst[-1].border)) and (len(i.G.nodes()) == len(lst[-1].G.nodes())) and (i.penta_n == lst[-1].penta_n) and (i.borderDeg2 == lst[-1].borderDeg2):
            if nx.is_isomorphic(i.G,lst[-1].G):
                return True

    return False



lst=[graf()]
lst[0].G.add_edges_from([(0,1),(1,2),(2,3),(3,4),(4,5),(5,0)])
lst[0].border = [0,1,2,3,4,5]
lst[0].borderDeg2 = 6

i = 0

while i<len(lst):

    border = lst[i].border
    borderDeg = lst[i].G.degree(lst[i].border)
    deg2 = [x for x in range(len(border)) if borderDeg[border[x]]==2]

    for j in range(len(deg2)-1):
        if deg2[j+1] - deg2[j] < 6:
            newBorder = [border[deg2[j]]]
            newBorder += list(range(len(lst[i].G.nodes()) , len(lst[i].G.nodes()) + 6 - 1 - (deg2[j+1] - deg2[j])))
            newBorder.append(border[deg2[j+1]])
            lst.append(graf())
            lst[-1].G = lst[i].G.copy()
            lst[-1].G.add_path(newBorder)
            lst[-1].border = lst[i].border[:deg2[j]] + newBorder + lst[i].border[deg2[j+1]+1:]
            lst[-1].penta = lst[i].penta
            lst[-1].penta_n = lst[i].penta_n
            lst[-1].borderDeg2 = lst[i].borderDeg2 + len(newBorder) - 4
            if (iso()) or (len(lst[-1].border)>19):
                lst.pop()

        if deg2[j+1] - deg2[j] < 5:
            newBorder = [border[deg2[j]]]
            newBorder += list(range(len(lst[i].G.nodes()) , len(lst[i].G.nodes()) + 5 - 1 - (deg2[j+1] - deg2[j])))
            newBorder.append(border[deg2[j+1]])
            if (lst[i].penta_n<5) and (len(set(newBorder + border[deg2[j]:deg2[j+1]]) & set(lst[i].penta)) == 0):
                lst.append(graf())
                lst[-1].G = lst[i].G.copy()
                lst[-1].G.add_path(newBorder)
                lst[-1].border = lst[i].border[:deg2[j]] + newBorder + lst[i].border[deg2[j+1]+1:]
                lst[-1].penta = lst[i].penta + newBorder
                lst[-1].penta_n = lst[i].penta_n + 1
                lst[-1].borderDeg2 = lst[i].borderDeg2 + len(newBorder) - 4
                if (iso()) or (len(lst[-1].border)>19):
                    lst.pop()

    if len(border) - deg2[-1] + deg2[0] < 6:
        newBorder = [border[deg2[-1]]]
        newBorder += list(range(len(lst[i].G.nodes()) , len(lst[i].G.nodes()) + 6 - 1 - (len(border) - deg2[-1] + deg2[0])))
        newBorder.append(border[deg2[0]])
        lst.append(graf())
        lst[-1].G = lst[i].G.copy()
        lst[-1].G.add_path(newBorder)
        lst[-1].border = lst[i].border[deg2[0]:deg2[-1]] + newBorder[:-1]
        lst[-1].penta = lst[i].penta
        lst[-1].penta_n = lst[i].penta_n
        lst[-1].borderDeg2 = lst[i].borderDeg2 + len(newBorder) - 4
        if (iso()) or (len(lst[-1].border)>19):
            lst.pop()

    if len(border) - deg2[-1] + deg2[0] < 5:
        newBorder = [border[deg2[-1]]]
        newBorder += list(range(len(lst[i].G.nodes()) , len(lst[i].G.nodes()) + 5 - 1 - (len(border) - deg2[-1] + deg2[0])))
        newBorder.append(border[deg2[0]])
        if (lst[i].penta_n<5) and (len(set(newBorder + border[:deg2[0]] + border [deg2[-1]:]) & set(lst[i].penta)) == 0):
            lst.append(graf())
            lst[-1].G = lst[i].G.copy()
            lst[-1].G.add_path(newBorder)
            lst[-1].border = lst[i].border[deg2[0]:deg2[-1]] + newBorder[:-1]
            lst[-1].penta = lst[i].penta + newBorder
            lst[-1].penta_n = lst[i].penta_n + 1
            lst[-1].borderDeg2 = lst[i].borderDeg2 + len(newBorder) - 4
            if (iso()) or (len(lst[-1].border)>19):
                lst.pop()

    i += 1


res = 0
for i, graph in enumerate(lst):
    nx.draw_spectral(graph.G)
    plt.savefig("graf_"+ str(i) +".png")
    plt.clf()
    print graph.G.nodes()
    for a in [x for x in graph.G.nodes() if graph.G.degree(x)==3]:
        tmp = 999
        for b in [x for x in graph.border if graph.G.degree(x)==2]:
            tmp = min(tmp, nx.shortest_path_length(graph.G,source=a,target=b))
        if (tmp > res) and(not(tmp == 999)):
            res, res_i = tmp, i

print res, res_i


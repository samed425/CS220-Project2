from z3 import *

import functools


def MySum(lst):
    return functools.reduce(lambda a, b: a + b, lst, 0)


def read_graph(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    num_vertices, num_edges, num_colors = map(int, lines[0].split())
    vertices = list(range(1, num_vertices + 1))
    graph = {v: set() for v in vertices}
    for line in lines[1:num_edges+1]:
        u, v = map(int, line.split())
        graph[u].add(v)
        graph[v].add(u)
    edges = [(u, v) for u in range(1, num_vertices + 1) for v in graph[u] if u < v]

    affinity_edges = []
    for line in lines[num_edges + 1:]:
        x, y = map(int, line.split())
        affinity_edges.append((x, y))
    return vertices, edges, affinity_edges


def main(V, E, A, k1, k2):
    vertices = len(V)
    X = [Int("x_%s" % i) for i in range(vertices)]
    Y = [Int("y_%s" % i) for i in range(len(A))]
    coloring = [And(0 <= X[i], X[i] < k1) for i in range(vertices)]
    adjacent = [Distinct(X[i-1], X[j-1]) for i, j in E]
    affinity = [(Y[i] == (X[A[i][0]-1] == X[A[i][1]-1])) for i in range(len(A))]
    s = Solver()
    s.add(coloring + adjacent + affinity)
    s.add(MySum(Y) >= k2)

    if s.check() == sat:
        m = s.model()
        r = [m.evaluate(X[i]) for i in range(vertices)]
        #p = [m.evaluate(Y[i]) for i in range(len(A))]
        #for i, j in E:
        #    print("Nodes: ", i, j, "Colors: ", r[i-1], r[j-1])
        #print(r)
        #print(p)

        file = open(r"output.txt", "w+")
        file.write("Yes")
        file.write("\n")
        for i in range(len(r)):
            file.write(str(r[i]))
            file.write("\n")
        file.close()
    else:
        file = open(r"output.txt", "w+")
        file.write("No")
        file.close()
        #print("failed to solve")

    return

file_path = ("Sample Inputs/sample_1.txt")
V, E, A = read_graph(file_path)
main(V, E, A, 12, 1)

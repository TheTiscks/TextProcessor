import sys
import numpy as np


def read_graph(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        size, is_directed = map(int, lines[0].strip().split()[:2])
        matrix = []
        for i in range(1, size + 1):
            row = list(map(int, lines[i].strip().split()))
            matrix.append(row)
    return matrix, size, is_directed


def get_edges(graph, is_directed):
    edges = {}
    idx = 0
    for i in range(len(graph)):
        for j in range(len(graph[i])):
            if graph[i][j] == 1:
                if is_directed:
                    edges[(i, j)] = idx
                    idx += 1
                else:
                    if (j, i) not in edges:
                        edges[(i, j)] = idx
                        idx += 1
    return edges


def cycle_to_edges(cycle, is_directed):
    edges = []
    for k in range(len(cycle) - 1):
        u, v = cycle[k], cycle[k + 1]
        edges.append((u, v))
    return edges


def build_incidence_matrix(cycles, edges, is_directed):
    num_edges = len(edges)
    matrix = []
    for cycle in cycles:
        row = [0] * num_edges
        cycle_edges = cycle_to_edges(cycle, is_directed)
        for (u, v) in cycle_edges:
            if (u, v) in edges:
                row[edges[(u, v)]] = 1
            elif not is_directed and (v, u) in edges:
                row[edges[(v, u)]] = 1
        matrix.append(row)
    return np.array(matrix, dtype=int)


def gaussian_elimination(matrix):
    matrix = matrix.copy()
    rows, cols = matrix.shape
    rank = 0
    pivots = []

    for col in range(cols):
        pivot = -1
        for row in range(rank, rows):
            if matrix[row, col] == 1:
                pivot = row
                break
        if pivot == -1:
            continue

        matrix[[rank, pivot]] = matrix[[pivot, rank]]
        for row in range(rows):
            if row != rank and matrix[row, col] == 1:
                matrix[row] ^= matrix[rank]
        pivots.append(col)
        rank += 1
    return rank, matrix[:rank]


def remove_dependent_cycles(cycles, edges, is_directed):
    if not cycles:
        return []

    matrix = build_incidence_matrix(cycles, edges, is_directed)
    rank, _ = gaussian_elimination(matrix)
    return cycles[:rank]


def dfs(u, graph, visited, parent, cycles, depth, is_directed):
    visited[u] = True
    for v in range(len(graph)):
        if graph[u][v] == 0:
            continue

        if not visited[v]:
            parent[v] = u
            depth[v] = depth[u] + 1
            dfs(v, graph, visited, parent, cycles, depth, is_directed)
        elif (is_directed or v != parent[u]) and depth[v] < depth[u]:
            cycle = []
            current = u
            path = [current]
            valid = True

            while current != v:
                next_node = parent[current]
                if is_directed and graph[current][next_node] == 0:
                    valid = False
                    break
                path.append(next_node)
                current = next_node

            if valid:
                if is_directed:
                    cycle = path + [v]
                else:
                    if graph[path[-1]][u] == 1 or graph[u][path[-1]] == 1:
                        cycle = path + [u]
                if not is_directed:
                    cycle_sorted = sorted(cycle[:-1])
                    cycle_sorted.append(cycle_sorted[0])
                    cycle = cycle_sorted
                if cycle not in cycles:
                    cycles.append(cycle)


def find_cycles(graph, size, is_directed):
    visited = [False] * size
    parent = [-1] * size
    depth = [0] * size
    cycles = []

    for i in range(size):
        if not visited[i]:
            dfs(i, graph, visited, parent, cycles, depth, is_directed)

    edges = get_edges(graph, is_directed)
    independent_cycles = remove_dependent_cycles(cycles, edges, is_directed)
    return independent_cycles


def save_result(input_file, matrix, cycles, is_directed):
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(f"{len(matrix)} {1 if is_directed else 0}\n")
        for row in matrix:
            f.write(' '.join(map(str, row)) + '\n')

        f.write("<Text>\n")
        f.write(f"Найдено независимых циклов: {len(cycles)}\n")
        for i, cycle in enumerate(cycles, 1):
            separator = " → " if is_directed else " — "
            cycle_str = separator.join(map(str, cycle))
            f.write(f"Цикл {i}: {cycle_str}\n")


def main(input_file):
    graph, size, is_directed = read_graph(input_file)
    cycles = find_cycles(graph, size, is_directed)
    save_result(input_file, graph, cycles, is_directed)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
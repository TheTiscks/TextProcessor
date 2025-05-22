import sys
from collections import deque


def find_path_in_tree(parent, u, v):
    path_u = []
    current = u
    while current != -1:
        path_u.append(current)
        current = parent[current]

    path_v = []
    current = v
    while current != -1:
        path_v.append(current)
        current = parent[current]

    i = len(path_u) - 1
    j = len(path_v) - 1
    while i >= 0 and j >= 0 and path_u[i] == path_v[j]:
        i -= 1
        j -= 1
    lca_index = i + 1 if i + 1 < len(path_u) else 0
    lca = path_u[lca_index]

    path = path_u[:lca_index + 1][::-1] + path_v[:j + 1][::-1][1:]
    return path


def find_cycle_basis(graph):
    n = len(graph)
    parent = [-1] * n
    visited = [False] * n
    non_tree_edges = []
    cycles = []

    queue = deque([0])
    visited[0] = True
    while queue:
        u = queue.popleft()
        for v in range(n):
            if graph[u][v]:
                if not visited[v]:
                    visited[v] = True
                    parent[v] = u
                    queue.append(v)
                elif parent[u] != v and parent[v] != u:
                    non_tree_edges.append((u, v))

    for u, v in non_tree_edges:
        path = find_path_in_tree(parent, u, v)
        cycle = path + [u]
        unique_cycle = sorted(set(cycle))
        if unique_cycle not in cycles:
            cycles.append(unique_cycle)

    return sorted(cycles, key=lambda x: (len(x), x)), False


def main(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        size = int(lines[0].strip())
        matrix = []
        for i in range(1, size + 1):
            row = list(map(int, lines[i].strip().split()))
            matrix.append(row)
    answer, directed = find_cycle_basis(matrix)
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(f"{size}\n")
        for i in range(size):
            f.write(' '.join(map(str, matrix[i])) + '\n')
        f.write("<Text>\n")
        for cycle in sorted(answer, key=lambda x: (len(x), x)):
            cycle_str = "{" + ", ".join(map(str, cycle)) + "}\n"
            f.write(cycle_str)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
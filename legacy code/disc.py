import sys
from collections import deque


def find_cycle_basis(graph):
    n = len(graph)
    visited = [False] * n
    parent = [-1] * n
    edge_used = {}  # Хранит рёбра остовного дерева
    non_tree_edges = []
    cycles = []

    # Построение остовного дерева с помощью BFS
    for start in range(n):
        if not visited[start]:
            queue = deque([start])
            visited[start] = True
            while queue:
                u = queue.popleft()
                for v in range(n):
                    if graph[u][v] and not visited[v]:
                        visited[v] = True
                        parent[v] = u
                        edge_used[(min(u, v), max(u, v))] = True
                        queue.append(v)
                    elif graph[u][v] and parent[u] != v and (min(u, v), max(u, v)) not in edge_used:
                        non_tree_edges.append((u, v))

    # Находим фундаментальные циклы для каждого недревесного ребра
    for u, v in non_tree_edges:
        # Находим путь от u до v в дереве
        path_u = []
        path_v = []
        current = u
        while current != -1:
            path_u.append(current)
            current = parent[current]
        current = v
        while current != -1:
            path_v.append(current)
            current = parent[current]
        # Находим общего предка
        i = len(path_u) - 1
        j = len(path_v) - 1
        while i >= 0 and j >= 0 and path_u[i] == path_v[j]:
            i -= 1
            j -= 1
        # Собираем цикл
        cycle = path_u[:i + 1] + path_v[j + 1::-1]
        cycle_edges = set()
        for i in range(len(cycle) - 1):
            a, b = sorted((cycle[i], cycle[i + 1]))
            cycle_edges.add((a, b))
        # Добавляем недревесное ребро
        a, b = sorted((u, v))
        cycle_edges.add((a, b))
        cycles.append(cycle_edges)

    # Преобразуем циклы в множества вершин
    basis = []
    for cycle in cycles:
        vertices = set()
        for a, b in cycle:
            vertices.add(a)
            vertices.add(b)
        basis.append(sorted(vertices))

    # Удаляем дубликаты
    unique_basis = []
    seen = set()
    for cycle in basis:
        t = tuple(cycle)
        if t not in seen:
            seen.add(t)
            unique_basis.append(cycle)
    return unique_basis, False


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
import sys
from collections import deque


def find_cycle_basis(graph):
    n = len(graph)
    parent = [-1] * n
    visited = [False] * n
    edge_used = set()
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
                    if graph[u][v]:
                        if not visited[v]:
                            visited[v] = True
                            parent[v] = u
                            edge_used.add((min(u, v), max(u, v)))
                            queue.append(v)
                        elif (min(u, v), max(u, v)) not in edge_used and parent[u] != v:
                            non_tree_edges.append((u, v))

    # Построение дерева в виде списка смежности
    tree = [[] for _ in range(n)]
    for v in range(n):
        if parent[v] != -1:
            u = parent[v]
            tree[u].append(v)
            tree[v].append(u)

    # Поиск пути между вершинами в дереве через BFS
    def bfs_path(start, end):
        visited_path = [False] * n
        queue = deque()
        queue.append((start, [start]))
        visited_path[start] = True
        while queue:
            node, path = queue.popleft()
            if node == end:
                return path
            for neighbor in tree[node]:
                if not visited_path[neighbor]:
                    visited_path[neighbor] = True
                    queue.append((neighbor, path + [neighbor]))
        return None

    # Обработка недревесных рёбер
    for u, v in non_tree_edges:
        path = bfs_path(u, v)
        if path:
            cycle = path + [u]
            # Убираем повторяющиеся вершины (если есть)
            unique_cycle = []
            seen = set()
            for node in cycle:
                if node not in seen:
                    seen.add(node)
                    unique_cycle.append(node)
            if len(unique_cycle) >= 3:
                cycles.append(sorted(unique_cycle))

    # Удаление дубликатов и фильтрация базиса
    basis = []
    seen = set()
    # Сортировка циклов по длине для обработки от меньших к большим
    cycles.sort(key=lambda x: len(x))
    for cycle in cycles:
        cycle_tuple = tuple(sorted(cycle))
        if cycle_tuple not in seen:
            # Проверяем, не покрывается ли цикл уже существующими
            is_independent = True
            for existing in seen:
                if set(existing).issubset(cycle_tuple):
                    is_independent = False
                    break
            if is_independent:
                seen.add(cycle_tuple)
                basis.append(cycle)

    return sorted(basis, key=lambda x: (len(x), x)), False


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
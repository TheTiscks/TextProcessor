import sys
from collections import deque

def find_cycle_basis(graph):
    n = len(graph)
    parent = [-1] * n
    visited = [False] * n
    edge_used = set()
    non_tree_edges = []
    cycles = []

    # Построение остовного дерева через DFS
    def dfs(u):
        visited[u] = True
        for v in range(n):
            if graph[u][v]:
                edge = (min(u, v), max(u, v))
                if not visited[v]:
                    parent[v] = u
                    edge_used.add(edge)
                    dfs(v)
                elif parent[u] != v and edge not in edge_used:
                    non_tree_edges.append((u, v))

    # Запуск DFS для построения остовного дерева
    for start in range(n):
        if not visited[start]:
            dfs(start)

    # Построение дерева в виде списка смежности
    tree = [[] for _ in range(n)]
    for u, v in edge_used:
        tree[u].append(v)
        tree[v].append(u)

    # Поиск пути между вершинами u и v в остовном дереве через BFS
    def bfs_path(start, end):
        visited_path = [False] * n
        queue = deque([(start, [start])])
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

    # Обработка недревесных рёбер для формирования циклов
    for u, v in non_tree_edges:
        path = bfs_path(u, v)
        if path:
            cycle = path
            # Добавляем ребро (u, v) для замыкания цикла
            if cycle[0] != v:
                cycle = [v] + cycle
            if cycle[-1] != u:
                cycle.append(u)
            # Удаляем дубликаты вершин, сохраняя порядок
            unique_cycle = []
            seen = set()
            for node in cycle:
                if node not in seen:
                    seen.add(node)
                    unique_cycle.append(node)
            if len(unique_cycle) >= 3:
                cycles.append(sorted(unique_cycle))

    # Фильтрация для получения минимального базиса циклов
    basis = []
    seen_cycles = set()
    cycles.sort(key=lambda x: len(x))
    for cycle in cycles:
        cycle_tuple = tuple(cycle)
        if cycle_tuple not in seen_cycles:
            # Проверяем, что цикл не является комбинацией других (упрощённая проверка)
            is_independent = True
            cycle_set = set(cycle)
            for existing in seen_cycles:
                existing_set = set(existing)
                # Если текущий цикл содержит вершины другого цикла и длиннее, он может быть зависимым
                if len(cycle) > len(existing) and len(cycle_set.intersection(existing_set)) >= len(existing_set) - 1:
                    is_independent = False
                    break
            if is_independent:
                seen_cycles.add(cycle_tuple)
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
import sys
from collections import deque


def find_cycle_basis(graph):
    n = len(graph)
    parent = [-1] * n  # Массив родителей для построения дерева
    visited = [False] * n  # Отмечаем посещённые вершины
    non_tree_edges = []  # Список рёбер, не входящих в остовное дерево
    cycles = []  # Список циклов

    # BFS для построения остовного дерева
    queue = deque([0])  # Начинаем с вершины 0, предполагая, что граф связный
    visited[0] = True
    while queue:
        u = queue.popleft()
        for v in range(n):
            if graph[u][v]:  # Если есть ребро
                if not visited[v]:  # Новая вершина
                    visited[v] = True
                    parent[v] = u
                    queue.append(v)
                elif parent[u] != v and parent[v] != u:  # Нетривиальное ребро
                    non_tree_edges.append((u, v))

    # Находим циклы для каждого нетривиального ребра
    for u, v in non_tree_edges:
        # Путь от u до корня
        path_u = []
        current = u
        while current != -1:
            path_u.append(current)
            current = parent[current]

        # Путь от v до корня
        path_v = []
        current = v
        while current != -1:
            path_v.append(current)
            current = parent[current]

        # Находим ближайшего общего предка (LCA)
        i = len(path_u) - 1
        j = len(path_v) - 1
        while i >= 0 and j >= 0 and path_u[i] == path_v[j]:
            i -= 1
            j -= 1

        # Формируем цикл: путь от u до LCA + путь от v до LCA + ребро (u,v)
        cycle = path_u[:i + 1] + path_v[:j + 1][::-1] + [u]
        unique_cycle = sorted(set(cycle))  # Убираем дубликаты и сортируем
        if unique_cycle not in cycles:  # Проверяем уникальность
            cycles.append(unique_cycle)

    # Сортируем циклы по длине и вершинам для консистентности
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
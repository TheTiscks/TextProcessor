import sys
from collections import deque


def find_triangles(graph, n):
    """Находит все треугольники в графе."""
    triangles = []
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if graph[i][j] and graph[j][k] and graph[k][i]:
                    triangles.append(sorted([i, j, k]))
    return triangles


def find_cycle_basis(graph):
    """Находит базис циклов, предпочитая треугольники."""
    n = len(graph)
    m = sum(sum(row) for row in graph) // 2  # Количество рёбер
    cycle_space_dim = m - n + 1  # Размерность циклического пространства

    # Находим все треугольники
    triangles = find_triangles(graph, n)

    if len(triangles) >= cycle_space_dim:
        # Берём первые cycle_space_dim треугольников
        basis = triangles[:cycle_space_dim]
    else:
        # Если треугольников недостаточно, находим фундаментальные циклы
        parent = [-1] * n
        visited = [False] * n
        non_tree_edges = []
        cycles = []

        # Строим остовное дерево с помощью BFS
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
                    elif v != parent[u]:
                        non_tree_edges.append((u, v))

        # Находим циклы для нетривиальных рёбер
        for u, v in non_tree_edges:
            path_u = []
            current = u
            while current != -1:
                path_u.append(current)
                current = parent[current]
            path_u = path_u[::-1]
            path_v = []
            current = v
            while current != -1:
                path_v.append(current)
                current = parent[current]
            path_v = path_v[::-1]
            # Находим LCA
            i = 0
            while i < min(len(path_u), len(path_v)) and path_u[i] == path_v[i]:
                i += 1
            lca = path_u[i - 1] if i > 0 else None
            # Формируем цикл
            cycle = path_u[i:] + [lca] + path_v[i:][::-1] + [u]
            unique_cycle = sorted(set(cycle))
            if unique_cycle not in cycles:
                cycles.append(unique_cycle)
        basis = cycles[:cycle_space_dim]

    return sorted(basis, key=lambda x: (len(x), x)), False


def main(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        size = int(lines[0].strip())
        matrix = [list(map(int, line.strip().split())) for line in lines[1:size + 1]]

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
import sys


def find_triangles(graph, n, directed):
    triangles = []
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if directed:
                    if graph[i][j] and graph[j][k] and graph[k][i]:
                        triangles.append([i, j, k])
                else:
                    if (
                        (graph[i][j] or graph[j][i])
                        and (graph[j][k] or graph[k][j])
                        and (graph[k][i] or graph[i][k])
                    ):
                        triangles.append([i, j, k])
    return triangles


def kosaraju_scc(graph, n):
    # Для орграфов, компоненты связанности
    def dfs_fill(u, visited, order):
        visited[u] = True
        for v in range(n):
            if graph[u][v] and not visited[v]:
                dfs_fill(v, visited, order)
        order.append(u)

    def dfs_assign(u, visited, transposed):
        visited[u] = True
        for v in range(n):
            if transposed[u][v] and not visited[v]:
                dfs_assign(v, visited, transposed)

    visited = [False] * n
    order = []
    for i in range(n):
        if not visited[i]:
            dfs_fill(i, visited, order)

    transposed = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if graph[i][j]:
                transposed[j][i] = 1

    visited = [False] * n
    components = 0
    for u in reversed(order):
        if not visited[u]:
            dfs_assign(u, visited, transposed)
            components += 1
    return components


def find_cycle_basis(graph):
    n = len(graph)
    # Определяем, ориентированный ли граф
    directed = False
    for i in range(n):
        for j in range(n):
            if graph[i][j] != graph[j][i]:
                directed = True
                break
        if directed:
            break

    # Подсчёт рёбер
    m = (
        sum(sum(row) for row in graph)
        if directed
        else sum(sum(row) for row in graph) // 2
    )

    # Подсчёт компонент
    if directed:
        components = kosaraju_scc(graph, n)
    else:
        components = 0
        visited = [False] * n
        for i in range(n):
            if not visited[i]:
                components += 1
                stack = [i]
                visited[i] = True
                while stack:
                    u = stack.pop()
                    for v in range(n):
                        if (graph[u][v] or graph[v][u]) and not visited[v]:
                            visited[v] = True
                            stack.append(v)

    cycle_space_dim = max(0, m - n + components)

    # Поиск треугольников
    triangles = find_triangles(graph, n, directed)
    if len(triangles) >= cycle_space_dim:
        return sorted(triangles[:cycle_space_dim], key=lambda x: (len(x), x)), directed

    # DFS для поиска циклов
    visited = [False] * n
    cycles = []

    def dfs(u, par, path):
        visited[u] = True
        path.append(u)
        for v in range(n):
            if (directed and graph[u][v]) or (
                not directed and (graph[u][v] or graph[v][u])
            ):
                if v != par:
                    if not visited[v]:
                        dfs(v, u, path)
                    elif v in path:
                        idx = path.index(v)
                        cycle = path[idx:]
                        if len(cycle) >= 3 and cycle not in cycles:
                            cycles.append(cycle)
        path.pop()

    for i in range(n):
        if not visited[i]:
            dfs(i, -1, [])

    return sorted(cycles[:cycle_space_dim], key=lambda x: (len(x), x)), directed


def main(input_file):
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        size = int(lines[0].strip())
        matrix = [list(map(int, line.strip().split())) for line in lines[1 : size + 1]]

    answer, _ = find_cycle_basis(matrix)
    with open(input_file, "w", encoding="utf-8") as f:
        f.write(f"{size}\n")
        for row in matrix:
            f.write(" ".join(map(str, row)) + "\n")
        f.write("<Text>\n")
        for cycle in answer:
            f.write("{" + ", ".join(map(str, cycle)) + "}\n")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])

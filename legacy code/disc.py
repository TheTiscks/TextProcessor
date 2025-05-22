import sys

def find_triangles(graph, n):
    triangles = []
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if graph[i][j] and graph[j][k] and graph[k][i]:
                    triangles.append(sorted([i, j, k]))
    return triangles

def find_cycle_basis(graph):
    n = len(graph)
    m = sum(sum(row) for row in graph) // 2

    # Подсчет компонент связности
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
                    if graph[u][v] and not visited[v]:
                        visited[v] = True
                        stack.append(v)

    cycle_space_dim = m - n + components
    if cycle_space_dim < 0:
        cycle_space_dim = 0

    visited = [False] * n
    parent = [-1] * n
    cycles = []

    triangles = find_triangles(graph, n)
    if len(triangles) >= cycle_space_dim:
        return sorted(triangles[:cycle_space_dim], key=lambda x: (len(x), x)), False

    def dfs(u, par, ancestors):
        visited[u] = True
        parent[u] = par
        ancestors.append(u)
        for v in range(n):
            if graph[u][v] and v != par:
                if not visited[v]:
                    dfs(v, u, ancestors.copy())
                else:
                    if v in ancestors:
                        idx = ancestors.index(v)
                        cycle = ancestors[idx:] + [v]
                        unique_cycle = sorted(set(cycle))
                        if len(unique_cycle) >= 3 and unique_cycle not in cycles:
                            cycles.append(unique_cycle)
        ancestors.pop()  # Удаление текущей вершины из стека

    # Запуск DFS для каждой непосещенной вершины
    for i in range(n):
        if not visited[i]:
            dfs(i, -1, [])

    # Сортировка и возврат нужного количества циклов
    sorted_cycles = sorted(cycles, key=lambda x: (len(x), x))
    return sorted_cycles[:cycle_space_dim], False

def main(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        size = int(lines[0].strip())
        matrix = [list(map(int, line.strip().split())) for line in lines[1:size + 1]]

    answer, directed = find_cycle_basis(matrix)
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(f"{size}\n")
        for row in matrix:
            f.write(' '.join(map(str, row)) + '\n')
        f.write("<Text>\n")
        for cycle in sorted(answer, key=lambda x: (len(x), x)):
            f.write("{" + ", ".join(map(str, cycle)) + "}\n")

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
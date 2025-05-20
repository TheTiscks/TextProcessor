import sys

def is_directed(graph):
    n = len(graph)
    for i in range(n):
        for j in range(n):
            if graph[i][j] != graph[j][i]:
                return True
    return False

def find_cycle_basis(graph):
    n = len(graph)
    directed = is_directed(graph)
    visited = [False] * n
    parent = [-1] * n
    cycle_basis = []

    def dfs(u):
        stack.append(u)
        visited[u] = True
        for v in range(n):
            if graph[u][v]:
                if not visited[v]:
                    parent[v] = u
                    dfs(v)
                else:
                    if (directed or v != parent[u]) and v in stack:
                        idx = stack.index(v)
                        cycle = stack[idx:] + [v]
                        if len(cycle) >= (3 if not directed else 2):
                            cycle_basis.append(cycle)
        stack.pop()

    for i in range(n):
        if not visited[i]:
            stack = []
            dfs(i)

    # Нормализация циклов для неориентированных графов
    unique_cycles = []
    seen = set()
    for cycle in cycle_basis:
        vertices = cycle[:-1]  # Убираем повторяющуюся вершину
        if not directed:
            if len(vertices) < 3:
                continue
            # Сортируем и находим минимальную вершину
            min_vertex = min(vertices)
            min_idx = vertices.index(min_vertex)
            rotated = vertices[min_idx:] + vertices[:min_idx]
            # Проверяем оба направления
            if tuple(rotated) not in seen and tuple(reversed(rotated)) not in seen:
                seen.add(tuple(rotated))
                unique_cycles.append(sorted(rotated))
        else:
            if len(vertices) < 2:
                continue
            cycle_tuple = tuple(vertices)
            if cycle_tuple not in seen:
                seen.add(cycle_tuple)
                unique_cycles.append(vertices)

    return unique_cycles, directed

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
        for cycle in answer:
            if directed:
                cycle_str = "{" + ", ".join(map(str, cycle)) + "}\n"
            else:
                cycle_str = "{" + ", ".join(map(str, sorted(cycle))) + "}\n"
            f.write(cycle_str)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
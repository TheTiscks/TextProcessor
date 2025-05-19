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
    cycle_basis = []
    stack = []
    in_stack = [False] * n

    def dfs(u, parent):
        visited[u] = True
        stack.append(u)
        in_stack[u] = True
        for v in range(n):
            if graph[u][v]:
                if not visited[v]:
                    dfs(v, u)
                else:
                    if directed:
                        if in_stack[v]:
                            idx = stack.index(v)
                            cycle = stack[idx:] + [v]
                            cycle_basis.append(cycle)
                    else:
                        if v != parent and in_stack[v]:
                            idx = stack.index(v)
                            cycle = stack[idx:] + [v]
                            cycle_basis.append(cycle)
        stack.pop()
        in_stack[u] = False

    for i in range(n):
        if not visited[i]:
            dfs(i, -1)

    # Удаление дубликатов и нормализация
    unique_cycles = []
    if not directed:
        seen = set()
        for cycle in cycle_basis:
            if len(cycle) < 3:
                continue
            vertices = cycle[:-1]
            min_vertex = min(vertices)
            min_idx = vertices.index(min_vertex)
            rotated = vertices[min_idx:] + vertices[:min_idx]
            normalized = tuple(rotated)
            reversed_normalized = tuple(reversed(rotated))
            if normalized not in seen and reversed_normalized not in seen:
                seen.add(normalized)
                unique_cycles.append(cycle)
    else:
        seen = set()
        for cycle in cycle_basis:
            vertices = cycle[:-1]
            cycle_tuple = tuple(vertices)
            if cycle_tuple not in seen:
                seen.add(cycle_tuple)
                unique_cycles.append(cycle)

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
            vertices = cycle[:-1]
            if not directed:
                vertices = sorted(vertices)
            if len(vertices) >= 2:
                cycle_str = "{" + ", ".join(map(str, vertices)) + "}\n"
                f.write(cycle_str)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
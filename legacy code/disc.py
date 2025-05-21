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
    cycles = []
    stack = []

    def dfs(u):
        nonlocal stack
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
                        if (directed and len(cycle) >= 2) or (not directed and len(cycle) >= 3):
                            cycles.append(cycle)
        stack.pop()

    for i in range(n):
        if not visited[i]:
            stack = []
            dfs(i)

    # Удаление избыточных циклов
    unique_cycles = []
    seen = set()
    for cycle in cycles:
        vertices = sorted(list(dict.fromkeys(cycle[:-1])))  # Сортировка и удаление дублей
        if directed:
            key = tuple(vertices)
        else:
            key = tuple(vertices)
            reversed_key = tuple(reversed(vertices))
        if key not in seen and (not directed and reversed_key not in seen):
            seen.add(key)
            # Проверка на минимальность: цикл не должен содержать подциклы
            is_minimal = True
            for existing in unique_cycles:
                if set(existing).issubset(set(vertices)):
                    is_minimal = False
                    break
            if is_minimal:
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
            cycle_str = "{" + ", ".join(map(str, sorted(cycle))) + "}\n"
            f.write(cycle_str)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
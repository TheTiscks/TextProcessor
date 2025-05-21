import sys

def is_directed(graph):
    n = len(graph)
    for i in range(n):
        for j in range(n):
            if graph[i][j] != graph[j][i]:
                return True
    return False

def get_edges(graph, directed):
    n = len(graph)
    edges = []
    for u in range(n):
        for v in range(n):
            if graph[u][v]:
                if directed or (u < v and graph[u][v] == graph[v][u]):
                    edges.append((u, v))
    return edges

def cycle_to_vector(cycle, edges):
    vector = [0] * len(edges)
    for i in range(len(cycle)-1):
        u, v = cycle[i], cycle[i+1]
        edge = (u, v) if (u, v) in edges else (v, u)
        if edge in edges:
            idx = edges.index(edge)
            vector[idx] ^= 1
    return vector

def gaussian_elimination(vectors):
    if not vectors:
        return [], []
    matrix = [vec.copy() for vec in vectors]
    rank = 0
    rows = len(matrix)
    cols = len(matrix[0])
    pivot_cols = []
    for col in range(cols):
        pivot = -1
        for row in range(rank, rows):
            if matrix[row][col] == 1:
                pivot = row
                break
        if pivot == -1:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        for row in range(rows):
            if row != rank and matrix[row][col] == 1:
                matrix[row] = [(a ^ b) for a, b in zip(matrix[row], matrix[rank])]
        pivot_cols.append(col)
        rank += 1
    basis = [matrix[i] for i in range(rank)]
    return basis, pivot_cols

def find_cycle_basis(graph):
    n = len(graph)
    directed = is_directed(graph)
    visited = [False] * n
    parent = [-1] * n
    raw_cycles = []
    edges = get_edges(graph, directed)

    def dfs(u):
        stack.append(u)
        visited[u] = True
        for v in range(n):
            if graph[u][v]:
                if not visited[v]:
                    parent[v] = u
                    dfs(v)
                else:
                    # Исправлено: строгая проверка для неориентированных графов
                    if directed or (v != parent[u]):
                        if v in stack:
                            idx = stack.index(v)
                            cycle = stack[idx:] + [v]
                            # Учитываем только циклы длиной >=3 для неориентированных
                            if (directed and len(cycle) >= 2) or (not directed and len(cycle) >= 3):
                                raw_cycles.append(cycle)
        stack.pop()

    for i in range(n):
        if not visited[i]:
            stack = []
            dfs(i)

    cycle_vectors = []
    valid_cycles = []
    for cycle in raw_cycles:
        vec = cycle_to_vector(cycle, edges)
        if sum(vec) > 0:
            cycle_vectors.append(vec)
            valid_cycles.append(cycle)

    basis, _ = gaussian_elimination(cycle_vectors)
    basis_indices = []
    for b in basis:
        for idx, vec in enumerate(cycle_vectors):
            if vec == b:
                basis_indices.append(idx)
                break

    unique_cycles = []
    seen = set()
    for idx in basis_indices:
        cycle = valid_cycles[idx]
        vertices = list(dict.fromkeys(cycle[:-1]))
        if not directed:
            # Нормализация: сортировка и проверка уникальности
            vertices = sorted(vertices)
            key = tuple(vertices)
            reversed_key = tuple(reversed(vertices))
            if key not in seen and reversed_key not in seen:
                seen.add(key)
                unique_cycles.append(vertices)
        else:
            key = tuple(vertices)
            if key not in seen:
                seen.add(key)
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
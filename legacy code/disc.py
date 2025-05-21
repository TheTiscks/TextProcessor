import sys
from collections import defaultdict

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
    edge_states = defaultdict(int)  # Для отслеживания посещённых рёбер

    def dfs(u):
        nonlocal stack
        stack.append(u)
        visited[u] = True
        for v in range(n):
            if graph[u][v]:
                if not visited[v]:
                    parent[v] = u
                    edge_states[(u, v)] += 1
                    dfs(v)
                    edge_states[(u, v)] -= 1
                else:
                    # Для неориентированных графов игнорируем обратное ребро к родителю
                    if (directed or v != parent[u]) and v in stack:
                        idx = stack.index(v)
                        cycle = stack[idx:] + [v]
                        # Проверка на минимальную длину цикла
                        if (directed and len(cycle) >= 2) or (not directed and len(cycle) >= 3):
                            # Нормализация цикла
                            vertices = sorted(list(set(cycle[:-1])))
                            if vertices not in cycles:
                                cycles.append(vertices)
        stack.pop()
        visited[u] = False  # Сбрасываем посещение для поиска всех циклов

    # Для ориентированных графов перебираем все вершины
    for start in range(n):
        if not visited[start]:
            stack = []
            dfs(start)

    # Фильтрация циклов: удаляем надмножества
    basis = []
    cycles.sort(key=lambda x: len(x))
    for cycle in cycles:
        cycle_set = set(cycle)
        is_independent = True
        for existing in basis:
            if existing.issubset(cycle_set):
                is_independent = False
                break
        if is_independent:
            basis.append(cycle_set)

    # Преобразуем обратно в списки и сортируем
    result = [sorted(list(s)) for s in basis]
    return result, directed

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
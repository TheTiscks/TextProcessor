import sys


def read_graph(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        size = int(lines[0].strip().split()[0])
        matrix = []
        for i in range(1, size + 1):
            row = list(map(int, lines[i].strip().split()))
            matrix.append(row)
    return matrix, size


def dfs(u, graph, visited, parent, cycles, depth):
    visited[u] = True
    for v in range(len(graph)):
        if graph[u][v] == 0:
            continue

        if not visited[v]:
            parent[v] = u
            depth[v] = depth[u] + 1
            dfs(v, graph, visited, parent, cycles, depth)
        elif v != parent[u] and depth[v] < depth[u]:
            # Обнаружен цикл
            cycle = []
            current = u
            while current != v:
                cycle.append(current)
                current = parent[current]
            cycle.extend([v, u])  # Замыкаем цикл
            cycles.append(cycle)


def find_cycles(graph, size):
    visited = [False] * size
    parent = [-1] * size
    depth = [0] * size
    cycles = []

    for i in range(size):
        if not visited[i]:
            dfs(i, graph, visited, parent, cycles, depth)

    # Удаление дубликатов
    unique_cycles = []
    for cycle in cycles:
        normalized = sorted(cycle[:-1])  # Игнорируем последний элемент (дублирует первый)
        if normalized not in [sorted(c[:-1]) for c in unique_cycles]:
            unique_cycles.append(cycle)

    return unique_cycles


def save_result(input_file, matrix, cycles):
    with open(input_file, 'w', encoding='utf-8') as f:
        # Сохраняем исходные данные
        f.write(f"{len(matrix)} 0\n")
        for row in matrix:
            f.write(' '.join(map(str, row)) + '\n')

        # Запись результатов
        f.write("<Text>\n")
        f.write(f"Найдено циклов: {len(cycles)}\n")
        for i, cycle in enumerate(cycles, 1):
            cycle_str = " → ".join(map(str, cycle))
            f.write(f"Цикл {i}: {cycle_str}\n")


def main(input_file):
    graph, size = read_graph(input_file)
    cycles = find_cycles(graph, size)
    save_result(input_file, graph, cycles)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
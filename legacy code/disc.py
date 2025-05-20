import sys


def canonical_cycle(cycle):
    """
    Возвращает каноническое представление цикла для неориентированных графов.
    """
    min_vertex = min(cycle)
    min_index = cycle.index(min_vertex)
    rotated = cycle[min_index:] + cycle[:min_index]
    reversed_rotated = rotated[::-1]
    return tuple(min(rotated, reversed_rotated))


def find_cycle_basis(graph, directed=False):
    """
    Находит базу циклов графа.
    """

    def dfs(v, parent, start, path, used, cycles):
        used[v] = True
        path.append(v)

        for u in range(len(graph)):
            if graph[v][u]:
                if not directed and u == parent:
                    continue
                if u in path:
                    cycle_start = path.index(u)
                    cycle = path[cycle_start:]
                    if directed or len(cycle) >= 3:  # В неориентированных графах минимальная длина цикла — 3
                        cycles.append(cycle)
                elif not used[u]:
                    dfs(u, v, start, path, used, cycles)

        path.pop()
        if not directed:
            used[v] = False

    n = len(graph)
    cycles = []
    used = [False] * n

    for start in range(n):
        dfs(start, -1, start, [], used, cycles)

    # Фильтрация уникальных циклов
    unique_cycles = []
    seen = set()
    for cycle in cycles:
        if not directed:
            canonical = canonical_cycle(cycle)
            if canonical not in seen:
                seen.add(canonical)
                unique_cycles.append(cycle)
        else:
            cycle_tuple = tuple(cycle)
            if cycle_tuple not in seen:
                seen.add(cycle_tuple)
                unique_cycles.append(cycle)

    return unique_cycles


def main(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        size = int(lines[0].strip())
        matrix = [list(map(int, line.strip().split())) for line in lines[1:size + 1]]

    # Проверка, ориентированный ли граф
    directed = False
    for i in range(size):
        for j in range(size):
            if matrix[i][j] != matrix[j][i]:
                directed = True
                break
        if directed:
            break

    answer = find_cycle_basis(matrix, directed)

    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(f"{size}\n")
        for i in range(size):
            f.write(' '.join(map(str, matrix[i])) + '\n')
        f.write("<Text>\n")
        if answer:
            max_len = max(len(cycle) for cycle in answer)
            for cycle in answer:
                if len(cycle) == max_len:
                    f.write("{")
                    f.write(', '.join(map(str, cycle)))
                    f.write("}\n")
        else:
            f.write("No cycles found.\n")


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
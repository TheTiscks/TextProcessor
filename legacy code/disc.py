import sys


def find_cycle_basis(graph, directed=False):
    """
    Находит базу циклов графа с использованием DFS.
    :param graph: Матрица смежности графа
    :param directed: Флаг, указывающий, является ли граф ориентированным
    :return: Список циклов, образующих базу
    """

    def dfs(v, parent, start, path, used, cycles):
        used[v] = True
        path.append(v)

        # Проверяем соседей вершины
        for u in range(len(graph)):
            if graph[v][u]:  # Если есть ребро
                # Для неориентированного графа пропускаем родителя
                if not directed and u == parent:
                    continue
                # Если нашли вершину из текущего пути (кроме родителя), то найден цикл
                if u in path:
                    cycle_start = path.index(u)
                    cycle = path[cycle_start:]
                    # Для неориентированного графа проверяем минимальность цикла
                    if directed or len(cycle) >= 3:
                        cycles.append(cycle)
                # Если вершина не посещена, продолжаем DFS
                elif not used[u]:
                    dfs(u, v, start, path, used, cycles)

        path.pop()
        # Для ориентированного графа не сбрасываем used, чтобы избежать повторных посещений
        if not directed:
            used[v] = False

    n = len(graph)
    cycles = []
    used = [False] * n

    # Запускаем DFS из каждой вершины
    for start in range(n):
        dfs(start, -1, start, [], used, cycles)

    # Фильтруем и минимизируем базу циклов
    unique_cycles = []
    seen = set()
    for cycle in cycles:
        # Приводим цикл к "каноническому" виду (начинается с минимальной вершины)
        min_idx = cycle.index(min(cycle))
        canonical = tuple(cycle[min_idx:] + cycle[:min_idx])
        # Для неориентированного графа добавляем обратный порядок
        if not directed:
            canonical_rev = tuple(cycle[::-1])
            canonical = min(canonical, canonical_rev)
        if canonical not in seen:
            seen.add(canonical)
            unique_cycles.append(list(cycle))

    return unique_cycles


def main(input_file):
    # Чтение входного файла
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        size = int(lines[0].strip())
        matrix = []
        for i in range(1, size + 1):
            row = list(map(int, lines[i].strip().split()))
            matrix.append(row)

    # Определяем, является ли граф ориентированным
    directed = False
    for i in range(size):
        for j in range(size):
            if matrix[i][j] != matrix[j][i]:
                directed = True
                break
        if directed:
            break

    # Находим базу циклов
    answer = find_cycle_basis(matrix, directed)

    # Запись результата в файл
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(f"{size}\n")
        for i in range(size):
            f.write(' '.join(map(str, matrix[i])) + '\n')
        f.write("<Text>\n")
        max_len = 0
        for cycle in answer:
            max_len = max(len(cycle), max_len)
        for cycle in answer:
            if len(cycle) == max_len:
                f.write("{")
                for j in range(len(cycle)):
                    f.write(str(cycle[j]))
                    if j < len(cycle) - 1:
                        f.write(', ')
                f.write("}\n")


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
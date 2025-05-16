import sys


class Graph:
    def __init__(self):
        self.V = 0
        self.matrix = []
        self.is_directed = False


def read_graph_from_file(filename):
    graph = Graph()
    with open(filename, 'r') as file:
        # Чтение количества вершин и игнорирование второго числа (для двудольных графов)
        line = file.readline().strip().split()
        graph.V = int(line[0])

        # Чтение матрицы смежности
        graph.matrix = []
        for _ in range(graph.V):
            row = list(map(int, file.readline().strip().split()))
            graph.matrix.append(row)

        # Проверка на ориентированность
        graph.is_directed = False
        for i in range(graph.V):
            for j in range(graph.V):
                if graph.matrix[i][j] != graph.matrix[j][i]:
                    graph.is_directed = True
                    break
            if graph.is_directed:
                break
    return graph


def find_cycles(graph):
    visited = [False] * graph.V
    parent = [-1] * graph.V
    depth = [0] * graph.V
    cycles = []

    def dfs(u):
        nonlocal visited, parent, depth, cycles
        visited[u] = True
        for v in range(graph.V):
            if graph.matrix[u][v] == 0:
                continue

            if not visited[v]:
                parent[v] = u
                depth[v] = depth[u] + 1
                dfs(v)
            elif v != parent[u] and depth[v] < depth[u]:
                # Обнаружено обратное ребро, формируем цикл
                current = u
                cycle = []
                while current != v:
                    cycle.append(current)
                    current = parent[current]
                cycle.extend([v, u])  # Замыкаем цикл
                cycles.append(cycle)

    for i in range(graph.V):
        if not visited[i]:
            dfs(i)

    return cycles


def save_result(filename, graph, cycles):
    with open(filename, 'w') as file:
        # Сохранение базовой структуры графа
        file.write(f"{graph.V} 0\n")
        for row in graph.matrix:
            file.write(" ".join(map(str, row)) + "\n")

        # Запись циклов в секцию <Text>
        file.write("<Text>\n")
        file.write(f"Найдено циклов: {len(cycles)}\n")
        for i, cycle in enumerate(cycles):
            file.write(f"Цикл {i + 1}: {' '.join(map(str, cycle))}\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python cycle_base.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    graph = read_graph_from_file(input_file)
    cycles = find_cycles(graph)
    save_result("output.txt", graph, cycles)

    print("Обработка завершена. Результат сохранен в output.txt")
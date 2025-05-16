import sys


class Graph:
    def __init__(self):
        self.V = 0
        self.matrix = []
        self.is_directed = False


def read_graph_from_file(filename):
    graph = Graph()
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            # Чтение количества вершин (первое число в первой строке)
            graph.V = int(lines[0].strip().split()[0])

            # Чтение матрицы смежности
            graph.matrix = []
            for i in range(1, graph.V + 1):
                row = list(map(int, lines[i].strip().split()))
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
    except Exception as e:
        print(f"Ошибка чтения файла: {e}")
        sys.exit(1)
    return graph


def find_cycles(graph):
    visited = [False] * graph.V
    parent = [-1] * graph.V
    cycles = []

    def dfs(u):
        nonlocal visited, parent, cycles
        visited[u] = True
        for v in range(graph.V):
            if graph.matrix[u][v] == 0:
                continue

            if not visited[v]:
                parent[v] = u
                dfs(v)
            elif v != parent[u]:
                # Обнаружен цикл
                cycle = []
                current = u
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
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            # Запись базовой структуры графа
            file.write(f"{graph.V} 0\n")
            for row in graph.matrix:
                file.write(" ".join(map(str, row)) + "\n")

            # Секция для вывода в консоль Графоида
            file.write("<Text>\n")
            file.write("=== Результаты анализа ===\n")
            file.write(f"Найдено циклов: {len(cycles)}\n\n")

            for i, cycle in enumerate(cycles, 1):
                cycle_str = " → ".join(map(str, cycle))
                file.write(f"Цикл {i}: {cycle_str}\n")

            # Пример добавления цвета (если требуется)
            file.write("\n<Vertex_Colors>\n")
            file.write("0 green\n")  # Пример окрашивания вершины 0 в зеленый

    except Exception as e:
        print(f"Ошибка сохранения файла: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python cycle_finder.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    graph = read_graph_from_file(input_file)
    cycles = find_cycles(graph)
    save_result("output.txt", graph, cycles)

    print("Обработка завершена. Файл 'output.txt' создан.")
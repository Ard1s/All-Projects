class Graph:
    def __init__(self, vertices):
        self.vertices = vertices
        self.graph = [[0 for column in range(vertices)]
                      for row in range(vertices)]

    def add_edge(self, u, v):
        """
        Добавить ребро между u и v в граф
        """
        self.graph[u - 1][v - 1] = 1
        self.graph[v - 1][u - 1] = 1

    def bron_kerbosch(self, r, p, x, cliques):
        """
        Реализация итеративного алгоритма Брона–Кербоша
        """
        stack = [(r, p, x)]
        while stack:
            r, p, x = stack.pop()
            if not p and not x:
                cliques.append(r)
            else:
                pivot = p + x
                if pivot:
                    try:
                        u = max(pivot, key=lambda v: self.degree(v))
                        pivot.remove(u)
                        for vertex in p[:]:
                            if self.graph[u - 1][vertex - 1]:
                                r_new = r + [vertex]
                                p_new = [v for v in p if self.graph[vertex - 1][v - 1]]
                                x_new = [v for v in x if self.graph[vertex - 1][v - 1]]
                                stack.append((r_new, p_new, x_new))
                    except IndexError:
                        pass

    def degree(self, vertex):
        """
        Определить степень вершины
        """
        return sum(self.graph[vertex - 1])

    def find_cliques(self):
        """
        Найти все клики в графе
        """
        cliques = []
        self.bron_kerbosch([], [i+1 for i in range(self.vertices)], [], cliques)
        return cliques

    def is_perfect_graph(self):
        """
        Проверить, является ли граф совершенным
        """
        for vertex in range(1, self.vertices + 1):
            try:
                subgraph = self.get_induced_subgraph(vertex)
                if not subgraph.is_perfect_graph_brute_force():
                    return False
            except IndexError:
                pass
        return True

    def is_perfect_graph_brute_force(self):
        """
        Проверить, является ли подграф совершенным
        (брутфорс-подход для малых подграфов)
        """
        cliques = self.find_cliques()
        max_clique_size = max([len(clique) for clique in cliques], default=0)
        if max_clique_size == self.vertices:
            return True
        return False

    def get_induced_subgraph(self, vertex):
        """
        Получить индуцированный подграф для заданной вершины
        """
        subgraph = Graph(self.vertices)
        for i in range(self.vertices):
            for j in range(i + 1, self.vertices):
                if self.graph[i][j] == 1 and (i + 1 == vertex or j + 1 == vertex):
                    subgraph.add_edge(i + 1, j + 1)
        return subgraph

    def chromatic_number(self):
        """
        Определить хроматическое число графа
        """
        return self.chromatic_number_recursive(list(range(1, self.vertices + 1)), [])

    def chromatic_number_recursive(self, vertices, coloring):
        """
        Рекурсивная функция для определения хроматического числа
        """
        if not vertices:
            if coloring:
                return len(set(coloring))
            else:
                return -1  # Отсутствие определенного хроматического числа
        vertex = vertices[0]
        neighbors = [v for v in vertices if self.graph[vertex - 1][v - 1] == 0]
        min_color = -1  # Обозначение отсутствия определенного хроматического числа
        for color in range(1, self.vertices + 1):
            if all((v - 1 < len(coloring) and coloring[v - 1] != color) for v in neighbors):
                if vertex - 1 < len(coloring):
                    coloring[vertex - 1] = color
                else:
                    coloring.append(color)
                result = self.chromatic_number_recursive(vertices[1:], coloring)
                if min_color == -1 or (result != -1 and result < min_color):
                    min_color = result
                if vertex - 1 < len(coloring):
                    coloring[vertex - 1] = 0
                else:
                    coloring.pop()
        return min_color


if __name__ == "__main__":
    while True:
        try:
            vertices = int(input("Введите количество вершин в графе: "))
            if vertices <= 0:
                raise ValueError
            break
        except ValueError:
            print("Некорректное значение. Введите положительное целое число.")

    g = Graph(vertices)

    while True:
        try:
            edges = int(input("Введите количество ребер: "))
            if edges < 0:
                raise ValueError
            break
        except ValueError:
            print("Некорректное значение. Введите неотрицательное целое число.")

    print("Введите ребра в формате 'u v':")
    for _ in range(edges):
        while True:
            try:
                u, v = map(int, input().split())
                if u <= 0 or v <= 0 or u > vertices or v > vertices:
                    raise ValueError
                break
            except ValueError:
                print("Некорректное значение. Введите два положительных целых числа в диапазоне от 1 до", vertices)

        g.add_edge(u, v)

    print("Клики в графе:")
    cliques = g.find_cliques()
    if not cliques:
        print("В графе нет клик.")
    else:
        for clique in cliques:
            print(clique)

    if g.is_perfect_graph():
        print("Граф является совершенным.")
    else:
        print("Граф не является совершенным.")

    chromatic_number = g.chromatic_number()
    print("Хроматическое число графа:", chromatic_number)

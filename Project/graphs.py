class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)] for row in range(vertices)]
        self.color_arr = [0 for i in range(vertices)]

    def add_edge(self, u, v):
        self.graph[u - 1][v - 1] = 1
        self.graph[v - 1][u - 1] = 1

    def bron_kerbosch(self, r, p, x, cliques):
        stack = [(r, p, x)]
        while stack:
            r, p, x = stack.pop()
            if not p and not x:
                cliques.append(r)
            else:
                for vertex in p[:]:
                    r_new = r + [vertex]
                    p_new = [v for v in p if self.graph[vertex - 1][v - 1]]
                    x_new = [v for v in x if self.graph[vertex - 1][v - 1]]
                    stack.append((r_new, p_new, x_new))

    def find_cliques(self):
        cliques = []
        self.bron_kerbosch([], [i+1 for i in range(self.V)], [], cliques)
        return cliques

    def chromatic_number(self):
        self.color_arr[0] = 0
        for u in range(1, self.V):
            self.color_arr[u] = -1

        for u in range(1, self.V):
            colored_neighbors = [False] * self.V
            for i in range(self.V):
                if self.graph[u][i] and self.color_arr[i] != -1:
                    colored_neighbors[self.color_arr[i]] = True

            color = 0
            while colored_neighbors[color]:
                color += 1

            self.color_arr[u] = color

        return max(self.color_arr) + 1
    
    def is_perfect(self):
        cliques = self.find_cliques()
        chromatic_number = self.chromatic_number()
        for clique in cliques:
            if len(clique) != chromatic_number:
                return False
        return True

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
    if g.is_perfect():
        print("Граф является совершенным.")
    else:
        print("Граф не является совершенным.")
    
    print("Хроматическое число графа: ", g.chromatic_number())

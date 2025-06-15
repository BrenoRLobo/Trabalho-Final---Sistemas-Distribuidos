import itertools
import math
import time
from utils.mordor_data import get_mordor_cities_data

#Constrói a matriz de distâncias entre todas as cidades usando a fórmula da distância Euclidiana
class TSPProblem:
    def __init__(self, cities):
        self.city_names = [name for name, _ in cities]
        self.coordinates = [coord for _, coord in cities]
        self.n = len(cities)
        self.distances = self._compute_distances()

    def _compute_distances(self):
        dist = [[0] * self.n for _ in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                if i != j:
                    xi, yi = self.coordinates[i]
                    xj, yj = self.coordinates[j]
                    dist[i][j] = math.hypot(xi - xj, yi - yj)
        return dist

    #Calcula o custo total de uma rota (soma das distâncias entre as cidades visitadas + retorno à cidade inicial)
    def route_cost(self, route):
        cost = 0
        for i in range(len(route) - 1):
            cost += self.distances[route[i]][route[i+1]]
        cost += self.distances[route[-1]][route[0]]
        return cost

#Avalia o custo de cada permutação e armazena a de menor custo como a melhor rota
class TSPBruteForceSolver:
    def __init__(self, problem):
        self.problem = problem

    def solve(self):
        best_cost = float('inf')
        best_route = []
        #Gera todas as possíveis ordens de visita às cidades
        for perm in itertools.permutations(range(self.problem.n)):
            cost = self.problem.route_cost(perm)
            if cost < best_cost:
                best_cost = cost
                best_route = perm
        return best_route, best_cost

#Testa o algoritmo com diferentes números de cidades (de 4 até 10) e imprime a melhor rota, o custo e o tempo gasto 
def main():
    cities_data = get_mordor_cities_data()
    for size in range(4, len(cities_data) + 1):
        print(f"\n🧭 Executando TSP para {size} cidades...")
        selected = cities_data[:size]
        problem = TSPProblem(selected)
        solver = TSPBruteForceSolver(problem)

        start = time.time()
        best_route, best_cost = solver.solve()
        end = time.time()

        named_route = [problem.city_names[i] for i in best_route]
        print(f"🔁 Melhor rota: {named_route}")
        print(f"💰 Custo total: {best_cost:.2f}")
        # Calcula o tempo de execução
        print(f"⏱️ Tempo de execução: {end - start:.5f} segundos")

if __name__ == "__main__":
    main()

import itertools
import math
import time
import os
import threading
from mordor_data import get_mordor_cities_data

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

    def route_cost(self, route):
        
        cost = 0
        for i in range(len(route) - 1):
            cost += self.distances[route[i]][route[i+1]]
        cost += self.distances[route[-1]][route[0]] 
        return cost


class TSPParallelBruteForceSolver:
    def __init__(self, problem, num_threads=None):
        self.problem = problem
        
        self.num_threads = num_threads if num_threads is not None else os.cpu_count()
        self.best_route = None
        self.best_cost = float('inf')
       
        self.lock = threading.Lock()

    def _worker(self, permutations_chunk):
    
        local_best_cost = float('inf')
        local_best_route = []

        for perm in permutations_chunk:
            cost = self.problem.route_cost(perm)
            if cost < local_best_cost:
                local_best_cost = cost
                local_best_route = perm
        
        
        with self.lock:
            if local_best_cost < self.best_cost:
                self.best_cost = local_best_cost
                self.best_route = local_best_route

    def solve(self):
       
        other_cities = range(1, self.problem.n)
        all_perms = list(itertools.permutations(other_cities))
        
        
        all_routes = [[0] + list(p) for p in all_perms]

        threads = []
        
        chunk_size = math.ceil(len(all_routes) / self.num_threads)

        for i in range(self.num_threads):
            start = i * chunk_size
            end = start + chunk_size
            chunk = all_routes[start:end]
            
            if not chunk: 
                continue

            # Cria e inicia o thread.
            thread = threading.Thread(target=self._worker, args=(chunk,))
            threads.append(thread)
            thread.start()
            
  
        for thread in threads:
            thread.join()
            
        return self.best_route, self.best_cost


def main():
    cities_data = get_mordor_cities_data()
  
    num_threads = os.cpu_count() 
    print(f"🚀 Iniciando a solução paralela com {num_threads} threads.")
    
    for size in range(4, len(cities_data) + 1):
        print(f"\n🧭 Executando TSP para {size} cidades...")
        selected = cities_data[:size]
        problem = TSPProblem(selected)
        # Instancia o solver paralelo.
        solver = TSPParallelBruteForceSolver(problem, num_threads)

        start = time.time()
        best_route, best_cost = solver.solve()
        end = time.time()
        
        if best_route is None:
            print("Não foi encontrada uma solução.")
            continue

        named_route = [problem.city_names[i] for i in best_route]
        print(f"🔁 Melhor rota: {named_route}")
        print(f"💰 Custo total: {best_cost:.2f}")
        # Calcula o tempo de execução.
        print(f"⏱️  Tempo de execução: {end - start:.5f} segundos")

if __name__ == "__main__":
    main()

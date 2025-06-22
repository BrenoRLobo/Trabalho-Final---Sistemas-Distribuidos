# utils/calculations.py
import math

def calculate_distance(city1_coords, city2_coords):
    """Calcula a distância euclidiana entre duas cidades."""
    return math.sqrt((city1_coords[0] - city2_coords[0])**2 + (city1_coords[1] - city2_coords[1])**2)

def precompute_distances(cities_coords):
    """Pré-calcula todas as distâncias entre as cidades."""
    num_cities = len(cities_coords)
    distances = {}
    for i in range(num_cities):
        distances[i] = {}
        for j in range(num_cities):
            if i == j:
                distances[i][j] = 0.0
            else:
                distances[i][j] = calculate_distance(cities_coords[i], cities_coords[j])
    return distances

def calculate_total_distance(tour_indices, precomputed_distances):
    """Calcula a distância total de um tour (lista de índices de cidades)."""
    total_dist = 0
    num_cities = len(tour_indices)
    if num_cities < 2:
        return 0

    for i in range(num_cities - 1):
        total_dist += precomputed_distances[tour_indices[i]][tour_indices[i+1]]
    total_dist += precomputed_distances[tour_indices[-1]][tour_indices[0]]
    return total_dist
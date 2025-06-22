# utils/mordor_data.py

MORDOR_LOCATIONS = {
    "Barad-dûr": (50, 50),
    "Mount Doom": (60, 40),
    "Cirith Ungol": (30, 70),
    # "Udûn": (45, 60),
    # "Morannon": (40, 80),
    # "Gorgoroth": (70, 30),
    # "Minas Morgul": (20, 55),
    # "Durthang": (55, 75),
    # "Isenmouthe": (65, 85),
    # "Narchost": (35, 45)
}

def get_mordor_cities_data():
    """
    Retorna as coordenadas das cidades, um mapeamento de nome para índice
    e de índice para nome para as cidades de Mordor.
    """
    city_names = list(MORDOR_LOCATIONS.keys())
    cities_coords = list(MORDOR_LOCATIONS.values())
    name_to_index = {name: i for i, name in enumerate(city_names)}
    index_to_name = {i: name for i, name in enumerate(city_names)}
    return cities_coords, name_to_index, index_to_name
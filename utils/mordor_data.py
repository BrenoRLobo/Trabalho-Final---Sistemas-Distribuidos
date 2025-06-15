#Grafo de coordenadas das cidades
MORDOR_LOCATIONS = {
    "Barad-dûr": (50, 50),
    "Mount Doom": (60, 40),
    "Cirith Ungol": (30, 70),
    "Udûn": (45, 60),
    "Morannon": (40, 80),
    "Gorgoroth": (70, 30),
    "Minas Morgul": (20, 55),
    "Durthang": (55, 75),
    "Isenmouthe": (65, 85),
    "Narchost": (35, 45)
}

def get_mordor_cities_data():
    return list(MORDOR_LOCATIONS.items())

# server.py
import socket
import pickle
import itertools
import threading
import time

from utils.calculations import precompute_distances, calculate_total_distance
from utils.mordor_data import get_mordor_cities_data

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

class TSPMaster:
    def __init__(self):
        self.cities_coords, self.name_to_index, self.index_to_name = get_mordor_cities_data()
        self.precomputed_distances = precompute_distances(self.cities_coords)
        self.num_cities = len(self.cities_coords)
        
        self.all_permutations = self._generate_all_permutations()
        self.total_permutations = len(self.all_permutations)
        self.permutation_index = 0
        
        self.best_overall_tour = None
        self.min_overall_distance = float('inf')
        
        self.lock = threading.Lock() # Para acesso thread-safe aos resultados e índice de permutações
        self.clients_connected = 0
        print(f"Servidor TSP inicializado com {self.num_cities} cidades e {self.total_permutations} permutações a considerar.")

    def _generate_all_permutations(self):
        """
        Gera todas as permutações das cidades, fixando a primeira cidade
        para evitar redundância e reduzir o espaço de busca.
        """
        if self.num_cities == 0:
            return []
        
        # Fixa a primeira cidade (índice 0) para reduzir o espaço de busca.
        # Todas as rotas válidas são permutações das cidades restantes
        # começando e terminando na cidade fixa.
        remaining_cities_indices = list(range(1, self.num_cities))
        
        permutations = []
        for p in itertools.permutations(remaining_cities_indices):
            permutations.append(tuple([0] + list(p))) # Adiciona a cidade fixa no início
        return permutations

    def get_work_chunk(self, chunk_size=1000):
        """
        Distribui um 'pedaço' de trabalho (permutations) para um cliente.
        Usa um lock para garantir que múltiplos clientes não peguem o mesmo trabalho.
        """
        with self.lock:
            if self.permutation_index >= self.total_permutations:
                return None # Não há mais trabalho
            
            start_index = self.permutation_index
            end_index = min(self.permutation_index + chunk_size, self.total_permutations)
            
            work_chunk = self.all_permutations[start_index:end_index]
            self.permutation_index = end_index
            
            print(f"Distribuindo chunk de permutações de {start_index} a {end_index-1}")
            return work_chunk

    def process_client_result(self, client_best_tour, client_min_distance):
        """
        Recebe o resultado de um cliente e atualiza o melhor resultado global, se for o caso.
        Usa um lock para acesso thread-safe.
        """
        with self.lock:
            if client_min_distance < self.min_overall_distance:
                self.min_overall_distance = client_min_distance
                self.best_overall_tour = client_best_tour
                print(f"Nova melhor rota encontrada: {self.format_tour(client_best_tour)} com distância {self.min_overall_distance:.2f}")

    def format_tour(self, tour_indices):
        """Converte uma lista de índices de cidades para nomes de cidades."""
        return " -> ".join([self.index_to_name[i] for i in tour_indices])

    def handle_client(self, conn, addr):
        """
        Lida com a comunicação com um cliente individual.
        """
        print(f"Conectado por {addr}")
        self.clients_connected += 1

        try:
            while True:
                work_chunk = self.get_work_chunk()
                if work_chunk is None:
                    print(f"Nenhum trabalho restante para {addr}. Encerrando conexão.")
                    conn.sendall(pickle.dumps(None)) # Sinaliza que não há mais trabalho
                    break
                
                # Envia o trabalho para o cliente
                conn.sendall(pickle.dumps({
                    'permutations': work_chunk,
                    'precomputed_distances': self.precomputed_distances
                }))

                # Espera o resultado do cliente
                data = conn.recv(4096)
                if not data:
                    print(f"Cliente {addr} desconectou.")
                    break
                
                client_result = pickle.loads(data)
                self.process_client_result(client_result['best_tour'], client_result['min_distance'])
                
        except Exception as e:
            print(f"Erro na comunicação com {addr}: {e}")
        finally:
            conn.close()
            self.clients_connected -= 1
            print(f"Conexão com {addr} fechada. Clientes ativos: {self.clients_connected}")

    def start(self):
        """
        Inicia o servidor e aguarda conexões de clientes.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            print(f"Servidor escutando em {HOST}:{PORT}")

            # Thread para imprimir o progresso periodicamente
            threading.Thread(target=self._print_progress, daemon=True).start()

            while True:
                conn, addr = s.accept()
                threading.Thread(target=self.handle_client, args=(conn, addr)).start()

    def _print_progress(self):
        """Imprime o progresso da computação a cada 10 segundos."""
        while self.permutation_index < self.total_permutations or self.clients_connected > 0:
            time.sleep(10)
            with self.lock:
                progress = (self.permutation_index / self.total_permutations) * 100
                print(f"\n--- Progresso: {progress:.2f}% concluído. Permutações processadas: {self.permutation_index}/{self.total_permutations} ---")
                if self.best_overall_tour:
                    print(f"--- Melhor rota atual: {self.format_tour(self.best_overall_tour)} Distância: {self.min_overall_distance:.2f} ---")
                else:
                    print("--- Nenhuma rota encontrada ainda ---")
        print("\n--- Todos os trabalhos distribuídos e clientes processados. Resultados finais: ---")
        if self.best_overall_tour:
            print(f"Melhor rota global: {self.format_tour(self.best_overall_tour)}")
            print(f"Distância mínima global: {self.min_overall_distance:.2f}")
        else:
            print("Nenhuma rota encontrada (possivelmente zero cidades ou erro).")


if __name__ == "__main__":
    master = TSPMaster()
    master.start()
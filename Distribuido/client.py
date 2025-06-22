# client.py
import socket
import pickle
import time
import sys

from utils.calculations import calculate_total_distance

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

class TSPWorker:
    def __init__(self):
        self.best_local_tour = None
        self.min_local_distance = float('inf')

    def connect_and_work(self):
        """
        Conecta ao servidor, recebe trabalho, processa e envia resultados.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((HOST, PORT))
                print(f"Conectado ao servidor {HOST}:{PORT}")

                while True:
                    # Recebe o trabalho do servidor
                    data = s.recv(4096)
                    if not data:
                        print("Conexão com o servidor perdida.")
                        break

                    work_package = pickle.loads(data)
                    
                    if work_package is None:
                        print("Servidor sinalizou que não há mais trabalho. Encerrando.")
                        break # Não há mais trabalho a ser feito

                    permutations = work_package['permutations']
                    precomputed_distances = work_package['precomputed_distances']
                    
                    if not permutations:
                        print("Nenhuma permutação no pacote de trabalho. Aguardando mais ou encerrando.")
                        continue # Pode ser um pacote vazio se o servidor estiver finalizando

                    print(f"Recebeu {len(permutations)} permutações para processar.")
                    
                    # Processa as permutações recebidas
                    self.best_local_tour, self.min_local_distance = self._find_best_tour_for_chunk(
                        permutations, precomputed_distances
                    )

                    # Envia o resultado de volta ao servidor
                    response = {
                        'best_tour': self.best_local_tour,
                        'min_distance': self.min_local_distance
                    }
                    s.sendall(pickle.dumps(response))
                    
                    print(f"Chunk processado. Melhor local: {self.min_local_distance:.2f}")
                    # Reinicia a melhor distância local para o próximo chunk,
                    # a menos que o cliente queira persistir o melhor de todos os chunks que já processou.
                    # Para esta solução simples, resetamos para cada chunk.
                    self.min_local_distance = float('inf')

            except ConnectionRefusedError:
                print(f"Não foi possível conectar ao servidor em {HOST}:{PORT}. Certifique-se de que o servidor está rodando.")
                sys.exit(1)
            except Exception as e:
                print(f"Ocorreu um erro no cliente: {e}")
            finally:
                print("Cliente encerrado.")

    def _find_best_tour_for_chunk(self, permutations, precomputed_distances):
        """
        Calcula a melhor rota para um determinado chunk de permutações.
        """
        current_best_tour = None
        current_min_distance = float('inf')

        for tour_indices in permutations:
            distance = calculate_total_distance(tour_indices, precomputed_distances)
            if distance < current_min_distance:
                current_min_distance = distance
                current_best_tour = tour_indices
        return current_best_tour, current_min_distance

if __name__ == "__main__":
    worker = TSPWorker()
    worker.connect_and_work()
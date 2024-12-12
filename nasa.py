import threading
import queue
import time
import random
import sys

def main():
    # le os argumentos da linha de comando
    if len(sys.argv) != 8:
        print("Uso: python3 nasa.py <N_ATRACOES> <N_PESSOAS> <N_VAGAS> <PERMANENCIA> <MAX_INTERVALO> <SEMENTE> <UNID_TEMPO>")
        return

    N_ATRACOES = int(sys.argv[1])
    N_PESSOAS = int(sys.argv[2])
    N_VAGAS = int(sys.argv[3])
    PERMANENCIA = float(sys.argv[4])
    MAX_INTERVALO = int(sys.argv[5])
    SEMENTE = int(sys.argv[6])
    UNID_TEMPO = float(sys.argv[7])

    # configurar a semente do rng
    random.seed(SEMENTE)

    # estruturas de sincronizacao
    fila = queue.Queue()
    lock = threading.Lock()

    # variaveis globais
    experiencia_atual = None
    ocupacao = 0
    tempo_total_simulacao = 0
    tempo_funcionamento = 0
    tempos_espera = {f"AT-{i + 1}": [] for i in range(N_ATRACOES)}
    pessoas_atendidas = 0

    # thread para gerar visitantes
    def gerador_pessoas():
        for i in range(1, N_PESSOAS + 1):
            experiencia_escolhida = f"AT-{random.randint(1, N_ATRACOES)}"
            chegada = time.time()
            with lock:
                fila.put((i, experiencia_escolhida, chegada))
                print(f"[Pessoa {i} / {experiencia_escolhida}] Aguardando na fila.")
            time.sleep(random.randint(1, MAX_INTERVALO) * UNID_TEMPO)

    # thread responsavel por gerir a fila e liberar as threads a acessarem atracoes
    def gestor_atracao():
        nonlocal experiencia_atual, ocupacao, tempo_funcionamento, pessoas_atendidas

        while True:
            with lock:
                if ocupacao == 0:
                    if experiencia_atual:
                        print(f"[NASA] Pausando a experiencia {experiencia_atual}.")
                        experiencia_atual = None
                        tempo_funcionamento += (time.time()*int(bool(inicio_atracao))) - inicio_atracao
                        inicio_atracao = 0

                    if pessoas_atendidas >= N_PESSOAS:
                        break

                if not fila.empty():
                    pessoa, experiencia, chegada = fila.queue[0]

                    if experiencia_atual is None or experiencia_atual == experiencia:
                        experiencia_atual = experiencia

                        if ocupacao == 0:
                            inicio_atracao = time.time()
                            print(f"[NASA] Iniciando a experiencia {experiencia_atual}.")

                        if ocupacao < N_VAGAS:
                            ocupacao += 1
                            fila.get()
                            print(f"[Pessoa {pessoa} / {experiencia}] Entrou na NASA Experiences (quantidade = {ocupacao}).")
                            threading.Thread(target=experiencia_pessoa, args=(pessoa, experiencia, chegada)).start()
                        else:
                            continue
                    else:
                        continue
                else:
                    if pessoas_atendidas >= N_PESSOAS:
                        break

    def experiencia_pessoa(pessoa, experiencia, chegada):
        nonlocal ocupacao, tempo_funcionamento, pessoas_atendidas
        tempo_espera = (time.time() - chegada)
        with lock:
            tempos_espera[experiencia].append(tempo_espera)
        
        time.sleep(PERMANENCIA * UNID_TEMPO)
        with lock:
            ocupacao -= 1
            print(f"[Pessoa {pessoa} / {experiencia}] Saiu da NASA Experiences (quantidade = {ocupacao}).")
            pessoas_atendidas += 1

    # inicializa as threads
    print("[NASA] Simulacao iniciada.")
    tempo_total_simulacao = time.time()
    gerador_thread = threading.Thread(target=gerador_pessoas)
    gerador_thread.start()

    gestor_atracao()
    gerador_thread.join()

    # calcula estatisticas
    tempo_total_simulacao = time.time() - tempo_total_simulacao
    print("[NASA] Simulacao finalizada.")
    print("\nTempo medio de espera:")
    for experiencia, tempos in tempos_espera.items():
        media = sum(tempos) / len(tempos) if tempos else 0
        print(f"{experiencia}: {(media/UNID_TEMPO)*1000:.2f}")

    taxa_ocupacao = tempo_funcionamento / tempo_total_simulacao if tempo_total_simulacao else 0
    print(f"\nTaxa de ocupacao: {taxa_ocupacao:.2f}")

if __name__ == "__main__":
    main()

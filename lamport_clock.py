from mpi4py import MPI
import random
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Inicializar o relógio lógico de Lamport
logical_clock = 0

def send_message(destination, tag):
    global logical_clock
    logical_clock += 1  # Incrementar o relógio lógico ao enviar a mensagem
    message = (logical_clock, rank)
    comm.send(message, dest=destination, tag=tag)
    print(f"Processo {rank} enviou mensagem para o processo {destination}. Clock: {logical_clock}")

def receive_message(source, tag):
    global logical_clock
    message = comm.recv(source=source, tag=tag)
    received_clock, sender_rank = message
    logical_clock = max(logical_clock, received_clock) + 1  # Atualizar o relógio lógico ao receber a mensagem
    print(f"Processo {rank} recebeu mensagem do processo {sender_rank}. Clock: {logical_clock}")

if __name__ == "__main__":
    if rank == 0:
        # Processo 0 envia mensagens para todos os outros processos
        for i in range(1, size):
            send_message(i, tag=11)
            time.sleep(random.uniform(0.1, 1.0))  # Espera aleatória para simular comportamento assíncrono
    else:
        # Outros processos recebem mensagem do processo 0
        receive_message(0, tag=11)

    # Sincronizar todos os processos
    comm.Barrier()
    print(f"Processo {rank} - Clock final: {logical_clock}")


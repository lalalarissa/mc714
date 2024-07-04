from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

token = False  # Inicialmente, nenhum processo possui o token
in_cs = False   # Indica se o processo está na seção crítica

lamport_clock = 0
request_queue = []  # Fila de requisições de entrada na seção crítica

def send_message(dest, tag, msg):
    global lamport_clock
    lamport_clock += 1
    comm.send((msg, lamport_clock), dest=dest, tag=tag)

def receive_message():
    global lamport_clock
    msg, timestamp = comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG)
    lamport_clock = max(lamport_clock, timestamp) + 1
    return msg, timestamp

def request_cs():
    global token, in_cs, request_queue

    # Adicionar próprio pedido à fila
    request_queue.append((rank, lamport_clock))

    # Enviar pedido para todos os outros processos
    for dest in range(size):
        if dest != rank:
            send_message(dest, tag=1, msg=lamport_clock)

    while not token:
        # Esperar pelo token
        msg, timestamp = receive_message()
        if isinstance(msg, str) and msg == "token":
            token = True

    # Verificar se o processo e seu relógio estão na fila antes de remover
    if (rank, lamport_clock) in request_queue:
        request_queue.remove((rank, lamport_clock))
    
    in_cs = True

def release_cs():
    global token, in_cs

    # Imprimir processo que sai da seção crítica e seu clock
    print(f"Processo {rank} saiu da seção crítica. Clock: {lamport_clock}")

    # Liberar a seção crítica
    in_cs = False

    # Enviar o token para o próximo processo na fila
    next_process = (rank + 1) % size
    send_message(next_process, tag=1, msg="token")
    token = False

if rank == 0:
    token = True  # Inicialmente, o processo 0 possui o token

# Simulação do uso da seção crítica
for _ in range(5):
    request_cs()
    print(f"Processo {rank} entrou na seção crítica. Clock: {lamport_clock}")
    # Simulação do uso da seção crítica (5 segundos)
    release_cs()



from mpi4py import MPI
import random

class Pro:
    def __init__(self, id):
        self.id = id
        self.act = True

class Ring_Election:
    def __init__(self, comm):
        self.TotalProcess = 0
        self.process = []
        self.comm = comm
    
    def initialiseRing(self):
        self.TotalProcess = self.comm.Get_size()
        self.process = [Pro(i) for i in range(self.TotalProcess)]
    
    def Election(self):
        # Simula falha aleatória de processo
        fail_process = random.randint(0, self.TotalProcess - 1)
        self.process[fail_process].act = False
        print(f"Processo {self.process[fail_process].id} falha")

        # Determina iniciador da eleição (aleatoriamente para ilustração)
        initializedProcess = random.randint(0, self.TotalProcess - 1)
        print(f"Eleicao iniciada por {initializedProcess}")

        old = initializedProcess
        newer = (old + 1) % self.TotalProcess

        while True:
            if self.process[newer].act:
                print(f"Processo {self.process[old].id} passa Eleição({self.process[old].id}) para {self.process[newer].id}")
                old = newer
            newer = (newer + 1) % self.TotalProcess
            if newer == initializedProcess:
                break

        # Determina coordenador (maior ID entre processos ativos)
        coord = self.FetchMaximum()
        print(f"Processo {self.process[coord].id} torna-se coordenador")

        old = coord
        newer = (old + 1) % self.TotalProcess
        while True:
            if self.process[newer].act:
                print(f"Processo {self.process[old].id} passa mensagem Coordenador({self.process[coord].id}) para processo {self.process[newer].id}")
                old = newer
            newer = (newer + 1) % self.TotalProcess
            if newer == coord:
                print("Fim da Eleicao ")
                break
    
    def FetchMaximum(self):
        maxId = -9999
        ind = 0
        for i in range(self.TotalProcess):
            if self.process[i].act and self.process[i].id > maxId:
                maxId = self.process[i].id
                ind = i
        return ind

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    object = Ring_Election(comm)
    object.initialiseRing()
    object.Election()

if __name__ == "__main__":
    main()

from mpi4py import MPI
import numpy as np
from time import time

# Partitionnement MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nbp = comm.Get_size()

# Taille de la matrice et du vecteur
N = 500 
if N % nbp != 0:
    if rank == 0:
        print("Erreur: N doit être divisible par le nombre de processus.")
    comm.Abort()


nloc = N // nbp

# Initialisation de la matrice
A = np.array([[(i+j) % N+1. for i in range(nloc*rank,nloc*(rank+1))] for j in range(N)])

# Initialisation du vecteur u
u = np.array([i+1. for i in range(nloc*rank, nloc*(rank+1))])

deb = time()

# Produit matrice-vecteur local
v_partial = A.dot(u)

# Somme local vecteurs
v_final = np.empty(N)

comm.Allreduce(v_partial, v_final, op=MPI.SUM)

fin = time()

temp_total = fin - deb
print(f"Partition {rank}: {temp_total}")

if rank == 0:
    print(f"N={N}, {nbp} partitions")
    #print(f"v = {v_final}")


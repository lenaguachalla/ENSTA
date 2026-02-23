import numpy as np
from mpi4py import MPI
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Length of the random array (can be changed)
len_array = 50

def bucket_sort():

    # Root process gets random array and distributes in buckets
    if rank == 0:

        array = np.random.standard_normal(len_array).tolist()
        print('array was', [round(x, 4) for x in array])
        buckets = []

        # Number of buckets equal to number of processes
        for i in range(size):
            buckets.append([])

        # Normalizing the array values to distribute them in buckets
        minimum = min(array)
        maximum = max(array)
        span = maximum - minimum

        # Distributes values into buckets according to index
        for value in array:
            index = int(size * (value - minimum) / span)
            # If value = max, index = size would be out of bounds (value is put in last bucket)
            if index == size:
                index = size - 1
            buckets[index].append(value)

    else:
        buckets = None

    # Each process receives a bucket and sorts it
    local_bucket = sorted(comm.scatter(buckets, root = 0))

    # Gathers all sorted buckets to root
    all_buckets = comm.gather(local_bucket, root = 0)

    # Merges the final sorted array
    if rank == 0:
        sortedArray = []
        for bucket in all_buckets:
            sortedArray.extend(bucket)
        print('array is', [round(x, 4) for x in sortedArray])
        
        return sortedArray

start = time.time()
sortedArray = bucket_sort()
end = time.time()

print(f'total time: {(end - start)*1000} milliseconds')

import time
from statistics import mean

import bcrypt

password = b"super secret password"
diff = 11


def time_hashing():
    t1 = time.time()
    hashed = bcrypt.hashpw(password, bcrypt.gensalt(diff))
    t2 = time.time()
    return t2 - t1


times = [time_hashing() for _ in range(10)]
print(f'Average Execution time with Difficulty: {diff} was {mean(times):.3f}s')

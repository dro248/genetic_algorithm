import random
import string
import time


x = set()
SET_SIZE = 1000000

while len(x) < SET_SIZE:
    rand_str = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(25))
    x.add(rand_str)

start = time.time()

y = list(x)

end = time.time()

print("Converting 1M Set to list in {total} seconds".format(total=(end - start)))

a = time.time()
time.sleep(1)
b = time.time()

print("sleep for a second", b-a)

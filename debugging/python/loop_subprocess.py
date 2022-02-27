import multiprocessing as mp
import time


def f():
    x = 0
    while True:
        x += 1
        print(f"x={x}")
        print("Sleeping for 1 second...")
        time.sleep(1)


if __name__ == "__main__":
    msg = "Looping"
    print(msg)
    p = mp.Process(target=f)
    p.start()
    p.join()

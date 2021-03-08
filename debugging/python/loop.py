import time

if __name__ == "__main__":
    print("Looping...")
    x = 0
    while True:
        x += 1
        print(f"x={x}")
        print("Sleeping for 1 second...")
        time.sleep(1)

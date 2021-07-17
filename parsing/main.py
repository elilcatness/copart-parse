import time

from data.copart import Copart


def main():
    start_time = time.time()
    copart = Copart()
    output = copart.get_data()
    print(len(output))
    finished = time.time()
    print('Time passed: {0:.2f}'.format(finished - start_time))


if __name__ == '__main__':
    main()

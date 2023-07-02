from time import time, sleep
from functools import wraps
import logging
from multiprocessing import Pool, cpu_count, Manager


def time_decorator(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start_time = time()
        res = f(*args)
        logging.debug(f"Execution time: {time() - start_time}s")
        return res
    return wrapper


def test():
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106,
                 1521580, 2130212, 2662765, 5325530, 10651060]
    print('Test passed! Ok!')


def find_factors(num, result_queue):
    factors = []
    for i in range(1, num + 1):
        if num % i == 0:
            factors.append(i)
    result_queue.put(factors)


@time_decorator
def sp_factorize(*numbers):
    result = []
    for num in numbers:
        factors = []
        for i in range(1, num + 1):
            if num % i == 0:
                factors.append(i)
        result.append(factors)
    return result


@time_decorator
def mp_factorize(*numbers):
    num_cores = cpu_count()
    manager = Manager()
    result_queue = manager.Queue()

    with Pool(processes=num_cores) as pool:
        processes = []
        for num in numbers:
            process = pool.apply_async(find_factors, args=(num, result_queue))
            processes.append(process)

        for process in processes:
            process.get()

    results = []
    while not result_queue.empty():
        results.append(result_queue.get())

    return results


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format="%(message)s")
    logging.warning('Single process start.')
    a, b, c, d = sp_factorize(128, 255, 99999, 10651060)
    sleep(1)
    logging.debug('Multi process start.')
    a, b, c, d = mp_factorize(128, 255, 99999, 10651060)

    # print(a)
    # print(b)
    # print(c)
    # print(d)
    # test()


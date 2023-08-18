import multiprocessing

# Function to calculate the square of a number
def calculate_square(number):
    square = number * number
    return square

# Process worker function to calculate square and return the result
def process_worker(fn, args, result_queue):
    result = fn(*args)
    result_queue.put(result)

if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5]
    result_queue = multiprocessing.Queue()
    processes = []

    for number in numbers:
        process = multiprocessing.Process(target=process_worker, args=(calculate_square,[number], result_queue))
        processes.append(process)
        process.start()

    # Wait for all processes to finish
    for process in processes:
        process.join()

    # Collect results from the queue
    total_sum = 0
    # print('entry', result_queue.get())
    while not result_queue.empty():
        total_sum += result_queue.get()
    print(f"Sum of squares: {total_sum}")

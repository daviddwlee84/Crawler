from typing import List, Callable, Any, Dict
from multiprocessing import Process, cpu_count
from multiprocessing import Queue
import json
from tqdm import tqdm

# https://stackoverflow.com/questions/37835179/how-can-i-specify-the-function-type-in-my-type-hints

from datetime import datetime, date


def json_serial(obj):
    """
    JSON serializer for objects not serializable by default json code

    https://stackoverflow.com/questions/11875770/how-to-overcome-datetime-datetime-not-json-serializable

    TODO: move this to utils
    """

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def _read_single_line(line: str, sep: str, names: List[str]):
    items = line.strip().split(sep)
    return {name: item for item, name in zip(items, names)}


def tsv_parallel_processing(filename: str, outputfile: str, function: Callable, numprocesses: int = None, keep_order: bool = False,
                            sep: str = '\t', names: List[str] = ['Url', 'DocHtmlBody', 'Language', 'Country', 'VisualTitle', 'Title', 'StaticRank1_16'], error_bad_lines: bool = False):
    """
    TODO: There is potential BUG here (Recurssion Error)

    Directly apply each line with func

    TODO: keep_order


    (X)
    1. Retrieve total line numbers
    2. split into number of threads
    3. apply function on each part of data (load file might habe problem)

    Candidate

    * pools + apply_async + async write file => the results are still in memory, not good
      * (https://pypi.org/project/aiofile/)
    * queues => multiple process for calculating, one process for write file

    https://www.machinelearningplus.com/python/parallel-processing-python/ (good material)
    https://www.blopig.com/blog/2016/08/processing-large-files-using-python/
    https://www.toptal.com/python/beginners-guide-to-concurrency-and-parallelism-in-python
    https://stackoverflow.com/questions/11983938/python-appending-to-same-file-from-multiple-threads (good material)
    https://stackoverflow.com/questions/4047789/parallel-file-parsing-multiple-cpu-cores
    https://stackoverflow.com/questions/55565509/how-to-parallel-process-a-large-file-without-load-all-in-memory
    """
    if not numprocesses:
        numprocesses = cpu_count()

    if not names:
        # TODO: assume header is in first line
        assert False, 'Currently you have to given column names.'
        pass

    def worker(in_queue: Queue, out_queue: Queue):
        """
        Keep working until get 'STOP'
        """
        for func, args in iter(in_queue.get, 'STOP'):
            result = calculate(func, *args)
            out_queue.put(result)

    def calculate(func: Callable, i: int, line: str):
        """
        Process single line and return
        """
        try:
            temp_dict = _read_single_line(line, sep, names)
        except Exception as e:
            if error_bad_lines:
                raise e
            return (i, None, False)

        result = None
        try:
            result = func(temp_dict)
            success = True
        except Exception as e:
            # print(str(e))
            success = False
        return (i, result, success)

    task_queue = Queue()
    done_queue = Queue()

    # Start worker processes
    for _ in range(numprocesses):
        Process(target=worker, args=(task_queue, done_queue)).start()

    # Assign tasks
    with open(filename, 'r', encoding='utf-8') as fp:
        for i, line in enumerate(fp):
            task_queue.put((function, (i, line)))
        total_lines = i + 1

    # Tell child processes to stop
    for _ in range(numprocesses):
        task_queue.put('STOP')

    if not outputfile:
        return

    # Get results and write file
    # https://stackoverflow.com/questions/45808140/using-tqdm-progress-bar-in-a-while-loop
    print('Total:', total_lines)
    pbar = tqdm(total=total_lines)
    i = 0
    total_success = 0
    total_fail = 0
    with open(outputfile, 'w', encoding='utf-8') as fp:
        while i < total_lines:
            idx, result, success = done_queue.get()
            # print(i, idx, result, success)
            if success:
                json.dump(result, fp, ensure_ascii=False, default=json_serial)
                fp.write('\n')
            total_success += success
            total_fail += not success
            i += 1
            pbar.update(1)
            pbar.set_description(
                f'success: {total_success}; fail: {total_fail}')

    pbar.close()


def tsv_sequential_processing(filename: str, outputfile: str, function: Callable,
                              sep: str = '\t', names: List[str] = ['Url', 'DocHtmlBody', 'Language', 'Country', 'VisualTitle', 'Title', 'StaticRank1_16'], error_bad_lines: bool = False):
    # https://stackoverflow.com/questions/16865390/why-no-lenfile-in-python/16865516
    with open(filename, 'r', encoding='utf-8') as fp:
        total_lines = sum(1 for _ in fp)

    with open(filename, 'r', encoding='utf-8') as fp:
        pbar = tqdm(fp, total=total_lines)
        total_success = 0
        total_fail = 0
        for line in pbar:
            try:
                temp_dict = _read_single_line(line, sep, names)
            except Exception as e:
                if error_bad_lines:
                    raise e
            try:
                result = function(temp_dict)
                total_success += 1
            except:
                total_fail += 1

            pbar.set_description(
                f'success: {total_success}; fail: {total_fail}')

            if outputfile:
                with open(outputfile, 'w', encoding='utf-8') as fp:
                    json.dump(result, fp, ensure_ascii=False,
                              default=json_serial)
                    fp.write('\n')

    pbar.close()


if __name__ == "__main__":
    # TODO: test
    pass

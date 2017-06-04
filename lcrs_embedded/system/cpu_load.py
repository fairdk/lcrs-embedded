"""
Generate a load on the CPU with one process per core.
"""
import logging
from multiprocessing import Process
import time

logger = logging.getLogger(__name__)

def multiple_processes_load_cpu(scan_result, duration_in_seconds):
    """
    Start a number of processes that each do simple arithmetics to
    generate a load on the CPU for a number of seconds.
    """
    def load_cpu():
        """
        Not using range(count) as that would put load on memory.
        """
        m = 1
        running = True
        while running:
            m = (m + 1) % 100000
            running = (m != 0) or (int(time.time()) - startTime < duration_in_seconds)
    
    number_of_processes = scan_result.processor_cores
    
    startTime = int(time.time())
    logger.info("Starting to generate load on CPU, time {}".format(startTime))
    processes = []
    for n in range(number_of_processes):
        process = Process(target = load_cpu, args = ( ))
        process.start()
        processes.append(process)
    for n in range(number_of_processes):
        processes[n].join()
    logger.info("Finished generating load on CPU, time {}".format(int(time.time())))


if __name__ == "__main__":
    from lcrs_embedded.models import ScanResult
    
    scan_result = ScanResult(
        processor_cores=2
    )
    multiple_processes_load_cpu(scan_result, 10)
    
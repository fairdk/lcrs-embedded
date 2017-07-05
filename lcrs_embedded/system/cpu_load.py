"""
Generate a load on the CPU with one process per core.
"""
import logging
from multiprocessing import Process
import time

logger = logging.getLogger(__name__)

def timed_cpu_load(endTime):
    """
    Add some numbers for a while.
    Could have been placed inside cpu_load below but there it
    is called within a separate process and is then not picked
    up in test coverage. Solved with a direct call in the test.
    """
    m = 1
    running = True
    while running:
        m = (m + 1) % 100000
        running = (m != 0) or (time.time() < endTime)

def cpu_load(scan_result, duration_in_seconds):
    """
    Load CPU.
    """
    
    def multiple_processes_load_cpu(duration_in_seconds):
        """
        Start a number of processes that each do simple arithmetics to
        generate a load on the CPU for a number of seconds.
        """
        number_of_processes = scan_result.processor_cores
        
        startTime = time.time()
        endTime = startTime + duration_in_seconds
        logger.info("Starting to generate load on CPU, time {}".format(startTime))
        processes = []
        for n in range(number_of_processes):
            process = Process(target = timed_cpu_load, args = (endTime,))
            process.start()
            processes.append(process)
        for n in range(number_of_processes):
            processes[n].join()
        logger.info("Finished generating load on CPU, time {}".format(time.time()))
    
    try:
        multiple_processes_load_cpu(duration_in_seconds)
        scan_result.processor_load_status = "Complete"
    except Exception as e:
        scan_result.processor_load_status = "Failed: %s %s" % (type(e), e)

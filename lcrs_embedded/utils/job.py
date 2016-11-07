import sys
import threading


class Job(threading.Thread):

    def __init__(self, output_queue, exception_queue, job_id, *args, **kwargs):
        # An async queue where we can put new output and it can be read out by
        # the parent thread or whatever
        self.output_queue = output_queue
        self.exception_queue = exception_queue
        self.job_id = job_id
        super(Job, self).__init__(*args, **kwargs)

    def run(self, *args, **kwargs):
        try:
            super(Job, self).run(*args, **kwargs)
            self.job()
        except Exception:
            exc_type, exc_obj, exc_trace = sys.exc_info()
            self.exception_queue.put(
                {'type': exc_type, 'obj': exc_obj, 'traceback': exc_trace}
            )
            raise

    def job(self):
        """
        Either set self._target (as with the typical Thread object) or
        implement this method if you inherit from the Job class.
        """
        return

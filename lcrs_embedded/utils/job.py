import threading


class Job(threading.Thread):

    def __init__(self, output_queue, job_id, *args, **kwargs):
        # An async queue where we can put new output and it can be read out by
        # the parent thread or whatever
        self.output_queue = output_queue
        self.job_id = job_id
        super(Job, self).__init__(*args, **kwargs)

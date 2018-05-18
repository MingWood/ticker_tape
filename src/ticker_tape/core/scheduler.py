import asyncio


class Scheduler(object):
    def __init__(self):
        self.schedule = None

    def find_task(self, task_name):
        for job in self.schedule:
            if job.task_name == task_name:
                return job

    def stop_task(self, task_name):
        self.find_task(task_name)['running_job'].cancel()

    def register_schedule(self, schedule):
        self.schedule = schedule

    def start_schedule(self):
        for job in self.schedule:
            job.running_job_reference(asyncio.ensure_future(job.periodic()))

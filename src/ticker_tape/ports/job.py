from abc import ABC, abstractmethod
import json

from ticker_tape.ports.loader import DataLoaderPort
from ticker_tape.adapters.pricehistory_job import PriceHistoryJob


class Job(ABC):
    @abstractmethod
    async def periodic(self):
        pass


class LiveJob(Job):
    def __init__(self,
                 adapter,
                 symbol=None,
                 loader=None,
                 frequency='daily',
                 minutes_to_look_back=None,
                 tasks=[],
                 minutes_between_runs=1,
                 **kw):
        self.adapter = adapter(symbol,
                               loader=loader,
                               frequency=frequency,
                               minutes_to_look_back=minutes_to_look_back,
                               tasks=tasks,
                               minutes_between_runs=minutes_between_runs,
                               **kw)
        self.symbol = symbol
        self.task_name = self.adapter.task_name
        self.minutes_between_runs = self.adapter.minutes_between_runs
        self.run_count = self.adapter.run_count
        self.failure_msg = self.adapter.failure_msg
        self.status = self.adapter.status
        self.tasks = self.adapter.tasks
        self.running_job = None

    def __repr__(self):
        return json.dumps({
            'task_name': self.task_name,
            'symbol': self.symbol,
            'minutes_between_runs': self.minutes_between_runs,
            'run_count': self.run_count,
            'failure_msg': self.failure_msg,
            'status': self.status,
            'tasks': [json.loads(repr(t)) for t in self.tasks],
        })

    def running_job_reference(self, job):
        self.running_job = job

    async def periodic(self):
        await self.adapter.periodic()


class LiveJobPort(LiveJob):
    def __init__(self, *args, **kw):
        super().__init__(PriceHistoryJob, *args, loader=DataLoaderPort, **kw)


if __name__ == '__main__':
    class Consumer(object):
        async def handle(self, data):
            print('handling, ', data)

    job = LiveJobPort(
        symbol='SPX',
        minutes_to_look_back=15 * 24 * 60,
        tasks=[Consumer()]
    )
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(job.periodic())

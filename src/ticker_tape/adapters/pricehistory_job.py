import asyncio
import logging

from ..util.timer import Timer


class PriceHistoryJob(object):
    def __init__(self,
                 symbol,
                 loader=None,
                 frequency='daily',
                 minutes_to_look_back=1 * 31 * 24 * 60,
                 tasks=[],
                 minutes_between_runs=1,
                 **kw):
        self.task_name = kw.get('task_name', symbol + '_' + str(minutes_to_look_back) + '_' + frequency)
        self.loader = loader(
            symbol,
            frequency=frequency,
            start=Timer.get_current_epoch_ms() - minutes_to_look_back * 60 * 1000,
            end=Timer.get_current_epoch_ms(),
        )
        self.minutes_between_runs = minutes_between_runs
        self.run_count = 0
        self.failure_msg = ''
        self.status = 'green'
        self.tasks = tasks

    async def load_and_process(self):
        data = await self.loader.load()
        for task in self.tasks:
            await task.handle(data)

    async def periodic(self):
        while True:
            self.run_count += 1
            try:
                await self.load_and_process()
                self.status = 'green'
            except Exception as emsg:
                self.status = 'red'
                self.failure_msg = str(emsg)
                logging.warning(str(emsg))

            await asyncio.sleep(self.minutes_between_runs * 60)

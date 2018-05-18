import json
import asyncio
from aiohttp import web

from ticker_tape.core.scheduler import Scheduler
from ticker_tape.core.manager import JobManager


ENV = 'dev'


class TickerServer(object):
    def __init__(self):
        self.scheduler = Scheduler()
        self.job_manager = JobManager()
        self.server = web.Application()

    async def list_tasks(self, request):
        print(self.scheduler.schedule[0].tasks[0].consumer_stats)
        return web.Response(text=json.dumps(self.scheduler.schedule))

    def _add_routes(self):
        self.server.add_routes([web.get('/', self.list_tasks)])

    def _configure_schedule(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.job_manager.load_schedule('test.yaml'))
        self.scheduler.register_schedule(self.job_manager.schedule)

    def serve_forever(self):
        self._configure_schedule()
        self.scheduler.start_schedule()
        self._add_routes()
        web.run_app(self.server)


if __name__ == "__main__":
    ticker_tape = TickerServer()
    ticker_tape.serve_forever()

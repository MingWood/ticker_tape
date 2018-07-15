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

    async def main_page(self, request):
        return web.Response(text="Up")

    async def list_tasks(self, request):
        return web.json_response(
            json.loads(
                repr(self.scheduler.schedule)
            )
        )

    async def start_schedule(self, request):
        self._configure_schedule(request.match_info['name'])
        self.scheduler.start_schedule()
        return web.Response(text="Schedule Started")

    def _add_routes(self):
        self.server.add_routes([web.get('/status', self.list_tasks)])
        self.server.add_routes([web.get('/schedule/{name}', self.start_schedule)])
        self.server.add_routes([web.get('/', self.main_page)])

    def _configure_schedule(self, name):
        schedule = 'schedules/{0}.yaml'.format(name)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.job_manager.load_schedule(schedule))
        self.scheduler.register_schedule(self.job_manager.schedule)

    def serve_forever(self):
        self._add_routes()
        web.run_app(self.server)


if __name__ == "__main__":
    ticker_tape = TickerServer()
    ticker_tape.serve_forever()

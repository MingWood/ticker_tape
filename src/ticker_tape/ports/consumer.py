from abc import ABC, abstractmethod
import json

from ticker_tape.adapters.stream_analyze_consumer import StreamPredictorConsumer
from ticker_tape.adapters.stream_export_consumer import StreamInfluxDBConsumer


class Consumer(ABC):
    @abstractmethod
    async def handle(self, payload):
        pass


class StreamConsumer(Consumer):
    def __init__(self,
                 adapter,
                 name=None,
                 algorithm=None,
                 **kw):
        self.adapter = adapter(name, algorithm=algorithm, **kw)
        self.consumer_stats = {
            'name': self.adapter.name,
            'run_count': self.adapter.run_count,
            'runs': self.adapter.runs
        }

    def __repr__(self):
        return json.dumps(self.consumer_stats)

    async def handle(self, payload):
        await self.adapter.handle(payload)


class StreamConsumerPort(StreamConsumer):
    def __init__(self, *args, **kw):
        super().__init__(StreamPredictorConsumer, *args, **kw)


class StreamExportConsumer(Consumer):
    def __init__(self,
                 adapter,
                 name=None,
                 **kw):
        self.adapter = adapter(name, **kw)
        self.consumer_stats = {
            'name': self.adapter.name,
            'run_count': self.adapter.run_count,
            'runs': self.adapter.runs
        }

    def __repr__(self):
        return json.dumps(self.consumer_stats)

    async def handle(self, payload):
        await self.adapter.handle(payload)


class StreamExportConsumerPort(StreamExportConsumer):
    def __init__(self, *args, **kw):
        super().__init__(StreamInfluxDBConsumer, *args, **kw)


if __name__ == '__main__':
    def fake_algorithm(d):
        if d > 1:
            results = 'good, no'
        else:
            results = 'bad'
        print(results, 'error')

    data = 2

    predictor = StreamPredictorConsumer(name='test', algorithm=fake_algorithm)
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(predictor.handle(data))

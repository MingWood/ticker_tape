from abc import ABC, abstractmethod
from ticker_tape.adapters.stream_analyze_consumer import StreamPredictorConsumer


class Consumer(ABC):
    @abstractmethod
    async def handle(self, payload):
        pass


class StreamConsumer(Consumer):
    def __init__(self,
                 adapter,
                 algorithm=None,
                 name=None):
        self.adapter = adapter(algorithm, name)
        self.consumer_stats = {
            'name': self.adapter.name,
            'run_count': self.adapter.run_count,
            'runs': self.adapter.runs
        }

    async def handle(self, payload):
        await self.adapter.handle(payload)


class StreamConsumerPort(StreamConsumer):
    def __init__(self, *args, **kw):
        super().__init__(StreamPredictorConsumer, *args, **kw)


if __name__ == '__main__':
    def fake_algorithm(d):
        if d > 1:
            results = 'good, no'
        else:
            results = 'bad'
        print(results, 'error')

    data = 2

    predictor = StreamPredictorConsumer(algorithm=fake_algorithm, name='test')
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(predictor.handle(data))

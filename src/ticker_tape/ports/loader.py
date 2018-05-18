from abc import ABC, abstractmethod
from ticker_tape.adapters.tda_loader import TDALoader
from ticker_tape.adapters.instruction_loader import InstructionFileLoaderAdapter


class Loader(ABC):
    @abstractmethod
    async def load(self):
        pass


class DataLoader(Loader):
    def __init__(self,
                 adapter,
                 symbol=None,
                 period='month',
                 frequency='daily',
                 start=None,
                 end=None
                 ):
        self.adapter = adapter(
            symbol,
            period=period,
            frequency=frequency,
            start=start,
            end=end
        )

    async def load(self):
        return await self.adapter.load()


class DataLoaderPort(DataLoader):
    def __init__(self, *args, **kw):
        super().__init__(TDALoader, *args, **kw)


class InstructionLoader(Loader):
    def __init__(self, adapter):
        self.adapter = adapter()

    async def load(self, path):
        await self.adapter.load(path)

    async def formatted_schedule(self, path=None):
        instruction = await self.adapter.format_schedule(path=path)

        self.check_job_top_level(instruction)
        self.check_job_meta(instruction)
        self.check_job_consumers(instruction)

        return instruction

    @staticmethod
    def check_job_top_level(instruction):
        if not isinstance(instruction, dict):
            raise ValueError('Jobs must be unique keys')

    @staticmethod
    def check_job_consumers(instruction):
        for name, job in instruction.items():
            for consumer in job['consumers']:
                if not isinstance(consumer, dict):
                    raise ValueError('Consumers must be key value pairs')

    @staticmethod
    def check_job_meta(instruction):
        for name, job in instruction.items():
            assert type(job['type']) == str
            assert type(job['symbol']) == str
            assert type(job['frequency']) == str
            assert type(job['consumers']) == list


class InstructionLoaderPort(InstructionLoader):
    def __init__(self, *args, **kw):
        super().__init__(InstructionFileLoaderAdapter, *args, **kw)


if __name__ == '__main__':
    loader = DataLoaderPort(
        symbol='SPX',
        start=1526014800000,
        end=1526285145000,
    )
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(loader.load())

    loader = InstructionLoaderPort()
    loop.run_until_complete(loader.formatted_schedule('test.yaml'))

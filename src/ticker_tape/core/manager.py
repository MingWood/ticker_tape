from ticker_tape.ports import port_factory
from ticker_tape.ports.loader import InstructionLoaderPort
from ticker_tape.core.registry import retrieve_algorithms


class ConsumerManager(object):
    def __init__(self):
        self.algorithms = retrieve_algorithms()

    def retrieve_algorithm(self, name):
        if name not in self.algorithms.keys():
            raise KeyError('algorithm selected was not found: ' + name)
        return self.algorithms[name]


class JobManager(object):
    def __init__(self):
        self.instruction = None
        self.schedule = []
        self.loader = InstructionLoaderPort()
        self.consumer_manager = ConsumerManager()

    async def load_instruction(self, path):
        self.instruction = await self.loader.formatted_schedule(path)

    def generate_consumers(self, consumers):
        configured_consumers = []
        for consumer in consumers:
            consumer_cls = port_factory(list(consumer.keys())[0])
            name = list(consumer.values())[0]

            algo = self.consumer_manager.retrieve_algorithm(name)
            configured_consumers.append(consumer_cls(algorithm=algo, name=name))

        return configured_consumers

    def generate_jobs(self):
        for name, job in self.instruction.items():
            consumers = self.generate_consumers(job.pop('consumers'))
            job_cls = port_factory(job.pop('type'))
            self.schedule.append(job_cls(**job, tasks=consumers, task_name=name))

    async def load_schedule(self, path):
        await self.load_instruction(path)
        self.generate_jobs()

        return self.schedule


if __name__ == '__main__':
    a = JobManager()

    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(a.load_schedule('test.yaml'))

    print(a.schedule)
    print(a.schedule[0].task_name)

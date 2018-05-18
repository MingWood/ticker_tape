import yaml


class InstructionFileLoaderAdapter(object):
    def __init__(self):
        self.instruction = None

    async def load(self, path):
        with open(path, 'r') as stream:
            try:
                self.instruction = yaml.load(stream)
            except yaml.YAMLError as exc:
                raise ValueError('Instruction file unreadable')

    async def format_schedule(self, path=None):
        if path or not self.instruction:
            await self.load(path)

        return self.instruction


class StreamPredictorConsumer(object):
    def __init__(self, name, algorithm=None, **kw):
        self.algorithm = algorithm
        self.name = name
        self.run_count = 0
        self.runs = []

    async def handle(self, payload):
        self.run_count += 1
        try:
            results, err = await self.algorithm(payload)
        except Exception as emsg:
            err = str(emsg)
            results = {}

        self.runs.append({
            'run_count': self.run_count - 1,
            'results': results,
            'error': err
        })

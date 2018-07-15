import json
from ..util.api import get
from ..util.constants import YEAR_TO_MINUTES, MONTH_TO_MINUTES
from ..util.datetime import datetime_to_epoch_ms


IEX_SUPPORTED_FREQUENCIES = ('daily')
IEX_SUPPORTED_TIMEFRAMES = {
    1 * YEAR_TO_MINUTES: '1y',
    2 * YEAR_TO_MINUTES: '2y',
    5 * YEAR_TO_MINUTES: '5y',
    6 * MONTH_TO_MINUTES: '6m',
    3 * MONTH_TO_MINUTES: '3m',
    1 * MONTH_TO_MINUTES: '1m'
}


def time_frame_conversion(start, end):
    minutes = (end - start) / 60
    return minutes


class IEXLoader(object):
    def __init__(self,
                 symbol,
                 frequency='daily',
                 start=None,
                 end=None):
        self.timeframe = (end - start) / 60 / 1000

        if frequency not in IEX_SUPPORTED_FREQUENCIES:
            raise ValueError('Frequency selected is not in supported options: ', str(IEX_SUPPORTED_FREQUENCIES))

        if self.timeframe not in IEX_SUPPORTED_TIMEFRAMES.keys():
            raise ValueError('Timeframe selected is not in supported options: ', str(IEX_SUPPORTED_TIMEFRAMES.keys()))

        self.host = 'https://api.iextrading.com'
        self.symbol = symbol

        self.query = '/1.0/stock/{0}/chart/{1}'.format(self.symbol.lower(), IEX_SUPPORTED_TIMEFRAMES[self.timeframe])

    async def load(self):
        resp = await get(self.host + self.query)

        if resp['status'] >= 400:
            raise ValueError('API failed: ' + resp['response'])

        data = json.loads(resp['response'])
        for tick in data:
            tick['datetime'] = datetime_to_epoch_ms(tick['date'])

        return data

import json
from ..util.api import get
from ..util.config import get_config


class TDALoader(object):
    def __init__(self,
                 symbol,
                 frequency='daily',
                 start=None,
                 end=None,
                 period='year'):
        self.host = 'https://api.tdameritrade.com/'
        self.symbol = symbol
        self.api_key = get_config('TDAmeritrade', 'API_KEY')

        self.params = {
            'apikey': self.api_key,
            'periodType': period,
            'frequencyType': frequency,
            'startDate': start,
            'endDate': end,
            'needExtendedHoursData': 'false'
        }
        self.headers = {'Authorization': ''}
        self.query = '/v1/marketdata/{0}/pricehistory'.format(self.symbol)

    async def load(self):
        resp = await get(self.host + self.query, params=self.params, headers=self.headers)
        if resp['status'] >= 400:
            raise ValueError('API failed: ' + resp['response'])

        return json.loads(resp['response'])['candles']


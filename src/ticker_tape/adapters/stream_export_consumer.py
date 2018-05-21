from influxdb import InfluxDBClient
from ticker_tape.util.config import get_config


class StreamInfluxDBConsumer(object):
    def __init__(self, name, **kw):
        self.name = name
        self.run_count = 0
        self.runs = []

        self.host = get_config('InfluxDB', 'HOST')
        self.port = get_config('InfluxDB', 'PORT')
        self.user = get_config('InfluxDB', 'USER')
        self.password = get_config('InfluxDB', 'PASSWORD')
        self.retention = get_config('InfluxDB', 'RETENTION_POLICY')
        self.ret_policy_name = 'streaming_ticker_history_ret'
        self.client = InfluxDBClient(self.host, self.port, self.user, self.password)
        self.dbname = 'streaming_ticker_history'

        self.job = {
            'type': kw.get('type'),
            'symbol': kw.get('symbol'),
            'frequency': kw.get('frequency'),
            'symbol': kw.get('symbol'),
            'minutes_to_look_back': kw.get('minutes_to_look_back'),
            'minutes_between_runs': kw.get('minutes_between_runs'),
        }

    def _ensure_db_connection(self):
        dbs = self.client.get_list_database()

        for db in dbs:
            if db['name'] == self.dbname:
                return

        self.client.create_database(self.dbname)

    def _ensure_retention_policy(self):
        policies = self.client.get_list_retention_policies(database=self.dbname)
        for policy in policies:
            if policy['name'] == self.ret_policy_name:
                return

        self.client.create_retention_policy(
            self.ret_policy_name,
            self.retention,
            3,
            database=self.dbname,
            default=True,
        )

    def _format_output(self, payload):
        time_series = []
        for tick in payload:
            point = {
                "measurement": self.name,
                "time": tick.pop('datetime'),
                "fields": tick,
                "tags": self.job,
            }
            time_series.append(point)

        return time_series

    def _write_datapoints(self, payload):
        self.client.write_points(
            self._format_output(payload),
            retention_policy=self.ret_policy_name,
            database=self.dbname,
            time_precision='ms'
        )
        return 'success', ''

    async def handle(self, payload):
        self.run_count += 1
        try:
            results, err = await self._write_datapoints(payload)
        except Exception as emsg:
            err = str(emsg)
            results = {}

        self.runs.append({
            'run_count': self.run_count - 1,
            'results': results,
            'error': err
        })

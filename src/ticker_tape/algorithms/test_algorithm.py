from ticker_tape.core.registry import register_algorithm


@register_algorithm
async def my_test_algorithm_1(data):
    print(data)
    print('Running some analysis...')
    print('Analyzing {0} datapoints'.format(len(data['response'])))
    return 'hello', 'there'

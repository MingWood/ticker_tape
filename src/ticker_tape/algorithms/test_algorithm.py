from ticker_tape.core.registry import register_algorithm


@register_algorithm
async def my_test_algorithm_1(data):
    print(data)
    print('Running some analysis...')
    print('Analyzing {0} datapoints'.format(len(data)))

    highest = data[0]['high']
    for tick in data:
        if tick['high'] > highest:
            highest = tick['high']

    return 'Highest value found: ' + str(highest), 'no errors'

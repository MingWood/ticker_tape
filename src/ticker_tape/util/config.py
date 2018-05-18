import os
from configparser import ConfigParser


def get_config(section, name, file_path=None):
    if not file_path:
        from ticker_tape.main import ENV
        file_path = ENV + '.ini'

    parser = ConfigParser()

    parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(parent, 'config', file_path)

    parser.read(file_path)
    return parser.get(section, name)

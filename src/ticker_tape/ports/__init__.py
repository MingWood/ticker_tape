from .loader import Loader
from .consumer import Consumer
from .job import Job

PORTS = [Loader, Consumer, Job]


def port_factory(port_name):
    for port in PORTS:
        for child_class in port.__subclasses__():
            if child_class.__name__ == port_name:
                return child_class.__subclasses__()[0]

import simpy


def run(until: float = 10.0) -> None:
    env = simpy.Environment()
    env.run(until=until)

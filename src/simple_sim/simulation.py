"""Simple single-server queue simulation using SimPy."""

from __future__ import annotations

from dataclasses import dataclass, field

import simpy


@dataclass
class SimulationResult:
    customers_served: int = 0
    total_wait_time: float = 0.0
    max_wait_time: float = 0.0
    wait_times: list[float] = field(default_factory=list)

    @property
    def avg_wait_time(self) -> float:
        if not self.wait_times:
            return 0.0
        return self.total_wait_time / len(self.wait_times)


def _customer(
    env: simpy.Environment,
    name: str,
    server: simpy.Resource,
    service_time: float,
    stats: SimulationResult,
) -> simpy.events.Generator:
    arrival = env.now
    with server.request() as request:
        yield request
        wait = env.now - arrival
        stats.wait_times.append(wait)
        stats.total_wait_time += wait
        stats.max_wait_time = max(stats.max_wait_time, wait)
        yield env.timeout(service_time)
    stats.customers_served += 1


def _customer_arrivals(
    env: simpy.Environment,
    server: simpy.Resource,
    interarrival: float,
    service_time: float,
    stats: SimulationResult,
) -> simpy.events.Generator:
    customer_id = 0
    while True:
        yield env.timeout(interarrival)
        customer_id += 1
        env.process(
            _customer(env, f"Customer {customer_id}", server, service_time, stats)
        )


def run(
    until: float = 100.0,
    *,
    num_servers: int = 2,
    interarrival: float = 2.0,
    service_time: float = 5.0,
) -> SimulationResult:
    """Run a queue simulation and return collected statistics."""

    env = simpy.Environment()
    server = simpy.Resource(env, capacity=num_servers)
    stats = SimulationResult()

    env.process(_customer_arrivals(env, server, interarrival, service_time, stats))
    env.run(until=until)
    return stats


def main() -> None:
    until = 100.0
    result = run(until=until)

    print(f"Simulation finished at t={until:.0f}")
    print(f"Customers served: {result.customers_served}")
    print(f"Average wait: {result.avg_wait_time:.2f}")
    print(f"Max wait: {result.max_wait_time:.2f}")


if __name__ == "__main__":
    main()

from simple_sim.simulation import run


def test_run_completes() -> None:
    result = run(until=50.0, interarrival=10.0, service_time=2.0)

    assert result.customers_served > 0
    assert result.avg_wait_time >= 0
    assert len(result.wait_times) == result.customers_served

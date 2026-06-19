from simple_sim.simulation import run


def test_run_completes() -> None:
    run(until=1.0)

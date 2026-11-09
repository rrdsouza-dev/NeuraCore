from neuracore.monitoring.tracing import tracer


def test_tracer_do_projeto_esta_disponivel() -> None:
    assert tracer is not None

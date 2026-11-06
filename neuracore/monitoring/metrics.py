"""Métricas Prometheus da aplicação."""

from prometheus_client import Counter, generate_latest

inference_requests = Counter(
    "neuracore_inference_requests_total",
    "Total de solicitações de inferência recebidas.",
)


def render_metrics() -> bytes:
    """Serializa as métricas no formato Prometheus."""
    return generate_latest()

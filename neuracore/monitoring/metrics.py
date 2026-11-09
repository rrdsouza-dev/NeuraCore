"""Métricas Prometheus da aplicação."""

from prometheus_client import Counter, Histogram, generate_latest

inference_requests = Counter(
    "neuracore_inference_requests_total",
    "Total de solicitações de inferência recebidas.",
)
inference_duration_seconds = Histogram(
    "neuracore_inference_duration_seconds",
    "Duração das solicitações de inferência em segundos.",
)


def render_metrics() -> bytes:
    """Serializa as métricas no formato Prometheus."""
    return generate_latest()

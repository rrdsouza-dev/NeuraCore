"""Ponto único para instrumentação OpenTelemetry."""

from opentelemetry import trace

tracer = trace.get_tracer("neuracore")

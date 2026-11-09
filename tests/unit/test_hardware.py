from neuracore.resources.hardware import HardwareDetector, HardwareSnapshot


def test_detector_de_hardware_nao_impede_execucao_sem_gpu() -> None:
    snapshot = HardwareDetector().snapshot()

    assert isinstance(snapshot, HardwareSnapshot)
    assert isinstance(snapshot.gpus, list)

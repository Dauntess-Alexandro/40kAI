from core.telemetry.gpu_backend import parse_nvidia_smi_csv, GpuSample


def test_parse_nvidia_smi_csv():
    text = (
        "0, NVIDIA GeForce RTX 5060 Ti, 81, 4096, 16384, 64\n"
        "1, NVIDIA GeForce RTX 2060 SUPER, 40, 2048, 8192, 55\n"
    )
    out = parse_nvidia_smi_csv(text)
    assert len(out) == 2
    g0 = out[0]
    assert isinstance(g0, GpuSample)
    assert g0.index == 0
    assert g0.name == "NVIDIA GeForce RTX 5060 Ti"
    assert g0.util == 81
    assert g0.mem_used_mb == 4096
    assert g0.mem_total_mb == 16384
    assert g0.temp_c == 64


def test_parse_nvidia_smi_csv_handles_na_and_blank():
    text = "0, GPU, [N/A], 100, 8192, [N/A]\n\n"
    out = parse_nvidia_smi_csv(text)
    assert len(out) == 1
    assert out[0].util is None
    assert out[0].temp_c is None
    assert out[0].mem_used_mb == 100

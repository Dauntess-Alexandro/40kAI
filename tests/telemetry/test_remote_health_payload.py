from tools.gmz_remote_inference_server import build_health_payload


def test_build_health_payload_includes_gpu_and_batch():
    payload = build_health_payload(
        protocol_version=1, policy_version=42, gpu_name="RTX 2060 SUPER",
        queue_depth=3, uptime_s=120, avg_batch=9.5,
        gpu_util=40, gpu_mem_used_mb=2048, gpu_mem_total_mb=8192, gpu_temp_c=55,
    )
    assert payload["kind"] == "health_check"
    assert payload["status"] == "ok"
    assert payload["gpu_util"] == 40
    assert payload["gpu_mem_used_mb"] == 2048
    assert payload["gpu_mem_total_mb"] == 8192
    assert payload["gpu_temp_c"] == 55
    assert payload["avg_batch"] == 9.5
    assert payload["policy_version"] == 42


def test_build_health_payload_tolerates_missing_gpu():
    payload = build_health_payload(
        protocol_version=1, policy_version=0, gpu_name="cpu",
        queue_depth=0, uptime_s=1, avg_batch=None,
        gpu_util=None, gpu_mem_used_mb=None, gpu_mem_total_mb=None, gpu_temp_c=None,
    )
    assert payload["status"] == "ok"
    assert payload["gpu_util"] is None
    assert payload["avg_batch"] is None


def test_gmz_build_health_payload_includes_cpu_ram():
    payload = build_health_payload(
        protocol_version=1, policy_version=7, gpu_name="RTX 2060 SUPER",
        queue_depth=0, uptime_s=5, avg_batch=None,
        gpu_util=10, gpu_mem_used_mb=512, gpu_mem_total_mb=8192, gpu_temp_c=44,
        cpu_name="Ryzen 5 1600", cpu_pct_system=38.0,
        ram_pct_system=31.0, ram_gb_system=5.0,
    )
    assert payload["cpu_name"] == "Ryzen 5 1600"
    assert payload["cpu_pct_system"] == 38.0
    assert payload["ram_pct_system"] == 31.0
    assert payload["ram_gb_system"] == 5.0


def test_gmz_build_health_payload_cpu_ram_default_none():
    payload = build_health_payload(
        protocol_version=1, policy_version=0, gpu_name="cpu",
        queue_depth=0, uptime_s=1, avg_batch=None,
        gpu_util=None, gpu_mem_used_mb=None, gpu_mem_total_mb=None, gpu_temp_c=None,
    )
    assert payload["cpu_pct_system"] is None
    assert payload["cpu_name"] is None

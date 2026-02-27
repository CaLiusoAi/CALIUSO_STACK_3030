from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(ROOT / "tools"))
import validate_stack as validator  # noqa: E402


def run_validator(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "tools/validate_stack.py", *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def test_validator_passes() -> None:
    proc = run_validator()
    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert "Stack validation passed" in proc.stdout


def test_parse_manifest_counts() -> None:
    manifest = validator.parse_manifest(ROOT / "stack.manifest.yaml")
    assert len(manifest.layers) == 8
    assert len(manifest.meta_layers) == 2
    assert "README.md" in manifest.required_artifacts


def test_invalid_manifest_order_fails() -> None:
    manifest = validator.parse_manifest(ROOT / "stack.manifest.yaml")
    bad_layers = list(manifest.layers)
    bad_layers[0], bad_layers[1] = bad_layers[1], bad_layers[0]
    bad_manifest = validator.StackManifest(
        layers=tuple(bad_layers),
        meta_layers=manifest.meta_layers,
        required_artifacts=manifest.required_artifacts,
    )
    with pytest.raises(validator.ValidationError, match="ascension order"):
        validator.validate_manifest_model(bad_manifest)


def test_missing_layer0_invariant_fails(tmp_path: Path) -> None:
    spec = tmp_path / "spec.md"
    spec.write_text("O = 10\nH = 0\nR = -∞\n", encoding="utf-8")
    (tmp_path / "layer0-default-lens").mkdir()
    target = tmp_path / "layer0-default-lens" / "spec.md"
    target.write_text(spec.read_text(encoding="utf-8"), encoding="utf-8")

    with pytest.raises(validator.ValidationError, match="StyleStep"):
        validator.check_layer0_invariants(tmp_path)

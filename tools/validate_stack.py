#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "stack.manifest.yaml"
ASCENSION_ORDER = [
    "layer0-default-lens",
    "layer1-cathedral",
    "layer2-pantheon",
    "layer3-omegaomega",
    "layer4-omega-manifold",
    "layer5-archivist",
    "layer6-ascension",
    "layer7-omegainfinity",
]


class ValidationError(RuntimeError):
    """Raised when stack validation fails."""


@dataclass(frozen=True)
class ManifestEntry:
    name: str
    module: str
    depends_on: tuple[str, ...]


@dataclass(frozen=True)
class StackManifest:
    layers: tuple[ManifestEntry, ...]
    meta_layers: tuple[ManifestEntry, ...]
    required_artifacts: tuple[str, ...]


NAME_RE = re.compile(r"^[a-z0-9\-]+$")
MODULE_RE = re.compile(r"^[A-Z0-9_]+$")


def fail(message: str) -> None:
    raise ValidationError(message)


def _parse_dep_list(raw: str) -> tuple[str, ...]:
    raw = raw.strip()
    if not raw.startswith("[") or not raw.endswith("]"):
        fail(f"invalid depends_on list: {raw}")
    inner = raw[1:-1].strip()
    if not inner:
        return tuple()
    return tuple(part.strip() for part in inner.split(","))


def _parse_entries(lines: list[str], start_idx: int) -> tuple[tuple[ManifestEntry, ...], int]:
    entries: list[ManifestEntry] = []
    i = start_idx
    while i < len(lines):
        line = lines[i]
        if re.match(r"^[a-z_]+:", line):
            break
        if not line.strip():
            i += 1
            continue

        m = re.match(r"^  - name: ([a-z0-9\-]+)$", line)
        if not m:
            fail(f"malformed manifest entry line: {line}")
        name = m.group(1)

        if i + 1 >= len(lines):
            fail(f"missing module line for entry {name}")
        module_line = lines[i + 1]
        mm = re.match(r"^    module: ([A-Z0-9_]+)$", module_line)
        if not mm:
            fail(f"missing/invalid module line for entry {name}")
        module = mm.group(1)

        depends_on: tuple[str, ...] = tuple()
        consumed = 2
        if i + 2 < len(lines):
            dep_line = lines[i + 2]
            dm = re.match(r"^    depends_on: (\[.*\])$", dep_line)
            if dm:
                depends_on = _parse_dep_list(dm.group(1))
                consumed = 3

        entries.append(ManifestEntry(name=name, module=module, depends_on=depends_on))
        i += consumed

    return tuple(entries), i


def parse_manifest(path: Path) -> StackManifest:
    if not path.exists():
        fail("missing stack.manifest.yaml")

    lines = path.read_text(encoding="utf-8").splitlines()
    i = 0
    layers: tuple[ManifestEntry, ...] = tuple()
    meta_layers: tuple[ManifestEntry, ...] = tuple()
    required_artifacts: tuple[str, ...] = tuple()

    while i < len(lines):
        line = lines[i]
        if line.startswith("layers:"):
            layers, i = _parse_entries(lines, i + 1)
            continue
        if line.startswith("meta_layers:"):
            meta_layers, i = _parse_entries(lines, i + 1)
            continue
        if line.startswith("required_artifacts:"):
            artifacts: list[str] = []
            i += 1
            while i < len(lines):
                if re.match(r"^[a-z_]+:", lines[i]):
                    break
                if not lines[i].strip():
                    i += 1
                    continue
                am = re.match(r"^  - ([\w./-]+)$", lines[i])
                if not am:
                    fail(f"malformed required artifact line: {lines[i]}")
                artifacts.append(am.group(1))
                i += 1
            required_artifacts = tuple(artifacts)
            continue
        i += 1

    if len(layers) != 8:
        fail(f"expected 8 layers, found {len(layers)}")
    if len(meta_layers) != 2:
        fail(f"expected 2 meta layers, found {len(meta_layers)}")
    if not required_artifacts:
        fail("manifest required_artifacts is empty")

    return StackManifest(layers=layers, meta_layers=meta_layers, required_artifacts=required_artifacts)


def validate_manifest_model(manifest: StackManifest) -> None:
    all_entries = list(manifest.layers) + list(manifest.meta_layers)
    names = [e.name for e in all_entries]
    modules = [e.module for e in all_entries]

    if len(set(names)) != len(names):
        fail("manifest has duplicate layer/meta names")
    if len(set(modules)) != len(modules):
        fail("manifest has duplicate module names")

    for entry in all_entries:
        if not NAME_RE.match(entry.name):
            fail(f"invalid entry name: {entry.name}")
        if not MODULE_RE.match(entry.module):
            fail(f"invalid module name: {entry.module}")

    known_names = set(names)
    for entry in all_entries:
        for dep in entry.depends_on:
            if dep not in known_names:
                fail(f"unknown dependency '{dep}' in entry '{entry.name}'")

    layer_order = [e.name for e in manifest.layers]
    if layer_order != ASCENSION_ORDER:
        fail("manifest layer order does not match canonical ascension order")


def check_required_files(root: Path, entry_name: str, required_artifacts: tuple[str, ...], strict_nonempty: bool) -> None:
    layer_dir = root / entry_name
    if not layer_dir.is_dir():
        fail(f"missing directory: {entry_name}")

    for rel in required_artifacts:
        artifact = layer_dir / rel
        if not artifact.exists():
            fail(f"missing artifact: {entry_name}/{rel}")
        if strict_nonempty and artifact.is_file() and artifact.stat().st_size == 0:
            fail(f"empty artifact file: {entry_name}/{rel}")


def check_layer0_invariants(root: Path) -> None:
    content = (root / "layer0-default-lens" / "spec.md").read_text(encoding="utf-8")
    required = ("O = 10", "H = 0", "R = -∞", "StyleStep -> H' = 0")
    for token in required:
        if token not in content:
            fail(f"layer0 invariant missing: {token}")


def check_ascension_sequence(root: Path) -> None:
    content = (root / "layer6-ascension" / "spec.md").read_text(encoding="utf-8")
    expected = " -> ".join(ASCENSION_ORDER)
    if expected not in content:
        fail("ascension sequence missing or malformed")


def check_module_names(root: Path, entries: tuple[ManifestEntry, ...]) -> None:
    for entry in entries:
        tla = root / entry.name / "tla" / "module.tla"
        text = tla.read_text(encoding="utf-8")
        marker = f"---- MODULE {entry.module} ----"
        if marker not in text:
            fail(f"module declaration mismatch in {entry.name}/tla/module.tla (expected {entry.module})")


def validate_stack(root: Path, strict_nonempty: bool = True) -> None:
    manifest = parse_manifest(root / "stack.manifest.yaml")
    validate_manifest_model(manifest)

    all_entries = manifest.layers + manifest.meta_layers
    for entry in all_entries:
        check_required_files(root, entry.name, manifest.required_artifacts, strict_nonempty=strict_nonempty)

    check_layer0_invariants(root)
    check_ascension_sequence(root)
    check_module_names(root, all_entries)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate CALIUSO stack integrity")
    parser.add_argument("--no-strict-nonempty", action="store_true", help="allow empty files")
    args = parser.parse_args()

    try:
        validate_stack(ROOT, strict_nonempty=not args.no_strict_nonempty)
    except ValidationError as exc:
        print(f"ERROR: {exc}")
        return 1

    print("Stack validation passed: manifest, layers, artifacts, invariants, and modules are consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

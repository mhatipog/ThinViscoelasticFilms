#!/usr/bin/env python3
"""Short linear-instability check against the Newtonian thin-film limit.

Runs in a temporary copy: the original physical parameters and working tree
are not changed.
"""
import math
import re
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def change_time_parameter(source, name, value):
    pattern = rf"(?m)^(\s*REAL\(DP\),\s*PARAMETER\s*::\s*{name}\s*=\s*)[^!\r\n]+"
    updated, count = re.subn(pattern, lambda match: match.group(1) + value + " ",
                              source)
    if count != 1:
        raise RuntimeError(f"Expected one declaration of {name}, found {count}")
    return updated


def run(command, directory):
    result = subprocess.run(command, cwd=directory, text=True, capture_output=True,
                            check=False, timeout=120)
    if result.returncode:
        raise RuntimeError(f"{' '.join(command)} failed:\n"
                           + (result.stdout + "\n" + result.stderr)[-2500:])


def parse_rows(path, skip_header=False):
    lines = path.read_text().splitlines()
    if skip_header:
        lines = lines[1:]
    return [[float(x.replace("D", "E")) for x in line.split()]
            for line in lines if line.strip()]


def slope(x, y):
    avg_x = sum(x) / len(x)
    avg_y = sum(y) / len(y)
    return sum((a - avg_x) * (b - avg_y) for a, b in zip(x, y)) / sum(
        (a - avg_x) ** 2 for a in x
    )


def main():
    with tempfile.TemporaryDirectory(prefix="thin-film-check-") as temp:
        source = Path(temp) / "source"
        shutil.copytree(ROOT, source, ignore=shutil.ignore_patterns(
            ".git", ".github", "output", "*.o", "*.mod", "ThinVEFilm", "__pycache__"
        ))
        times = source / "domain_time.f90"
        content = times.read_text()
        for name, value in (("t_end", "0.30d0"),
                            ("dt_init", "0.005d0"),
                            ("t_out", "0.05d0")):
            content = change_time_parameter(content, name, value)
        times.write_text(content)
        (source / "output").mkdir()
        run(["make", "-C", "build", "all"], source)
        run(["./build/ThinVEFilm"], source)

        rows = parse_rows(source / "output" / "range.dat", skip_header=True)
        profile = parse_rows(source / "output" / "resLastOut.dat")
        if len(rows) < 4 or len(profile) != 1000:
            raise RuntimeError("Incomplete simulation output")

        times = [row[0] for row in rows]
        amplitudes = [(row[2] - row[4]) / 2 for row in rows]
        if any(a <= 0 for a in amplitudes):
            raise RuntimeError("Nonpositive instability amplitude")
        observed = slope(times, [math.log(a) for a in amplitudes])

        # Reference: the original default coefficients in paras.f90.
        k = 2 * math.pi / 10.0
        hstar = 0.005
        epsilon = 0.01
        kappa = (1 - math.cos(math.radians(15.0))) / (0.5 * hstar * epsilon**2)
        pi_prime = -3 * hstar**3 + 2 * hstar**2
        expected = k * k * (kappa * pi_prime - k * k) / 3.0

        error = abs(observed / expected - 1)
        mass_error = abs(math.fsum(row[1] for row in profile) / len(profile) - 1)
        print(f"Linear growth: computed={observed:.8f}, theory={expected:.8f}, "
              f"relative error={error:.4%}")
        print(f"Final mass relative error: {mass_error:.3e}")
        if error >= 0.005 or mass_error >= 1e-9:
            raise AssertionError("Thin-film numerical regression failed")


if __name__ == "__main__":
    main()

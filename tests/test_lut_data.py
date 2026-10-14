"""Regression checks for the pressure blocks in the 2006 CHF tables."""

import json
import re
import runpy
import sys
import types
import unittest
from pathlib import Path
from unittest import mock

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
FULL_PRESSURES = [0.1, 0.3, 0.5, *range(1, 22)]
SPARSE_PRESSURES = [0.1, 0.3, 0.5, 1, 2, 3, 5, 7, 10, 12, 14, 16, 18, 20, 21]


class LutDataTests(unittest.TestCase):
    def test_matlab_pressure_grids(self):
        for source, expected in (
            (ROOT / "Groeneveld_LUT.m", FULL_PRESSURES),
            (ROOT / "AllCorrelations" / "Groeneveld_LUT.m", SPARSE_PRESSURES),
        ):
            match = re.search(r"P_lut\s*=\s*\[(.*?)\];", source.read_text(), re.DOTALL)
            self.assertIsNotNone(match, str(source))
            grid = []
            for value in re.split(r"[,\s]+", match.group(1).replace("...", "")):
                if not value:
                    continue
                if ":" in value:
                    start, end = map(int, map(float, value.split(":")))
                    grid.extend(range(start, end + 1))
                else:
                    grid.append(float(value))
            self.assertEqual(grid, expected)

    def test_table_shapes_and_sparse_subset(self):
        full = np.loadtxt(ROOT / "2006LUTdata.txt")
        sparse = np.loadtxt(ROOT / "AllCorrelations" / "2006LUTdata.txt")
        self.assertEqual(full.shape, (21 * len(FULL_PRESSURES), 23))
        self.assertEqual(sparse.shape, (21 * len(SPARSE_PRESSURES), 23))

        for sparse_index, pressure in enumerate(SPARSE_PRESSURES):
            full_index = FULL_PRESSURES.index(pressure)
            np.testing.assert_array_equal(
                sparse[sparse_index * 21 : (sparse_index + 1) * 21],
                full[full_index * 21 : (full_index + 1) * 21],
            )

        # G = 2000 kg/m2s is row 8; x = 0 is column 7.
        self.assertEqual(full[FULL_PRESSURES.index(10) * 21 + 8, 7], 4131)

    def test_sdf_exporter_uses_the_full_pressure_grid(self):
        # The installed SDF package is not needed to inspect the exported arrays.
        sdf_stub = types.SimpleNamespace(
            Dataset=lambda *args, **kwargs: None,
            Group=lambda *args, **kwargs: None,
            save=lambda *args, **kwargs: None,
        )
        with mock.patch.dict(sys.modules, {"sdf": sdf_stub}):
            exported = runpy.run_path(str(ROOT / "2006LUT_to_SDF.py"))

        pressure_index = list(exported["P"]).index(10e6)
        self.assertEqual(exported["q"].shape, (21, 23, 24))
        self.assertEqual(exported["q"][8, 7, pressure_index], 4_131_000)

    def test_notebook_uses_the_full_pressure_grid(self):
        notebook = json.loads((ROOT / "2006LUT_to_sdf.ipynb").read_text(encoding="utf-8"))
        cells = ["".join(cell["source"]) for cell in notebook["cells"]]
        axes = next(cell for cell in cells if "# Pressure range" in cell)
        reshape = next(cell for cell in cells if "# Convert the imported array" in cell)
        namespace = {"np": np, "q_raw": np.loadtxt(ROOT / "2006LUTdata.txt") * 1e3}
        exec(axes, namespace)
        exec(reshape, namespace)

        pressure_index = list(namespace["P"]).index(10e6)
        self.assertEqual(namespace["q"].shape, (21, 23, 24))
        self.assertEqual(namespace["q"][8, 7, pressure_index], 4_131_000)

    def test_sdf_exporter_rejects_incomplete_table(self):
        sdf_stub = types.SimpleNamespace()
        with mock.patch.dict(sys.modules, {"sdf": sdf_stub}):
            with mock.patch.object(np, "loadtxt", return_value=np.zeros((315, 23))):
                with self.assertRaisesRegex(ValueError, "Expected LUT shape"):
                    runpy.run_path(str(ROOT / "2006LUT_to_SDF.py"))


if __name__ == "__main__":
    unittest.main()

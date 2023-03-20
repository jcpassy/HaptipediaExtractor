from glob import glob
import os
from pathlib import Path
from shutil import rmtree
import subprocess
import sys

from unittest import TestCase


class TestCaseValidation(TestCase):
    """Class for the validation tests."""

    ROOT_DIR = Path(__file__).parent
    DATA_DIR = ROOT_DIR / "data"

    def setUp(self):
        self.exe = sys.executable
        self.assertTrue(self.DATA_DIR.is_dir())

    def test_extraction(self):
        """Helper to execute a script."""

        output_dir = self.ROOT_DIR / "output"
        output_dir.mkdir(parents=True, exist_ok=True)
        # Define command
        command = [
            self.exe,
            "src/main.py",
            "-i",
            str(self.DATA_DIR),
            "-o",
            str(output_dir),
            "-d",
            "/work/src/pdffigures2"]

        # Run command
        with open(os.devnull) as dev_null, \
                open(output_dir / 'stdout.txt', 'wb+') as stdout, \
                open(output_dir / 'stderr.txt', 'wb+') as stderr:

            r_code = subprocess.call(
                command,
                stdin=dev_null,
                stdout=stdout,
                stderr=stderr)

            stdout.seek(0)
            stderr.seek(0)
            if r_code:
                message = f'Return code was {r_code}.\nOUT:\n{stdout.read()}\nERR:\n{stderr.read()}'
                raise RuntimeError(message)

        # Check output folder
        main_folder = output_dir / 'Large Workspace Haptic Devices -A New Actuation Approach'
        self.assertTrue(main_folder.is_dir())
        fig_folder = main_folder / 'Figures'
        self.assertTrue(fig_folder.is_dir())

        # Expected number of figures and captions
        num_figs = 15

        for ext in ["png", "txt"]:
            self.assertEqual(len(glob(str(fig_folder / ("*." + ext)))), num_figs)

        # Delete folder -  we keep it in case something fails for debugging
        rmtree(output_dir)

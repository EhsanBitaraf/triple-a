from triplea.cli.export_pretrain_llm import export_llm
import os
import json
from venv import logger
from click.testing import CliRunner

import pytest

class TestExportPreTrainLLM:

    def test_export_pretrain_llm(self):
        output_dir = "ff"
        runner = CliRunner()
        result = runner.invoke(
            export_llm,
            [
                r"ff",
                "--merge=false",
                "--bar=true",
                "--limit=10"
            ]
        )

        assert result.exit_code == 0
        assert "Task Done" in result.output

        # Assert that the output file exists
        assert os.path.exists(output_dir)

        # Clean up the output file
        # os.remove(output_dir)

    def test_export_pretrain_llm_with_no_dir(self):
        output_dir = "ff2"
        runner = CliRunner()
        result = runner.invoke(
            export_llm,
            [
                "--merge=false",
                "--bar=true",
                "--limit=10"
            ]
        )

        assert result.exit_code == 2
        assert "Missing argument 'OUTPUT_DIRECTORY'" in result.output


    
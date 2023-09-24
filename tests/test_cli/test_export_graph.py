from triplea.cli.export_graph import export_graph
import os
import json
from venv import logger
from click.testing import CliRunner

import pytest

class TestExportGraph:


    def test_export_graph_article_author_affiliation_graphml(self):
        output_file = "output.graphml"
        runner = CliRunner()
        result = runner.invoke(
            export_graph,
            [
                "--generate", "article-author-affiliation",
                "--format", "graphml",
                "--output", output_file,
                "--bar", "True",
                "--removed", "True"
            ]
        )

        assert result.exit_code == 0
        assert "Remove duplication in Nodes & Edges." in result.output
        assert "Save temp file with duplication." in result.output

        # Assert that the output file exists
        assert os.path.exists(output_file)

        # Clean up the output file
        os.remove(output_file)

    def test_export_graph_article_topic_gexf(self):
        output_file = "output.gexf"
        runner = CliRunner()
        result = runner.invoke(
            export_graph,
            [
                "--generate", "article-topic",
                "--format", "gexf",
                "--output", output_file,
                "--bar", "True",
                "--removed", "True"
            ]
        )

        assert result.exit_code == 0
        assert "Remove duplication in Nodes & Edges." in result.output
        assert "Save temp file with duplication." in result.output

        # Assert that the output file exists
        assert os.path.exists(output_file)

        # Clean up the output file
        os.remove(output_file)

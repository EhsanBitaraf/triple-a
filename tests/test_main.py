import os
import pathlib
from click.testing import CliRunner
from triplea.cli.main import cli
from triplea import __version__
import networkx as nx
from tests.fixtures.graph_52 import graph52
from triplea.config.settings import SETTINGS
from triplea.config.settings import ROOT


def test_cli_version():
  runner = CliRunner()
  result = runner.invoke(cli, ['--version'])
  v= f'version  {__version__}' + '\n'
  # print(v)
  # print(result.output)
  assert result.exit_code == 0
  assert result.output == v

# if __name__ == "__main__":
#   test_cli_version()

def test_path():
  # root = pathlib.Path(__file__).resolve()
  root = os.path.join(ROOT, "tests" , "fixtures")
  # assert ROOT / "tests" == ""
  assert root == root
   

def test_fixture_graph52(graph52):
    assert isinstance(graph52, nx.Graph)
    assert len(graph52.nodes) == 962
    assert len(graph52.edges) == 1460
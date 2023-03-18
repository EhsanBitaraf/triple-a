from click.testing import CliRunner
from triplea.cli.main import cli
from triplea import __version__


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
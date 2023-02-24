import click
from triplea.cli.main import cli


@cli.command('export_graph',help = 'Export Graph.')
@click.option("--generate", "-g" , "generate_type",type=click.Choice(['tool1', 'tool2', 'tool3']), multiple=False, help="Generate graph and export.")
@click.option("--format", "-f" , "format_type",type=click.Choice(['tool1', 'tool2', 'tool3']), multiple=False, help="Generate graph and export.")

def export(generate_type,format_type):
    print(generate_type)
    pass
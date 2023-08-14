from tool import get_all_filesize
from tool import python_du

import asyncio
import click

@click.command()
@click.option('-p','--path','path',help='--path [PATH/TO/MONITOR/FOLDER]')
@click.option('-o','--output', 'output', help='--output [PATH/TO/OUTPUT/FILE]')
def main(path: str, output: str) -> None:

    # Create event
    loop = asyncio.get_event_loop()

    # Get User Usage
    user_file_map = loop.run_until_complete(
        get_all_filesize("/workpool/*/*")
    )

    # get folder size
    data = loop.run_until_complete(
        python_du(user_file_map)
    )

    # output result to csv
    data.to_csv(output)

if __name__ == "__main__":

    main()

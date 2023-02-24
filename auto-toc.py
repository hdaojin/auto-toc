"""
Name: auto-toc.py
Description: Automatically gererate a table of contents for the lists of markdown files.
Author: hdaojin
Date: 2023.02.23
Update: 2023.02.23
Version: 0.0.1
"""

import sys
from pathlib import Path
import click
import markdown


def process_file(file):
    # Get the metadata of the markdown file.
    md = markdown.Markdown(extensions=['meta'])
    md.convert(file.read_text(encoding='utf-8'))
    # md.Meta is a dict where the value is a list.
    md_metadata = md.Meta
    # Convert the list to a string.
    md_metadata = { key: ''.join(value) for key, value in md_metadata.items() }
    # Get the title of the markdown file from task name in metadata.
    file_title = md_metadata.get('task', file.stem)
    # Get the link of the markdown file from the file path.
    file_link = file.relative_to(top_dir).as_posix()

    return file_title, file_link


def process_dir(top_dir, output_file):
    # sort files by modified time
    sorted_entries = sorted(top_dir.glob('*.md'), key=lambda p: (p.is_file(), p.stat().st_mtime))
    for entry in sorted_entries:
        # don't include hidden files and output file
        if entry.name.startswith('.') or entry.name.lower() == output_file.lower():
            continue
        if entry.is_dir():
            process_dir(entry, output_file)

        if entry.is_file():
            if entry.suffix.lower() == '.md':
                process_file(entry)
    return file_title, file_link



@click.command()
# @click.option('-e', '--exclude', multiple=True, help='Exclude file or directory') 
@click.option('-o', '--output', type=click.File('w', encoding='utf-8'), help='Output file')
@click.argument('directory', default='.', nargs=1, type=click.Path(exists=True, dir_okay=True, file_okay=False))
def generate_toc(output, directory):
    """
    Automatically generate a table of contents for the lists of markdown files.
    """

    process_dir(directory, exclude, output)

    if output is None:
         print(f'* [{md_title}]({md_link})')
    else:
        output.write(f'* [{md_title}]({md_link})\r ')

    # # Using the name of the directory as the title of the table of contents.
    # toc_title = p.stem

    # # Using the name of the subdirectory as the title of the category.
    # category_title = [ x for x in p.iterdir() if x.is_dir() and x.name != '.git' ]
    

    # # Get the list of markdown files in the specified directory with subdirectories.
    # files = Path(directory).rglob('*.md')
    # print(files)
    # # Sort the files by modified time.
    # files = sorted(files, key=lambda x: x.stat().st_mtime)
    # for file in files:
    #     md_metadata = get_metadata(file)
    #     # Get the title of the markdown file from task name in metadata.
    #     md_title = md_metadata.get('task', file.stem)
    #     # Get the link of the markdown file from the file path.
    #     md_link = file.relative_to(directory).as_posix()
    #     # Write the link to the output file or stdout if not specified.


if __name__ == '__main__':
    generate_toc()
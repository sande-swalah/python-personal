# Project Management CLI Tool

This is a Python command-line application to manage users, projects, and tasks. It demonstrates object-oriented design, CLI interaction, and built-in JSON persistence (no separate module required).

## Features

- Create and list users
- Add projects to users
- Add tasks to projects and mark them complete
- Persist data to a JSON file (`data.json`) via internal helper functions
- Pretty CLI output using [rich](https://pypi.org/project/rich/)

## Installation

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

Run commands via the module entrypoint:

```bash
python -m src.cli add-user "Alice" alice@example.com
python -m src.cli list-users
python -m src.cli add-project 1 "Build API" --description "API for team"
python -m src.cli list-projects 1
# filter projects by keyword
python -m src.cli list-projects 1 --search api
python -m src.cli add-task 1 1 "Write tests"
python -m src.cli list-tasks 1 1
python -m src.cli complete-task 1 1 1
```
Data is saved to `data.json` in the project root.

## Testing

```bash
pytest
```

## Structure

```
src/
    models.py
    cli.py
tests/
    test_models.py
    test_cli.py
requirements.txt
README.md
```

## Notes

- The `rich` package is used for nicer terminal tables.
- Users, projects, and tasks have simple serialization methods for JSON.
- CLI built with `argparse` and supports subcommands.

Feel free to extend or improve this tool!

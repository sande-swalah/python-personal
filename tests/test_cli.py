import os
import json
import tempfile
import subprocess
import sys

from src import cli


def setup_module(module):
    # use temporary file for persistence
    cli.DATA_FILE = os.path.join(tempfile.gettempdir(), 'test_data.json')
    try:
        os.remove(cli.DATA_FILE)
    except OSError:
        pass


def teardown_module(module):
    try:
        os.remove(cli.DATA_FILE)
    except OSError:
        pass


def run_cli_command(args):
    # run using the current python interpreter
    full = [sys.executable, '-m', 'src.cli'] + args
    res = subprocess.run(full, capture_output=True, text=True)
    return res


def test_add_and_list_user():
    r = run_cli_command(['add-user', 'Charlie', 'charlie@example.com'])
    assert 'Created user' in r.stdout

    r2 = run_cli_command(['list-users'])
    assert 'Charlie' in r2.stdout

    with open(cli.DATA_FILE, 'r') as f:
        data = json.load(f)
    assert data['users'][0]['name'] == 'Charlie'


def test_search_projects():
    # add a project that will match and one that won't
    run_cli_command(['add-project', '1', 'Alpha Project'])
    run_cli_command(['add-project', '1', 'Beta'])
    r = run_cli_command(['list-projects', '1', '--search', 'alpha'])
    assert 'Alpha Project' in r.stdout
    assert 'Beta' not in r.stdout

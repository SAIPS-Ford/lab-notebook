import shutil

from runs.database import DataBase
from runs.logger import UI
from runs.shell import Bash
from runs.tmux_session import TMUXSession
from runs.util import nonempty_string


def add_subparser(subparsers):
    parser = subparsers.add_parser('killall', help='Destroy all runs.')
    parser.add_argument(
        '--assume-yes',
        '-y',
        action='store_true',
        help='Don\'t ask permission before performing operations.')
    parser.add_argument(
        '--root',
        help='Custom path to directory where config directories (if any) are automatically '
        'created',
        type=nonempty_string)
    return parser


@UI.wrapper
@DataBase.wrapper
def cli(db, root, *args, **kwargs):
    runs = [e.path for e in db.all()]
    db.logger.check_permission('\n'.join(
        map(str, ["Runs to be removed:", *runs, "Continue?"])))
    bash = Bash(logger=db.logger)
    for run in db.all():
        TMUXSession(run.path, bash).kill()
    db.delete()
    db.path.unlink()
    shutil.rmtree(str(root), ignore_errors=True)

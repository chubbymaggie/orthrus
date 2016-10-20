import unittest
from orthrus.commands import *
from orthrusutils.orthrusutils import *

class TestOrthrusShow(unittest.TestCase):

    description = 'Test harness'
    orthrusdirname = '.orthrus'
    config = {'orthrus': {'directory': orthrusdirname}}
    # abconf_file = orthrusdirname + '/conf/abconf.conf'

    # Add
    def test_add_early_exit(self):
        args = parse_cmdline(self.description, ['add', '--job=main @@', '-s=./seeds'])
        cmd = OrthrusAdd(args, self.config)
        self.assertFalse(cmd.run())

    # Remove
    def test_remove_early_exit(self):
        # Job ID does not matter since exit precedes job ID validation
        args = parse_cmdline(self.description, ['remove', '-j', '123'])
        cmd = OrthrusRemove(args, self.config)
        self.assertFalse(cmd.run())

    # Start
    def test_start_early_exit(self):
        args = parse_cmdline(self.description, ['start', '-j', '123'])
        cmd = OrthrusStart(args, self.config)
        self.assertFalse(cmd.run())

    # Stop
    def test_stop_early_exit(self):
        args = parse_cmdline(self.description, ['stop', '-j', '123'])
        cmd = OrthrusStop(args, self.config)
        self.assertFalse(cmd.run())

    # Triage
    def test_triage_early_exit(self):
        args = parse_cmdline(self.description, ['triage', '-j', '123'])
        cmd = OrthrusTriage(args, self.config)
        self.assertFalse(cmd.run())

    # Coverage
    def test_coverage_early_exit(self):
        args = parse_cmdline(self.description, ['coverage', '-j', '123'])
        cmd = OrthrusCoverage(args, self.config)
        self.assertFalse(cmd.run())

    # Show
    def test_show_early_exit(self):
        args = parse_cmdline(self.description, ['show', '-j', '123'])
        cmd = OrthrusShow(args, self.config)
        self.assertFalse(cmd.run())
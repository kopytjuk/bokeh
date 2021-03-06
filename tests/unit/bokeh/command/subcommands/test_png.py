#-----------------------------------------------------------------------------
# Copyright (c) 2012 - 2020, Anaconda, Inc., and Bokeh Contributors.
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Boilerplate
#-----------------------------------------------------------------------------
import pytest ; pytest

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

# Standard library imports
import argparse
import os

# Bokeh imports
import bokeh.command.subcommands.png as scpng
from _util_subcommands import basic_scatter_script
from bokeh._testing.util.filesystem import TmpDir, WorkingDir, with_directory_contents
from bokeh.command.bootstrap import main

#-----------------------------------------------------------------------------
# Setup
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
# General API
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Dev API
#-----------------------------------------------------------------------------

def test_create() -> None:
    import argparse
    from bokeh.command.subcommand import Subcommand

    obj = scpng.PNG(parser=argparse.ArgumentParser())
    assert isinstance(obj, Subcommand)

def test_name() -> None:
    assert scpng.PNG.name == "png"

def test_help() -> None:
    assert scpng.PNG.help == "Create standalone PNG files for one or more applications"

def test_args() -> None:
    assert scpng.PNG.args == (

        ('files', dict(
            metavar='DIRECTORY-OR-SCRIPT',
            nargs='+',
            help="The app directories or scripts to generate PNG for",
            default=None,
        )),


        ('--height', dict(
            metavar='HEIGHT',
            type=int,
            help="The desired height of the exported layout obj only if it's a Plot instance",
            default=None,
        )),

        ('--width', dict(
            metavar='WIDTH',
            type=int,
            help="The desired width of the exported layout obj only if it's a Plot instance",
            default=None,
        )),

        (('-o', '--output'), dict(
            metavar='FILENAME',
            action='append',
            type=str,
            help="Name of the output file or - for standard output."
        )),

        ('--args', dict(
            metavar='COMMAND-LINE-ARGS',
            nargs=argparse.REMAINDER,
            help="Any command line arguments remaining are passed on to the application handler",
        )),

    )

def test_no_script(capsys) -> None:
    with (TmpDir(prefix="bokeh-png-no-script")) as dirname:
        with WorkingDir(dirname):
            with pytest.raises(SystemExit):
                main(["bokeh", "png"])
        out, err = capsys.readouterr()
        too_few = "the following arguments are required: DIRECTORY-OR-SCRIPT"
        assert err == """usage: bokeh png [-h] [--height HEIGHT] [--width WIDTH] [-o FILENAME]
                 [--args ...]
                 DIRECTORY-OR-SCRIPT [DIRECTORY-OR-SCRIPT ...]
bokeh png: error: %s
""" % (too_few)
        assert out == ""

@pytest.mark.selenium
def test_basic_script(capsys) -> None:
    def run(dirname):
        with WorkingDir(dirname):
            main(["bokeh", "png", "scatter.py"])
        out, err = capsys.readouterr()
        assert err == ""
        assert out == ""

        assert set(["scatter.png", "scatter.py"]) == set(os.listdir(dirname))

    with_directory_contents({ 'scatter.py' : basic_scatter_script }, run)

@pytest.mark.selenium
def test_basic_script_with_output_after(capsys) -> None:
    def run(dirname):
        with WorkingDir(dirname):
            main(["bokeh", "png", "scatter.py", "--output", "foo.png"])
        out, err = capsys.readouterr()
        assert err == ""
        assert out == ""

        assert set(["foo.png", "scatter.py"]) == set(os.listdir(dirname))

    with_directory_contents({ 'scatter.py' : basic_scatter_script }, run)

@pytest.mark.selenium
def test_basic_script_with_output_before(capsys) -> None:
    def run(dirname):
        with WorkingDir(dirname):
            main(["bokeh", "png", "--output", "foo.png", "scatter.py"])
        out, err = capsys.readouterr()
        assert err == ""
        assert out == ""

        assert set(["foo.png", "scatter.py"]) == set(os.listdir(dirname))

    with_directory_contents({ 'scatter.py' : basic_scatter_script }, run)

@pytest.mark.selenium
def test_basic_script_with_output_stdout(capsysbinary) -> None:
    def run(dirname):
        with WorkingDir(dirname):
            main(["bokeh", "png", "--output", "-", "scatter.py"])
        out, err = capsysbinary.readouterr()
        assert len(err) == 0
        assert len(out) > 0
        assert out.startswith(b'\x89PNG')

        assert set(["scatter.py"]) == set(os.listdir(dirname))

    with_directory_contents({ 'scatter.py' : basic_scatter_script }, run)

@pytest.mark.selenium
def test_basic_script_with_multiple_png_plots(capsys) -> None:
    def run(dirname):
        with WorkingDir(dirname):
            main(["bokeh", "png", "scatter1.py", "scatter2.py", "scatter3.py"])
        out, err = capsys.readouterr()
        assert err == ""
        assert out == ""

        assert set(["scatter1.png", "scatter2.png", "scatter3.png", "scatter1.py", "scatter2.py", "scatter3.py"]) == set(os.listdir(dirname))

    with_directory_contents({ 'scatter1.py' : basic_scatter_script,
                              'scatter2.py' : basic_scatter_script,
                              'scatter3.py' : basic_scatter_script, },
                            run)

#-----------------------------------------------------------------------------
# Private API
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Code
#-----------------------------------------------------------------------------

import subprocess

from django.core.management import call_command


def test_options_added(mocker):
    run = mocker.patch.object(subprocess, "run")
    call_command("dbshell")
    run.assert_called_once()
    PGOPTIONS = run.call_args[1]["env"]["PGOPTIONS"]
    assert "search_path" in PGOPTIONS

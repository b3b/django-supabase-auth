import subprocess

from django.core.management import call_command


def test_options_added(mocker):
    run = mocker.patch.object(subprocess, "run")
    call_command("dbshell")
    run.assert_called_once()
    PGOPTIONS = run.call_args[1]["env"]["PGOPTIONS"]
    assert "search_path" in PGOPTIONS


def test_dbshell_search_path_outputs_expected_result(db, capfd):
    call_command(
        "dbshell", "--", "--no-align", "--tuples-only", "-c", "show search_path;"
    )
    search_path = capfd.readouterr().out.strip().split(",")
    assert search_path == ["django", "public", "auth", "extensions"]


def test_dbshell_tcp_keepalives_idle_outputs_expected_value(db, capfd):
    call_command(
        "dbshell",
        "--",
        "--no-align",
        "--tuples-only",
        "-c",
        "show tcp_keepalives_idle;",
    )
    assert int(capfd.readouterr().out.strip()) == 75

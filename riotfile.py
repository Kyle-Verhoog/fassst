from riot import Venv, latest


venv = Venv(
    pys=[3.9],
    venvs=[
        Venv(
            name="test",
            command="pytest {cmdargs}",
            pkgs={
                "pytest-benchmark": latest,
            },
        ),
        Venv(
            pys=[3.9],
            name="fmt",
            command="black .",
        ),
    ],
)

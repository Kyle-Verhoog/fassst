from riot import Venv, latest


venv = Venv(
    pys=3.9,
    venvs=[
        Venv(
            pys=[
                3.8,
                3.9,
            ],
            name="test",
            command="pytest {cmdargs}",
            pkgs={
                "pytest-benchmark": latest,
            },
        ),
        Venv(
            name="fmt",
            venvs=[
                Venv(
                    name="black",
                    command="black {cmdargs}",
                ),
                Venv(
                    name="fmt",
                    command="black .",
                ),
            ],
        ),
    ],
)

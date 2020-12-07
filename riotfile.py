from riot import Venv, latest


venv = Venv(
    pys=3.9,
    venvs=[
        Venv(
            pys=[
                3.8,
                3.9,
            ],
            pkgs={
                "pytest": latest,
                "pytest-benchmark": latest,
            },
            venvs=[
                Venv(
                    name="test",
                    command="pytest --benchmark-disable {cmdargs}",
                ),
                Venv(
                    name="bench",
                    command="pytest --benchmark-group-by=param {cmdargs}",
                ),
            ],
        ),
        Venv(
            pkgs={
                "black": "==20.8b1",
            },
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

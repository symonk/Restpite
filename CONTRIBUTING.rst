Contributing
----

 .. code-block:: console

    git clone git@github.com:symonk/restpite.git
    cd restpite
    python -m venv .venv
    source .venv/bin/activate
    pip install -e ".[testing]"
    pre-commit install
    # make a branch and apply changes
    tox -e linting, py38
    push changes to upstream branch and open a pull request!

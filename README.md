# Bls Verification Contract

This is an implementation of the bls signature verification using solidity

# Installing

You need to setup two environments due to the fact that the tests were written in python

# Python stack setup

The project uses a Python stack for unit tests. It is suggested to use `pipenv` (https://pipenv.pypa.io/en/latest/) to manage dependencies.

Once `pipenv` is installed:

```
$ pipenv --python $PATH_TO_PY_38 shell
# once inside the virtualenv
$ pipenv install
```

# JS Stack
Install truffle (https://github.com/trufflesuite/truffle)

# Testing 

Start truffle, compile and migrate code
```
         bash $ truffle develop
truffle_shell $ compile
truffle_shell $ migrate
```

On another shell, run with the python virtual environment setup, run:

```
$ pytest -n auto tests
```

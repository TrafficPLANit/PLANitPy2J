# Creating a PLANit-Python setup for Pip

We use `setuptools` to create a setup for easy installation via pip. To do so, the `setup.py` outlines 
this process in the root dir of this project.

We can create a binary distribution in the /dist directory by running (make sure it is empty because it won't 
delete old files)

```cmd
python setup.py sdist bdist_wheel
```

> in case it does not run, you probably need to install setuptools wheel first via: `python -m pip install 
> --user --upgrade setuptools wheel`

For more information on setuptools, please visit the [setuptools website](https://setuptools.readthedocs.io/en/latest/setuptools.html)

For a tutorial on how to setup your own packaging process, see for example this [Python tutorial](https://packaging.python.org/tutorials/packaging-projects/)

## Test.PyPi

Before anyone should ever attempt to register a release on production via PyPi, it should be tested first on 
Test.PyPi (these have separate accounts).

In the tutorial mentioned earlier, there is a suggestion on packaging  projects, which states that we can 
upload our candidate release distribution via twine using the following command

```cmd
python -m twine upload -u __token__ -p INSERTTHETOKEN --repository testpypi dist/*
```

> In case twine is not installed, run `python -m pip install --user --upgrade twine` first

However, when using a username of `__token__` and then copying the generated token (from test.pypi website) 
into the prompt can cause an error. This likely is a bug. To solve this we recommend using the following 
command instead where you explicitly state the user and password in the command line:

```cmd
python -m twine upload -u ___username___ -p ___password___ --repository testpypi dist/*
```

> you can only gain access if you have an account, for example with your own user name. 
> The password you use for the account can be used to upload your packages, e.g. PLANit1234, etc.

Before you test if the distribution works properly. Make sure you are working in a virtual 
environment (see next section), so that the package is only installed there.

## PyPi

The motions you go through to upload your distribution to test.PyPi also hold for uploading your 
distribution to the actual PyPi.

> Only proceed with this when you are certain your release is working!

The only difference with test.PyPi is that we do not provide a --repository handle as the default is 
PyPi. Hence, to upload call

```cmd
python -m twine upload -u ___username___ -p ___password___ dist/*
```

to install we can leave out the additional index and simply call

```cmd
pip install PLANit-Python
```

### Switching to a virtual environment

For detailed information on virtual environments see Pythons' [virtual environment documentation](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

The below can be found in the mentioned tutorial, here we quickly reiterate the main points for a 
Windows installation of Python:

Since we use Python 3, we can use `venv` for this purpose. If you haven't created a virtual environment 
for this project do so via:

```cmd
python -m venv env  
```

This will create a local python installation in the /env directory. It should be included in the 
.gitignore already, so it won't affect any commits.

Activate it, so that we are working on the virtual environment while testing via 

```cmd
.\env\Scripts\activate
```

Your command line is now prefixed with (env) indicating we moved to the virtual environment. You can leave 
the environment via

```cmd
deactivate 
```

### Installing a test distribution

We can now try and install our test distribution via

```
pip install --no-cache-dir -i https://test.pypi.org/simple/ PLANit-Python==<explicit version number>
```

> Note that we must provide the extra index url because otherwise it will try and install from pypi rather than test.pypi.
> As a result it is possible that the dependencies cannot be installed properly, try manually installing them
> from regular pip installs, if that works, and then the pip install with the testpypi index works as well it should
> also work for a production version.

You can uninstall the test distribution via

```
python -m pip uninstall PLANit-Python
```

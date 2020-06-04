# PLANitPy2J
Python part of the PLANit Java/Python interface

PLANitPy2J aims to provide a Python interface into the PLANit project allowing users to parse inputs, create projects, run projects, and persist results all via a Python shell while the underlying PLANit code utilizes the Java VM for its algorithms.

The interaction with Java is made available via a seaprate project PLANitJ2Py. In PLANitJ2Py we implemented the gateway that allows the interaction between Python and Java. When creating your planit python project, a java call is made to bootstrap the java side.

We utilise py4j (www.p4j.org) to establish the connection between Java and Python. On the Python side, we provide Python wrapper classes around the Java objects such that the user is not exposed to the Java internals.  

# Getting Started

If you want to use PLANit-Python as a user, please refer to the online documentation. This readme is intended solely for developers.

# Dependency on Java Projects

There is a directory "rsc" which holds JAR files for the Java projects.  The "rsc" directory contains JAR files from the following three PLANit Java projects (and one thrid party jar) on which PLANitPy2J depends.

* PLANit
* PLANitIO
* PLANitJ2Py

Thirs party dependencies:

* Py4J

This project uses Java methods in these JAR files.  If you make changes to any of the Java projects to support the Python side, you must recompile the Java project and place the updated jar in this directory.

Note that as long as you have all projects (Python and Java) residing in the same directory, the POMs in the Java projects will attempt to copy the compiled jar files to the python rsc directory ensuring consistency.

# Versioning

Whenever a change in version occurs for either the planit jars or the py4j jar, the new version(s) must be explicitly identified in this project. We do so in the `src/planit/version.py`. 

We must make sure that our version numbering folllows the naming conventions outlined in [PEP0440](https://www.python.org/dev/peps/pep-0440/) because otherwise we are not able to distribute our version via pip. 

By updating the variables to the new version it ensures that:

1) The gateway bootstraps the Java entry point with the right jars in its classpath
2) The setup.py (see [Setup](./#setup)) that is used to create a binary release for pip include the right version number

Failing to do this will cause the runs to fail.

# Py4J

PLANitPy2J relies on Py4J for its interface with the underlying PLANit code which is programmed in Java. The Py4J code gateway and entry point are hidden from the user via the PLANit class which instantiates the Java gateway server by invoking an external subprocess call. The functionality of the gateway is provided in the Py4J jar file which is included in the "rsc" directory.

For more information on Py4J, please see www.py4j.org

# Conceptual differences compared to PLANit-Java

Current design choices for this Python based PLANit module include

* Only a single PLANit Python instance can be active as the Java interface is created statically. 
* Only a single traffic assignment, network, zoning, demands can be instantiated on the project. More advanced configurations currently require the use of the native Java code
* Only the native PLANit I/O format can be used, if you want to use a third-party/custom input/output format you'll have to use the native Java code instead
* Python Wrappers for the Java classes are utilized to ensure that Python coding conventions regarding methods/variables apply. Hence, the Python interface of PLANit is not a 1:1 copy of the Java source but rather a Pythonic interpretation geared towards maximum usability and minimum configuration 

# Current limitations and peculiarities

It seems that Py4j cannot deal with variable argument lists for methods. The reflection does not seem to work in those cases at least in case of the variable arguments being enums. Therefore avoid using those on the Java side at all times if they are exposed to the user on the Python side

## Dealing with the mapping of enums between Java and Python
It is not difficult to instantiate a Java enum using Py4J, however it has to go through the gateway instance like the following gateway.jvm.<java_packages>.<Enum_name>.<EnumField> This is very cumbersome and unintuitive from a user perspective which we want to avoid in our wrappers. Therefore we only want to use Python enums which then under the hood are converted into
their Java counterpart and passed on. The problem is that constructing a Java enum depends on the named variable for the gateway which may change over the lifetime of this project. To avoid such dependencies we instead create all Java Enums on the Java side instead via PLANitJ2Py.createEnum(String canonicalEnumName, String EnumFieldName).

Each Python enum that mimics a Java enum we implement with an additional method java_class_name() (See PLANitEnums.py). We utilize the field value (string) and this method (java canonical class name) to pass on plain strings to the Java side which in turn creates the enum via reflection and returns it. The Enum is then passed in as a parameter to the underlying java call that is being made for the method at hand hiding all details from the user while still using the same conceptual approach as we do in the Java source.

```Python
planIt.assignment.activate_output(OutputType.LINK)
```

with 

```Python
class OutputType(Enum):
    LINK = "LINK"
    
    def java_class_name(self) -> str:
        return "org.planit.output.OutputType"   
```

In activate_output we then call the java side to create the enum and pass on the method call

```Python
    def activate_output(self, output_type : OutputType):
        output_type_instance = GatewayState.python_2_java_gateway.entry_point.createEnum(output_type.java_class_name(),output_type.value)
        self._java_counter_part.activateOutput(output_type_instance)
```

While the Java side creates the enum via reflection

```Java
    public Enum createEnum(String enumCanonicalName, String EnumEntryName) throws ClassNotFoundException, PlanItException {
        Class<?> enumClass = Class.forName(enumCanonicalName);
        if(!enumClass.isEnum()) {
            throw new PlanItException("Class is not an enum");
        }
        return Enum.valueOf((Class<Enum>)enumClass,EnumEntryName);        
    }
```

# Developing for PLANitPy2J

## Preparation

How to install Py4j as a module on your Python installation is discussed in detail on <https://www.py4j.org/install.html>

How to install Python can be found on <https://www.python.org/downloads/>. We are currently using Python version 3.7, but the code has been tested on Python 3.6.

## Testing and running PLANitPy2J in Python

If PLANitPy2J is to be run from the command line, Python must be installed on the computer.  If it is to be run from Eclipse, the PyDev plugin must also be installed.

Make sure that the py4j version used in J2Py and this project are the same as the one used in your local python installation when you intend to run planit-python scripts outside of your IDE.

The Python code uses the following Python libraries:

* Py4j
* Pandas
* unittest
* traceback

Install these onto your computer using Python's "pip install" facility if you have not already done so. Similarly, install pip if you haven't already done so.

A test case is made available under src/examples/basic/basic.py.  It uses src/examples/basic/input as it project directory, and a macroscopicinput.xml input file is located in this directory.  
This is a duplicate of the same testcase in PLANitIO. It contains a very simple network with three origins and destinations without any route choice, shaped in the form of a triangle (Tipi). It can be used to test if the PLANitPython interface is setup correctly.

The directory src/planit/tests contains a file test_suite.py which contains several Python unit tests (currently six).  This file uses the test_utils.py file (in the test_util package) to set up a run PLANit from Python.  

To run test_suite.py from Eclipse using PyDev, right-click it and select Run as/Python unit-test.  To run from the command prompt, navigate to the directory where it is stored (<path_of_project>/src/tests) and enter "python test_suite.py".

The tests in test_suite.py use XML input files and CSV comparison files in  sub-directories of the directory "testcases".  This directory is an exact copy of the equivalent one in the PLANitIO directory src/test/resources. 
 
All the Python unit tests have an exact Java equivalent in PLANitIO.  However there are far fewer unit tests in Python than in Java.  Whereas the Java unit tests are intended to verify that the model results are correct for a variety of inputs, the Python unit tests exists to verify that the Python interface sends the correct values to Java.
In theory we could create many more Python unit tests using the files in the testcases directory, but in Python we only need a few to test the reading from and writing to files are working.

The __init__() method of the PLANit.py class can take an argument project_path which tells it where to find the XML input file and put the CSV output files.  This corresponds to the Java, where the PLANitIO constructor requires an equivalent argument.
If the project_path argument is omitted, the current directory (i.e. where the PLANit.py file is located) is used.

# Creating a Setup

We use setuptools to create a setup for easy installation via pip. To do so, `setup.py` outlines this process in the root dir of this project.

We can create a binary distribution in the /dist directory by running (make sure it is empty because it won't delete old files)

```python
python setup.py sdist bdist_wheel
```

> in case it does not run, you probably need to install setuptools wheel first via: `python -m pip install --user --upgrade setuptools wheel`

For more information on setuptools, please visit the [setuptools website](https://setuptools.readthedocs.io/en/latest/setuptools.html)

For a tutorial on how to setup your own packaging process, see for example this [Python tutorial](https://packaging.python.org/tutorials/packaging-projects/)

## Test.PyPi

Before we put any release on production via PyPi, we test it first on Test.PyPi (these have separate accounts).

Note that the suggestion in the tutorial on packaging  projects states that we can upload our candidate release distribution via twine through

```python
python -m twine upload --repository testpypi dist/*
```

> In case twine is not installed, run `python -m pip install --user --upgrade twine` first

However, when using a username of `__token__` and then copying the generated token (from test.pypi website) into the prompt can cause an error. This likely is a bug. to solve this use the following command instead where you explicitly state the user and password in the command line:

```python
python -m twine upload -u __token__ -p INSERTTHETOKEN --repository testpypi dist/*
```

Before you test if the distribution works properly. Make sure you are working in a virtual environment, so that the package is only installed there.

### Switching to a virtual environment

For detailed information on virtual environments see Pythons' [virtual environment documentation](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

The below can be found in the mentioned tutorial, here we quickly reiterate the main points for a Windows installation of python:

Since we use Python 3, we can use `venv` for this purpose. If you haven't created a virtual environment for this project do so via:

```python
python -m venv env
``` 

This will create a local python installation in the /env directory. It should be included in the .gitignore already, so it won't affect any commits.

Activate it, so that we are working on the virtual environment while testing via 

```python
.\env\Scripts\activate
``` 

Your command line is now prefixed with (env) indicating we moved to the virtual environment. You can leave the environment via

```python
deactivate 
```

### installing a test distribution

We can now try and install our test distribution via

```
pip install PLANit-Python --extra-index-url https://test.pypi.org/simple/
```

> Note that we must provide the extra index url because otherwise it will try and install the dependency on py4j from test.pypi, instead of using the one on pypi.

You can uninstall the test distribution via

```
python -m pip uninstall PLANit-Python
```

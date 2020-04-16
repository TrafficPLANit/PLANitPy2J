# PLANitPy2J
Python part of the PLANit Java/Python interface

PLANitPy2J aims to provide a Python interface into the PLANit project allowing users to parse inputs, create projects, run projects, and persist results all via a Python shell while the underlying PLANit code utilizes the Java VM for its algorithms.

## Py4J

PLANitPy2J relies on Py4J for its interface with the underlying PLANit code which is programmed in Java. The Py4J code gateway and entry point
are hidden from the user via the PLANit class which instantiates the Java gateway server by invoking an external subprocess call. The functionality of the gateway is provided in the Py4J jar file (py4j0.10.9.jar) which is included in the "rsc" directory..

### Installation

The Py4J version used in the Java side of this project is mentioned in the POM as a dependency. If you intend to run Python scripts as well you have to make sure that the Python installation has the same Py4j library installation as the one used in Eclipse otherwise mismatches will occur.

How to install Py4j as a module on your Python installation is discussed in detail on <https://www.py4j.org/install.html>

How to install Python can be found on <https://www.python.org/downloads/>. We are currently using Python version 3.7, but the code has been tested on Python 3.6.

# Dependence on Java Projects

There is a directory "rsc" which holds JAR files for the Java projects.  The "rsc" directory contains JAR files from the following three PLANit Java projects:

* PLANit
* PLANitIO
* PLANitJ2Py

This project uses Java methods in these JAR files.  You must create these jar files and put them in this directory before running the Python code.  The Maven POM files for the Java projects put a copy of the JAR files in this directory when they are run.  Or the user can copy over the JAR files directly.

## PLANitPy2J

Current design choices for this Python based PLANit module include

* Only a single PLANit Python instance can be active as the Java interface is created statically. 
* Only a single traffic assignment, network, zoning, demands can be instantiated on the project. More advanced configurations currently require the use of the native Java code
* Only the native PLANit I/O format can be used, if you want to use a third-party/custom input/output format you'll have to use the native Java code instead
* Python Wrappers for the Java classes are utilized to ensure that Python coding conventions regarding methods/variables apply. Hence, the Python interface of PLANit is not a 1:1 copy of the Java source but rather a Pythonic interpretation geared towards maximum usability and minimum configuration 

## Current limitations

### on PLANit side

### on Py4j side
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

# Examples

Currently the examples are not complete nor fully functional but to give an idea an example of what a Pythonic PLANit configuration roughly will look like a partial example is provided below:

```python
from PLANit import PLANit
from PLANitEnums import *

planIt = PLANit(".\\input")
planIt.set(Assignment.TRADITIONAL_STATIC)
planIt.assignment.set(PhysicalCost.BPR)
planIt.assignment.set(VirtualCost.FIXED)
planIt.assignment.output_configuration.set_persist_only_final_Iteration(True)

planIt.run()
```

## Testing and running PLANitPy2J in Python

If PLANitPy2J is to be run from the command line, Python must be installed on the computer.  If it is to be run from Eclipse, the PyDev plugin must also be installed.

The Python code uses the following Python libraries:

* Py4j
* Pandas
* unittest
* traceback

Install these onto your computer using Python's "pip install" facility if you have not already done so.

A test case is made available under src/examples/basic/basic.py.  It uses src/examples/basic/input as it project directory, and a macroscopicinput.xml input file is located in this directory.  
This is a duplicate of the same testcase in PLANitIO. It contains a very simple network with three origins and destinations without any route choice, shaped in the form of a triangle (Tipi). It can be used to test if the PLANitPython interface is setup correctly.

The directory src/planit/tests contains a file test_suite.py which contains several Python unit tests (currently six).  This file uses the test_utils.py file (in the test_util package) to set up a run PLANit from Python.  

To run test_suite.py from Eclipse using PyDev, right-click it and select Run as/Python unit-test.  To run from the command prompt, navigate to the directory where it is stored (<path_of_project>/src/tests) and enter "python test_suite.py".

The tests in test_suite.py use XML input files and CSV comparison files in  sub-directories of the directory "testcases".  This directory is an exact copy of the equivalent one in the PLANitIO directory src/test/resources. 
 
All the Python unit tests have an exact Java equivalent in PLANitIO.  However there are far fewer unit tests in Python than in Java.  Whereas the Java unit tests are intended to verify that the model results are correct for a variety of inputs, the Python unit tests exists to verify that the Python interface sends the correct values to Java.
In theory we could create many more Python unit tests using the files in the testcases directory, but in Python we only need a few to test the reading from and writing to files are working.

The __init__() method of the PLANit.py class can take an argument project_path which tells it where to find the XML input file and put the CSV output files.  This corresponds to the Java, where the PLANitIO constructor requires an equivalent argument.
If the project_path argument is omitted, the current directory (i.e. where the PLANit.py file is located) is used.

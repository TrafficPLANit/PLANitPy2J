# Release Log

PLANitPy2J releases.  The Python interface for PLANit.

## 0.3.0

* Rename PLANit() to Planit() to keep things simple #6
* Split PLANit() from project, instead make it a property. Now instantiating PLANit() creates a project and reads network etc. This should not be the case since we are adding more functionality to PLANit which might not result in a project, i.e. converters #5
* Added support for creating converters so that we can convert networks etc in python from XtoY #4
* OutputProperty LinkCost renamed to LinkSegmentCost (planit/#9)
* OutputProperty LinkType not correctly defined, should be segment based (planit/#8)
* added norm based gap function (planit/#65)
* added support for inflow/outflow properties alongside the already existing flow property (planit/#66)
* initialCosts are not properly implemented. They require more flexibility (period agnostic/specific parsing, registration on assignment separate and again timeperiod specific or agnostic and unrelated to parsing) (planit/#68)
* added support for overriding units in output type configuration #10
* added support for user based setting of the used gapfunction #9
* update packages to conform to new domain org.goplanit.* #11

## 0.2.0

* Rename RouteIdType to PathIdType (PlanitPy2J/#1)
* add LICENSE.TXT to each repository so it is clearly licensed (planit/#33)
* changes to be compatible, i.e., compilable, with PLANit changes for version 0.2.0

## 0.1.0

* Move repository to new location (www.github.com/trafficplanit/PLANitPy2J)
* Create Python library installer (#3)

## 0.0.4

* Create tests that set/get every configurable option of every component on Python side (#1)
* Renamed project to PLANitJ2Py and rename PLANitPythonRunner to PLANitPy2J (#2)
* Support all user configurable java options in Python interface (#3)
* Technical documentation PLANitPy2J/PLANitJ2Py (#4)  
* Python library installer added (#5)
* Output formatter can be activated before assignment is set (#6)
* Accessing any output type configuration activates the corresponding output type if it is not already active (#7)
* Deactivate output types added (#8)
* Initial costs no longer require assignment to be set (#12)
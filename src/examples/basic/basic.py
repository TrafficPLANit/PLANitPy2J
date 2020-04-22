#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" All "objects", i.e. non getters/setters are to be made available by the Python approach that simply access the variable, i.e.,
    planIt.<var_name>.
    
    The getters/setters of primitives,strings, etc. are directly passed on to Java albeit in Python coding convention, i.e.,
    planIt.assignment.output_configuration.set_persist_only_final_Iteration(True)
    
    Main choices are configured using Python enums and appropriate set methods, i.e.,
    planIt.set(Assignment.TRADITIONAL_STATIC). This will create the assignment instance that subsequently is made available on the parent
    instance.
"""

__author__ = "Mark Raadsen"
__copyright__ = "Copyright 2019, The PLANit Project"
__credits__ = ["Mark Raadsen"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Mark Raadsen"
__email__ = "mark.raadsen@sydney.edu.au"
__status__ = "Prototype" 

import os, sys
this_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(this_path + "\\..\\..")

from planit import PLANit
from planit import TrafficAssignment
from planit import PhysicalCost
from planit import VirtualCost
from planit import Smoothing
from planit import OutputType
from planit import OutputFormatter

# start the planit journey
plan_it = PLANit(this_path + ".\\input")
# choose the assignment
plan_it.set(TrafficAssignment.TRADITIONAL_STATIC)
# ----- BELOW THE DEFAULTS ARE EXPLICITLY SET BUT ARE IN FACT OPTIONAL-------    <---- NOT YET IMPLEMENTED AS DEFAULTS SO CURRENTLY NOT OPTIONAL
plan_it.assignment.set(PhysicalCost.BPR)
plan_it.assignment.physical_cost.set_default_parameters(0.5, 4.0)
plan_it.assignment.set(VirtualCost.FIXED)
plan_it.assignment.set(Smoothing.MSA)
plan_it.assignment.activate_output(OutputType.LINK)
plan_it.assignment.gap_function.stop_criterion.set_max_iterations(500)
plan_it.assignment.gap_function.stop_criterion.set_epsilon(0.001)
plan_it.assignment.output_configuration.set_persist_only_final_Iteration(True)
# ----- END DEFAULTS --------------------------------

#deactivate file output
plan_it.deactivate_formatter(OutputFormatter.PLANIT_IO)

plan_it.run()
""" Not complete continue here for a full blown example of all properties! """
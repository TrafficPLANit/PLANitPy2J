import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../..', 'src'))

import gc
import unittest
from planit import *

ABSOLUTE_PATH = os.path.dirname(__file__)
ABSOLUTE_PATH_TEST_DATA = os.path.join(ABSOLUTE_PATH, '..', '..', 'testdata')
ABSOLUTE_PATH_TEST_DATA_WEBSITE = os.path.join(ABSOLUTE_PATH_TEST_DATA, 'website_examples')

class TestSuiteWebsiteExamples(unittest.TestCase):

    def test_getting_started(self):
        project_path = os.path.join(ABSOLUTE_PATH_TEST_DATA_WEBSITE, 'getting_started')
        plan_it = Planit()
        planit_project = plan_it.create_project(project_path)

        # COMPONENTS
        planit_project.set(TrafficAssignment.TRADITIONAL_STATIC)
        planit_project.assignment.set(PhysicalCost.BPR)
        planit_project.assignment.set(VirtualCost.FIXED)
        planit_project.assignment.set(Smoothing.MSA)

        # CONFIGURE COST COMPONENT
        # 	BPR Travel time function
        alpha = 0.9
        beta = 4.5
        planit_project.assignment.physical_cost.set_default_parameters(alpha, beta)

        # CONFIGURE OUTPUT
        planit_project.assignment.output_configuration.set_persist_only_final_Iteration(True)

        # RUN ASSIGNMENT
        planit_project.run()
        gc.collect()

if __name__ == '__main__':
    unittest.main()

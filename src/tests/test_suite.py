import os, sys
this_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(this_path + "\\..")

import gc
import unittest
from test_utils import Helper
from planit import OutputType

class TestSuite(unittest.TestCase):
      
    @classmethod
    def setUpClass(cls):
        cls.test_data_path = this_path  + "\\..\\..\\testcases\\"
    
    def test_route_choice_2_initial_costs_500_iterations(self):
        """Unit test for route 2 with initial costs and 500 iterations (corresponds to testRouteChoice2InitialCosts500Iterations() in Java)
        """
        project_path = self.test_data_path + "route_choice\\xml\\test2initialCosts500iterations"
        description = "testRouteChoice2initialCosts"
        csv_file_name = "Time Period 1_500.csv"
        od_csv_file_name = "Time Period 1_499.csv"
        xml_file_name = "Time Period 1.xml"
        initial_costs_file_location = self.test_data_path + "route_choice\\xml\\test2initialCosts500iterations\\initial_link_segment_costs.csv"
        max_iterations = 500
        epsilon = 0.0000000001
        Helper.run_test(max_iterations, epsilon, description, 1, initial_costs_file_location, None, 0, None, 1, project_path)       
        Helper.delete_file(OutputType.LINK, description, xml_file_name, project_path)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name, project_path))        
        Helper.delete_file(OutputType.PATH, description, xml_file_name, project_path)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name, project_path))        
        Helper.delete_file(OutputType.OD, description, xml_file_name, project_path)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name, project_path))
        gc.collect()
  
    def test_route_choice_2_initial_costs_one_iteration_three_time_periods(self):
        """Unit test for route 2 with three time periods (corresponds to testRouteChoice2InitialCostsOneIterationThreeTimePeriods() in Java)
        """
        print("Running test_route_choice_2_initial_costs_one_iteration_three_time_periods")
        project_path = self.test_data_path + "route_choice\\xml\\test2initialCostsOneIterationThreeTimePeriods"
        description = "test2initialCostsOneIterationThreeTimePeriods"
        csv_file_name1 = "Time Period 1_1.csv"
        od_csv_file_name1 = "Time Period 1_0.csv"
        csv_file_name2 = "Time Period 2_1.csv"
        od_csv_file_name2 = "Time Period 2_0.csv"
        csv_file_name3 = "Time Period 3_1.csv"
        od_csv_file_name3 = "Time Period 3_0.csv"
        xml_file_name1 = "Time Period 1.xml"
        xml_file_name2 = "Time Period 2.xml"
        xml_file_name3 = "Time Period 3.xml"
        max_iterations = 1
        initial_link_segment_locations_per_time_period = {}
        initial_link_segment_locations_per_time_period[0] = self.test_data_path + "route_choice\\xml\\test2initialCostsOneIterationThreeTimePeriods\\initial_link_segment_costs_time_period_1.csv"
        initial_link_segment_locations_per_time_period[1] = self.test_data_path + "route_choice\\xml\\test2initialCostsOneIterationThreeTimePeriods\\initial_link_segment_costs_time_period_2.csv"
        initial_link_segment_locations_per_time_period[2] = self.test_data_path + "route_choice\\xml\\test2initialCostsOneIterationThreeTimePeriods\\initial_link_segment_costs_time_period_3.csv"
        epsilon = 0.001
        Helper.run_test(max_iterations, epsilon, description, 1, None, None, 0, initial_link_segment_locations_per_time_period, 2, project_path)
        Helper.delete_file(OutputType.LINK, description, xml_file_name1, project_path)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name1, project_path))
        Helper.delete_file(OutputType.LINK, description, xml_file_name2, project_path)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name2, project_path))
        Helper.delete_file(OutputType.LINK, description, xml_file_name3, project_path)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name3, project_path))
        Helper.delete_file(OutputType.PATH, description, xml_file_name1, project_path)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name1, project_path))
        Helper.delete_file(OutputType.PATH, description, xml_file_name2, project_path)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name2, project_path))
        Helper.delete_file(OutputType.PATH, description, xml_file_name3, project_path)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name3, project_path))
        Helper.delete_file(OutputType.OD, description, xml_file_name1, project_path)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name1, project_path))
        Helper.delete_file(OutputType.OD, description, xml_file_name2, project_path)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name2, project_path))
        Helper.delete_file(OutputType.OD, description, xml_file_name3, project_path)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name3, project_path))
        gc.collect()

    def test_basic_shortest_path_algorithm_a_to_c(self):
        """ Unit test 2 using basic network (corresponds to testBasicShortestPathAlgorithmAtoC() in Java)
        """
        print("Running test_basic_shortest_path_algorithm_a_to_c")
        project_path = self.test_data_path + "basic\\xml\\test2";
        description = "testBasic2";
        csv_file_name = "Time Period 1_2.csv";
        od_csv_file_name = "Time Period 1_1.csv";
        xml_file_name = "Time Period 1.xml";
        max_iterations = 500
        epsilon = 0.001
        Helper.run_test(max_iterations, epsilon, description, 1, None, None, 0, None, 1, project_path)
        Helper.delete_file(OutputType.LINK, description, xml_file_name, project_path)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name, project_path))
        Helper.delete_file(OutputType.PATH, description, xml_file_name, project_path)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name, project_path))
        Helper.delete_file(OutputType.OD, description, xml_file_name, project_path)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name, project_path))
        gc.collect()
        
    def test_basic_shortest_path_algorithm_a_to_d(self):
        """Unit test 3 using basic network (corresponds to testBasicShortestPathAlgorithmAtoD() in Java)
        """
        print("Running test_basic_shortes_path_algorithm_a_to_d")
        project_path = self.test_data_path + "basic\\xml\\test3";
        description = "testBasic3";
        csv_file_name = "Time Period 1_2.csv";
        od_csv_file_name = "Time Period 1_1.csv";
        xml_file_name = "Time Period 1.xml";
        max_iterations = 500
        epsilon = 0.001
        Helper.run_test(max_iterations, epsilon, description, 1, None, None, 0, None, 1, project_path)
        Helper.delete_file(OutputType.LINK, description, xml_file_name, project_path)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name, project_path))
        Helper.delete_file(OutputType.PATH, description, xml_file_name, project_path)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name, project_path))
        Helper.delete_file(OutputType.OD, description, xml_file_name, project_path)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name, project_path))
        gc.collect()
    
    def test_explanatory(self):
        """Explanatory unit test, which uses the default project path rather than specifying its own (corresponds to testExplanatory() in Java)
        """
        print("Running test_explanatory")
        description = "explanatory";
        csv_file_name = "Time Period 1_2.csv";
        od_csv_file_name = "Time Period 1_1.csv";
        xml_file_name = "Time Period 1.xml";
        max_iterations = 500
        epsilon = 0.001
        Helper.run_test(max_iterations, epsilon, description, 1, None, None, 0, None, 1)
        Helper.delete_file(OutputType.LINK, description, xml_file_name)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name))
        Helper.delete_file(OutputType.PATH, description, xml_file_name)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name))
        Helper.delete_file(OutputType.OD, description, xml_file_name)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name))
        gc.collect()
    
    def test_basic_three_time_periods(self):
        """Unit test 1 using basic network three time periods (corresponds to testBasicThreeTimePeriods() in Java)
        """
        print("Running test_basic_three_time_periods")
        project_path = self.test_data_path + "basic\\xml\\test13"
        description = "testBasic13"
        csv_file_name1 = "Time Period 1_2.csv"
        csv_file_name2 = "Time Period 2_2.csv"
        csv_file_name3 = "Time Period 3_2.csv"
        od_csv_file_name1 = "Time Period 1_1.csv"
        od_csv_file_name2 = "Time Period 2_1.csv"
        od_csv_file_name3 = "Time Period 3_1.csv"
        xml_file_name1 = "Time Period 1.xml"
        xml_file_name2 = "Time Period 2.xml"
        xml_file_name3 = "Time Period 3.xml"
        max_iterations = 500
        epsilon = 0.001
        Helper.run_test(max_iterations, epsilon, description, 1, None, None, 0, None, 1, project_path)
        Helper.delete_file(OutputType.LINK, description, xml_file_name1, project_path)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name1, project_path))
        Helper.delete_file(OutputType.LINK, description, xml_file_name2, project_path)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name2, project_path))
        Helper.delete_file(OutputType.LINK, description, xml_file_name3, project_path)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name3, project_path))
        Helper.delete_file(OutputType.PATH, description, xml_file_name1, project_path)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name1, project_path))
        Helper.delete_file(OutputType.PATH, description, xml_file_name2, project_path)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name2, project_path))
        Helper.delete_file(OutputType.PATH, description, xml_file_name3, project_path)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name3, project_path))
        Helper.delete_file(OutputType.OD, description, xml_file_name1, project_path)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name1, project_path))
        Helper.delete_file(OutputType.OD, description, xml_file_name2, project_path)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name2, project_path))
        Helper.delete_file(OutputType.OD, description, xml_file_name3, project_path)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name3, project_path))
        gc.collect()
        
    def test_route_choice_compare_with_OmniTRANS4_using_two_time_periods(self):
        """Unit test using route choice network 4 and two time periods (corresponds to testRouteChoiceCompareWithOmniTRANS4UsingTwoTimePeriods() in Java)
        """
        print("Running test_route_choice_compare_with_OmniTRANS4_using_two_time_periods")
        project_path = self.test_data_path + "route_choice\\xml\\test42"
        description = "testRouteChoice42"
        csv_file_name1 = "Time Period 1_500.csv"
        od_csv_file_name1 = "Time Period 1_499.csv"
        csv_file_name2 = "Time Period 2_500.csv"
        od_csv_file_name2 = "Time Period 2_499.csv"
        xml_file_name1 = "Time Period 1.xml"
        xml_file_name2 = "Time Period 2.xml"
        max_iterations = 500
        epsilon = 0.0
        Helper.run_test(max_iterations, epsilon, description, 1, None, None, 0, None, 1, project_path)
        Helper.delete_file(OutputType.LINK, description, xml_file_name1, project_path)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name1, project_path))
        Helper.delete_file(OutputType.LINK, description, xml_file_name2, project_path)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name2, project_path))
        Helper.delete_file(OutputType.PATH, description, xml_file_name1, project_path)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name1, project_path))
        Helper.delete_file(OutputType.PATH, description, xml_file_name2, project_path)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name2, project_path))
        Helper.delete_file(OutputType.OD, description, xml_file_name1, project_path)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name1, project_path))
        Helper.delete_file(OutputType.OD, description, xml_file_name2, project_path)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name2, project_path))
        gc.collect()
        
if __name__ == '__main__':
    unittest.main()
    
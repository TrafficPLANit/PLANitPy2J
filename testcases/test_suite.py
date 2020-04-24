import os, sys
this_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(this_path + "\\..\\src\\")

import gc
import unittest
import math
from test_utils import Helper
from planit import OutputType
from planit import OutputProperty
from planit import ModeWrapper
from planit import TimePeriodWrapper
from planit import MemoryOutputIteratorWrapper
from planit import GatewayState

class TestSuite(unittest.TestCase):
      
    @classmethod
    def setUpClass(cls):
        #cls.test_data_path = this_path  + "\\..\\..\\testcases\\"
        cls.test_data_path = this_path+ "\\"
    
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
        
    def test_explanatory_with_memory_output(self):
        """Explanatory unit test, which save results to memory only and not to file, to test contents of memory output formatter are correct
        """
        print("Running test_explanatory with results only stored in memory")
        description = "explanatory";
        max_iterations = 2
        epsilon = 0.001
        plan_it = Helper.run_test(max_iterations, epsilon, description, 1, None, None, 0, None, 1, None, True)
        memory_output_formatter = plan_it.memory
        mode_counterpart = plan_it.project.get_mode_by_external_id(1)
        mode = ModeWrapper(mode_counterpart)
        time_period_counterpart =  plan_it.project.get_time_period_by_external_id(0)
        time_period = TimePeriodWrapper(time_period_counterpart)
        output_type_link_instance = GatewayState.python_2_java_gateway.entry_point.createEnum(OutputType.LINK.java_class_name(), OutputType.LINK.value)
        memory_output_iterator_counterpart = memory_output_formatter.get_iterator(mode.java, time_period.java, max_iterations, output_type_link_instance)
        memory_output_iterator = MemoryOutputIteratorWrapper(memory_output_iterator_counterpart)
        while memory_output_iterator.has_next():
            keys = memory_output_iterator.get_keys()
            values = memory_output_iterator.get_values()
            output_property_flow_instance = GatewayState.python_2_java_gateway.entry_point.createEnum(OutputProperty.FLOW.java_class_name(), OutputProperty.FLOW.value)
            output_property_cost_instance = GatewayState.python_2_java_gateway.entry_point.createEnum(OutputProperty.LINK_COST.java_class_name(), OutputProperty.LINK_COST.value) 
            output_property_length_instance = GatewayState.python_2_java_gateway.entry_point.createEnum(OutputProperty.LENGTH.java_class_name(), OutputProperty.LENGTH.value) 
            output_property_speed_instance = GatewayState.python_2_java_gateway.entry_point.createEnum(OutputProperty.CALCULATED_SPEED.java_class_name(), OutputProperty.CALCULATED_SPEED.value) 
            output_property_capacity_instance = GatewayState.python_2_java_gateway.entry_point.createEnum(OutputProperty.CAPACITY_PER_LANE.java_class_name(), OutputProperty.CAPACITY_PER_LANE.value) 
            output_property_number_of_lanes_instance = GatewayState.python_2_java_gateway.entry_point.createEnum(OutputProperty.NUMBER_OF_LANES.java_class_name(), OutputProperty.NUMBER_OF_LANES.value) 
     
            flow_position = memory_output_formatter.get_position_of_output_value_property(mode.java, time_period.java, max_iterations, output_type_link_instance, output_property_flow_instance)
            cost_position = memory_output_formatter.get_position_of_output_value_property(mode.java, time_period.java, max_iterations, output_type_link_instance, output_property_cost_instance)
            length_position = memory_output_formatter.get_position_of_output_value_property(mode.java, time_period.java, max_iterations, output_type_link_instance, output_property_length_instance)
            speed_position = memory_output_formatter.get_position_of_output_value_property(mode.java, time_period.java, max_iterations, output_type_link_instance, output_property_speed_instance)
            capacity_position = memory_output_formatter.get_position_of_output_value_property(mode.java, time_period.java, max_iterations, output_type_link_instance, output_property_capacity_instance)
            number_of_lanes_position = memory_output_formatter.get_position_of_output_value_property(mode.java, time_period.java, max_iterations, output_type_link_instance, output_property_number_of_lanes_instance)
            self.assertEquals(values[flow_position], 1)
            self.assertTrue(math.isclose(values[cost_position], 10, rel_tol=0.001))
            self.assertEquals(values[length_position], 10)
            self.assertEquals(values[capacity_position], 2000)
            self.assertEquals(values[number_of_lanes_position], 1)
       
        gc.collect()
 
    def test_explanatory(self):
        """Explanatory unit test, which uses the default project path rather than specifying its own (corresponds to testExplanatory() in Java)
        """
        print("Running test_explanatory with default project path")
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
    
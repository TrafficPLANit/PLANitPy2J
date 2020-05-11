import os, sys
this_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(this_path + "\\..\\src\\")

import gc
import unittest
import math
from test_utils import PlanItHelper
from planit import OutputType
from planit import OutputProperty
from planit import ModeWrapper
from planit import TimePeriodWrapper
from planit import MemoryOutputIteratorWrapper
from planit import GatewayState

class TestSuite(unittest.TestCase):
      
    @classmethod
    def setUpClass(cls):
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
        PlanItHelper.run_test(max_iterations, epsilon, description, 1, initial_costs_file_location, None, 0, None, 1, project_path)       
        PlanItHelper.delete_file(OutputType.LINK, description, xml_file_name, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name, project_path))        
        PlanItHelper.delete_file(OutputType.PATH, description, xml_file_name, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name, project_path))        
        PlanItHelper.delete_file(OutputType.OD, description, xml_file_name, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name, project_path))
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
        PlanItHelper.run_test(max_iterations, epsilon, description, 1, None, None, 0, initial_link_segment_locations_per_time_period, 2, project_path)
        PlanItHelper.delete_file(OutputType.LINK, description, xml_file_name1, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name1, project_path))
        PlanItHelper.delete_file(OutputType.LINK, description, xml_file_name2, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name2, project_path))
        PlanItHelper.delete_file(OutputType.LINK, description, xml_file_name3, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name3, project_path))
        PlanItHelper.delete_file(OutputType.PATH, description, xml_file_name1, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name1, project_path))
        PlanItHelper.delete_file(OutputType.PATH, description, xml_file_name2, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name2, project_path))
        PlanItHelper.delete_file(OutputType.PATH, description, xml_file_name3, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name3, project_path))
        PlanItHelper.delete_file(OutputType.OD, description, xml_file_name1, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name1, project_path))
        PlanItHelper.delete_file(OutputType.OD, description, xml_file_name2, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name2, project_path))
        PlanItHelper.delete_file(OutputType.OD, description, xml_file_name3, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name3, project_path))
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
        PlanItHelper.run_test(max_iterations, epsilon, description, 1, None, None, 0, None, 1, project_path)
        PlanItHelper.delete_file(OutputType.LINK, description, xml_file_name, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name, project_path))
        PlanItHelper.delete_file(OutputType.PATH, description, xml_file_name, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name, project_path))
        PlanItHelper.delete_file(OutputType.OD, description, xml_file_name, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name, project_path))
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
        PlanItHelper.run_test(max_iterations, epsilon, description, 1, None, None, 0, None, 1, project_path)
        PlanItHelper.delete_file(OutputType.LINK, description, xml_file_name, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name, project_path))
        PlanItHelper.delete_file(OutputType.PATH, description, xml_file_name, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name, project_path))
        PlanItHelper.delete_file(OutputType.OD, description, xml_file_name, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name, project_path))
        gc.collect()
        
    def test_explanatory_with_memory_output(self):
        """Explanatory unit test, which saves results to memory only and not to file, to test contents of memory output formatter are correct
        """
        print("Running test_explanatory with results only stored in memory")
        description = "explanatory";
        max_iterations = 2
        epsilon = 0.001
        plan_it = PlanItHelper.run_test(max_iterations, epsilon, description, 1, None, None, 0, None, 1, None, True)

        mode_external_id = 1
        time_period_external_id = 0
        
        flow_position = plan_it.memory.get_position_of_output_value_property(mode_external_id, time_period_external_id, max_iterations, OutputType.LINK, OutputProperty.FLOW)
        cost_position = plan_it.memory.get_position_of_output_value_property(mode_external_id, time_period_external_id, max_iterations, OutputType.LINK, OutputProperty.LINK_COST)
        length_position = plan_it.memory.get_position_of_output_value_property(mode_external_id, time_period_external_id, max_iterations, OutputType.LINK, OutputProperty.LENGTH)
        speed_position = plan_it.memory.get_position_of_output_value_property(mode_external_id, time_period_external_id, max_iterations, OutputType.LINK, OutputProperty.CALCULATED_SPEED)
        capacity_position = plan_it.memory.get_position_of_output_value_property(mode_external_id, time_period_external_id, max_iterations, OutputType.LINK, OutputProperty.CAPACITY_PER_LANE)
        number_of_lanes_position = plan_it.memory.get_position_of_output_value_property(mode_external_id, time_period_external_id, max_iterations, OutputType.LINK, OutputProperty.NUMBER_OF_LANES)
        
        memory_output_iterator_link = plan_it.memory.iterator(mode_external_id, time_period_external_id, max_iterations, OutputType.LINK)
        while memory_output_iterator_link.has_next():
            keys = memory_output_iterator_link.get_keys()
            values = memory_output_iterator_link.get_values()
            self.assertEquals(values[flow_position], 1)
            self.assertTrue(math.isclose(values[cost_position], 10, rel_tol=0.001))
            self.assertEquals(values[length_position], 10)
            self.assertEquals(values[capacity_position], 2000)
            self.assertEquals(values[number_of_lanes_position], 1)
            
        path_position = plan_it.memory.get_position_of_output_value_property(mode_external_id, time_period_external_id, max_iterations, OutputType.PATH, OutputProperty.PATH_STRING)
        key1_position = plan_it.memory.get_position_of_output_key_property(mode_external_id, time_period_external_id, max_iterations, OutputType.PATH, OutputProperty.ORIGIN_ZONE_EXTERNAL_ID)
        key2_position = plan_it.memory.get_position_of_output_key_property(mode_external_id, time_period_external_id, max_iterations, OutputType.PATH, OutputProperty.DESTINATION_ZONE_EXTERNAL_ID)
        memory_output_iterator_path = plan_it.memory.iterator(mode_external_id, time_period_external_id, max_iterations, OutputType.PATH)
        while memory_output_iterator_path.has_next():
            keys = memory_output_iterator_path.get_keys()
            self.assertTrue(keys[key1_position] in [1,2])
            self.assertTrue(keys[key2_position] in [1,2])
            values = memory_output_iterator_path.get_values()
            value = values[path_position]
            if ((keys[key1_position] == 1) and (keys[key2_position] == 2)):
                self.assertEquals(value,"[1,2]")
            else:
                self.assertEquals(value, "")
                
        od_position = plan_it.memory.get_position_of_output_value_property(mode_external_id, time_period_external_id, max_iterations-1, OutputType.OD, OutputProperty.OD_COST)
        key1_position = plan_it.memory.get_position_of_output_key_property(mode_external_id, time_period_external_id, max_iterations-1, OutputType.OD, OutputProperty.ORIGIN_ZONE_EXTERNAL_ID)
        key2_position = plan_it.memory.get_position_of_output_key_property(mode_external_id, time_period_external_id, max_iterations-1, OutputType.OD, OutputProperty.DESTINATION_ZONE_EXTERNAL_ID)
        memory_output_iterator_od = plan_it.memory.iterator(mode_external_id, time_period_external_id, max_iterations, OutputType.PATH)
        while memory_output_iterator_od.has_next():
            keys = memory_output_iterator_path.get_keys()
            self.assertTrue(keys[key1_position] in [1,2])
            self.assertTrue(keys[key2_position] in [1,2])
            values = memory_output_iterator_path.get_values()
            value = values[path_position]
            if ((keys[key1_position] == 1) and (keys[key2_position] == 2)):
                self.assertEquals(value,10)
            else:
                self.assertEquals(value, "")
       
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
        PlanItHelper.run_test(max_iterations, epsilon, description, 1, None, None, 0, None, 1)
        PlanItHelper.delete_file(OutputType.LINK, description, xml_file_name)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name))
        PlanItHelper.delete_file(OutputType.PATH, description, xml_file_name)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name))
        PlanItHelper.delete_file(OutputType.OD, description, xml_file_name)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name))
        gc.collect()
    
    def test_explanatory_without_activating_outputs(self):
        """Explanatory unit test, which does not activate the output type configurations directly, but relies on the code to do this automatically (corresponds to testExplanatory() in Java)
            Includes test that OD csv output file has not been created, since this OutputType.OD was deactivated
        """
        print("Running test_explanatory with default project path")
        description = "explanatory";
        csv_file_name = "Time Period 1_2.csv";
        od_csv_file_name = "Time Period 1_1.csv";
        xml_file_name = "Time Period 1.xml";
        max_iterations = 500
        epsilon = 0.001
        plan_it = PlanItHelper.run_test_without_activating_outputs(max_iterations, epsilon, description, 1, None, None, 0, None, 1)
        output_type = OutputType.OD
        output_type_instance = GatewayState.python_2_java_gateway.entry_point.createEnum(output_type.java_class_name(), output_type.value)
        self.assertTrue(plan_it.assignment.is_output_type_active(output_type_instance))
        plan_it.assignment.deactivate_output(OutputType.OD)
        self.assertFalse(plan_it.assignment.is_output_type_active(output_type_instance))
        PlanItHelper.delete_file(OutputType.LINK, description, xml_file_name)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name))
        PlanItHelper.delete_file(OutputType.PATH, description, xml_file_name)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name))
        project_path = os.getcwd()
        od_file_name = PlanItHelper.create_full_file_name(OutputType.OD, project_path, description,  od_csv_file_name)
        self.assertFalse(os.path.exists(od_file_name))
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
        PlanItHelper.run_test(max_iterations, epsilon, description, 1, None, None, 0, None, 1, project_path)
        PlanItHelper.delete_file(OutputType.LINK, description, xml_file_name1, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name1, project_path))
        PlanItHelper.delete_file(OutputType.LINK, description, xml_file_name2, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name2, project_path))
        PlanItHelper.delete_file(OutputType.LINK, description, xml_file_name3, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name3, project_path))
        PlanItHelper.delete_file(OutputType.PATH, description, xml_file_name1, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name1, project_path))
        PlanItHelper.delete_file(OutputType.PATH, description, xml_file_name2, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name2, project_path))
        PlanItHelper.delete_file(OutputType.PATH, description, xml_file_name3, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name3, project_path))
        PlanItHelper.delete_file(OutputType.OD, description, xml_file_name1, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name1, project_path))
        PlanItHelper.delete_file(OutputType.OD, description, xml_file_name2, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name2, project_path))
        PlanItHelper.delete_file(OutputType.OD, description, xml_file_name3, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name3, project_path))
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
        PlanItHelper.run_test(max_iterations, epsilon, description, 1, None, None, 0, None, 1, project_path)
        PlanItHelper.delete_file(OutputType.LINK, description, xml_file_name1, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name1, project_path))
        PlanItHelper.delete_file(OutputType.LINK, description, xml_file_name2, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name2, project_path))
        PlanItHelper.delete_file(OutputType.PATH, description, xml_file_name1, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name1, project_path))
        PlanItHelper.delete_file(OutputType.PATH, description, xml_file_name2, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name2, project_path))
        PlanItHelper.delete_file(OutputType.OD, description, xml_file_name1, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name1, project_path))
        PlanItHelper.delete_file(OutputType.OD, description, xml_file_name2, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name2, project_path))
        gc.collect()
        
if __name__ == '__main__':
    unittest.main()
    
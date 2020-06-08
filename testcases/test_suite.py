import os, sys   
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),'..','src'))

import gc
import unittest
import math
from test_utils import PlanItHelper
from planit import OutputType
from planit import OutputProperty
from planit import GatewayState
from planit import PLANit

class TestSuite(unittest.TestCase):

    def test_route_choice_2_initial_costs_one_iteration_three_time_periods(self):
        #corresponds to testRouteChoice2InitialCostsOneIterationThreeTimePeriods() in Java)
        
        print("Running test_route_choice_2_initial_costs_one_iteration_three_time_periods")
        project_path = os.path.join('route_choice', 'xml', 'test2initialCostsOneIterationThreeTimePeriods')
        plan_it = PLANit(project_path)
        description = "test2initialCostsOneIterationThreeTimePeriods"
        csv_file_name1 = "Time_Period_1_1.csv"
        od_csv_file_name1 = "Time_Period_1_0.csv"
        csv_file_name2 = "Time_Period_2_1.csv"
        od_csv_file_name2 = "Time_Period_2_0.csv"
        csv_file_name3 = "Time_Period_3_1.csv"
        od_csv_file_name3 = "Time_Period_3_0.csv"
        xml_file_name1 = "Time_Period_1.xml"
        xml_file_name2 = "Time_Period_2.xml"
        xml_file_name3 = "Time_Period_3.xml"
        max_iterations = 1
        plan_it.initial_cost.set(os.path.join("route_choice", "xml\\test2initialCostsOneIterationThreeTimePeriods", "initial_link_segment_costs_time_period_1.csv"), 0)
        plan_it.initial_cost.set(os.path.join("route_choice", "xml", "test2initialCostsOneIterationThreeTimePeriods", "initial_link_segment_costs_time_period_2.csv"), 1)
        plan_it.initial_cost.set(os.path.join("route_choice", "xml", "test2initialCostsOneIterationThreeTimePeriods", "initial_link_segment_costs_time_period_3.csv"), 2)
        epsilon = 0.001
        PlanItHelper.run_test(plan_it, max_iterations, epsilon, description, 1, project_path)
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
              
    def test_mode_test(self):
        project_path = os.path.join('mode_test', 'xml', 'simple')
        plan_it = PLANit(project_path)
        description = "mode_test"
        csv_file_name = "Time_Period_1_2.csv"
        od_csv_file_name = "Time_Period_1_1.csv"
        xml_file_name = "Time_Period_1.xml"
        max_iterations = 2
        epsilon = 0.0000000001
        PlanItHelper.run_mode_test(plan_it, max_iterations, epsilon, description, 1, project_path)
        PlanItHelper.delete_file(OutputType.LINK, description, xml_file_name, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name, project_path))        
        PlanItHelper.delete_file(OutputType.PATH, description, xml_file_name, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name, project_path))        
        PlanItHelper.delete_file(OutputType.OD, description, xml_file_name, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name, project_path))
        gc.collect()
        
    def test_route_choice_5(self):
        project_path = os.path.join('route_choice', 'xml', 'test5')
        plan_it = PLANit(project_path)
        description = "testRouteChoice5"
        csv_file_name = "Time_Period_1_500.csv"
        od_csv_file_name = "Time_Period_1_499.csv"
        xml_file_name = "Time_Period_1.xml"
        plan_it.initial_cost.set(os.path.join("route_choice", "xml", "test2initialCosts500iterations", "initial_link_segment_costs.csv"))
        max_iterations = 500
        epsilon = 0.0000000001
        
        PlanItHelper.run_test5(plan_it, max_iterations, epsilon, description, 1, project_path)
        PlanItHelper.delete_file(OutputType.LINK, description, xml_file_name, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name, project_path))        
        PlanItHelper.delete_file(OutputType.PATH, description, xml_file_name, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name, project_path))        
        PlanItHelper.delete_file(OutputType.OD, description, xml_file_name, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name, project_path))
        gc.collect()
    
    def test_route_choice_2_initial_costs_500_iterations(self):
        # Unit test for route 2 with initial costs and 500 iterations (corresponds to testRouteChoice2InitialCosts500Iterations() in Java)

        project_path = os.path.join('route_choice', 'xml', 'test2initialCosts500iterations')
        plan_it = PLANit(project_path)
        description = "testRouteChoice2initialCosts"
        csv_file_name = "Time_Period_1_500.csv"
        od_csv_file_name = "Time_Period_1_499.csv"
        xml_file_name = "Time_Period_1.xml"
        initial_cost_path = os.path.join('route_choice', 'xml', 'test2initialCosts500iterations', 'initial_link_segment_costs.csv')
        max_iterations = 500
        epsilon = 0.0000000001
        PlanItHelper.run_test(plan_it, max_iterations, epsilon, description, 1, project_path)
        PlanItHelper.delete_file(OutputType.LINK, description, xml_file_name, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name, project_path))        
        PlanItHelper.delete_file(OutputType.PATH, description, xml_file_name, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name, project_path))        
        PlanItHelper.delete_file(OutputType.OD, description, xml_file_name, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name, project_path))
        gc.collect()

    def test_basic_shortest_path_algorithm_a_to_c(self):
        # corresponds to testBasicShortestPathAlgorithmAtoC() in Java)
        
        print("Running test_basic_shortest_path_algorithm_a_to_c")
        project_path = os.path.join('basic', 'xml', 'test2')
        plan_it = PLANit(project_path)
        description = "testBasic2";
        csv_file_name = "Time_Period_1_2.csv";
        od_csv_file_name = "Time_Period_1_1.csv";
        xml_file_name = "Time_Period_1.xml";
        max_iterations = 500
        epsilon = 0.001
        PlanItHelper.run_test(plan_it, max_iterations, epsilon, description, 1, project_path)
        PlanItHelper.delete_file(OutputType.LINK, description, xml_file_name, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name, project_path))
        PlanItHelper.delete_file(OutputType.PATH, description, xml_file_name, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name, project_path))
        PlanItHelper.delete_file(OutputType.OD, description, xml_file_name, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name, project_path))
        gc.collect()
        
    def test_basic_shortest_path_algorithm_a_to_d(self):
        # corresponds to testBasicShortestPathAlgorithmAtoD() in Java
        
        print("Running test_basic_shortes_path_algorithm_a_to_d")
        project_path = os.path.join('basic', 'xml', 'test3')
        plan_it = PLANit(project_path)
        description = "testBasic3";
        csv_file_name = "Time_Period_1_2.csv";
        od_csv_file_name = "Time_Period_1_1.csv";
        xml_file_name = "Time_Period_1.xml";
        max_iterations = 500
        epsilon = 0.001
        PlanItHelper.run_test(plan_it, max_iterations, epsilon, description, 1, project_path)
        PlanItHelper.delete_file(OutputType.LINK, description, xml_file_name, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name, project_path))
        PlanItHelper.delete_file(OutputType.PATH, description, xml_file_name, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name, project_path))
        PlanItHelper.delete_file(OutputType.OD, description, xml_file_name, project_path)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name, project_path))
        gc.collect()
        
    def test_explanatory_with_memory_output(self):
        # Explanatory unit test, which saves results to memory only and not to file, to test contents of memory output formatter are correct
        
        print("Running test_explanatory with results only stored in memory")
        description = "explanatory";
        max_iterations = 2
        epsilon = 0.001
        plan_it = PLANit()
        plan_it = PlanItHelper.run_test(plan_it, max_iterations, epsilon, description, 1, deactivate_file_output=True)

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
            memory_output_iterator_link.next()
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
            memory_output_iterator_path.next()
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
            memory_output_iterator_od.next()
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
        # corresponds to testExplanatory() in Java
        
        print("Running test_explanatory with default project path")
        description = "explanatory";
        csv_file_name = "Time_Period_1_2.csv";
        od_csv_file_name = "Time_Period_1_1.csv";
        xml_file_name = "Time_Period_1.xml";
        max_iterations = 500
        epsilon = 0.001
        plan_it = PLANit()
        PlanItHelper.run_test(plan_it, max_iterations, epsilon, description, 1)
        PlanItHelper.delete_file(OutputType.LINK, description, xml_file_name)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name))
        PlanItHelper.delete_file(OutputType.PATH, description, xml_file_name)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name))
        PlanItHelper.delete_file(OutputType.OD, description, xml_file_name)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name))
        gc.collect()
    
    def test_explanatory_without_activating_outputs(self):
        #Explanatory unit test, which does not activate the output type configurations directly, but relies on the code to do this automatically (corresponds to testExplanatory() in Java)
        #    Includes test that OD csv output file has not been created, since this OutputType.OD was deactivated
        
        print("Running test_explanatory with default project path")
        description = "explanatory";
        csv_file_name = "Time_Period_1_2.csv";
        od_csv_file_name = "Time_Period_1_1.csv";
        xml_file_name = "Time_Period_1.xml";
        max_iterations = 500
        epsilon = 0.001
        plan_it = PLANit()
        plan_it = PlanItHelper.run_test_without_activating_outputs(plan_it, max_iterations, epsilon, description, 1)
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
        # corresponds to testBasicThreeTimePeriods() in Java)
        
        print("Running test_basic_three_time_periods")
        project_path = os.path.join('basic', 'xml', 'test13')
        plan_it = PLANit(project_path)
        description = "testBasic13"
        csv_file_name1 = "Time_Period_1_2.csv"
        csv_file_name2 = "Time_Period_2_2.csv"
        csv_file_name3 = "Time_Period_3_2.csv"
        od_csv_file_name1 = "Time_Period_1_1.csv"
        od_csv_file_name2 = "Time_Period_2_1.csv"
        od_csv_file_name3 = "Time_Period_3_1.csv"
        xml_file_name1 = "Time_Period_1.xml"
        xml_file_name2 = "Time_Period_2.xml"
        xml_file_name3 = "Time_Period_3.xml"
        max_iterations = 500
        epsilon = 0.001
        PlanItHelper.run_test(plan_it, max_iterations, epsilon, description, 1, project_path)
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
        # corresponds to testRouteChoiceCompareWithOmniTRANS4UsingTwoTimePeriods() in Java
        
        print("Running test_route_choice_compare_with_OmniTRANS4_using_two_time_periods")
        project_path = os.path.join('route_choice', 'xml', 'test42')
        plan_it = PLANit(project_path)
        description = "testRouteChoice42"
        csv_file_name1 = "Time_Period_1_500.csv"
        od_csv_file_name1 = "Time_Period_1_499.csv"
        csv_file_name2 = "Time_Period_2_500.csv"
        od_csv_file_name2 = "Time_Period_2_499.csv"
        xml_file_name1 = "Time_Period_1.xml"
        xml_file_name2 = "Time_Period_2.xml"
        max_iterations = 500
        epsilon = 0.0
        PlanItHelper.run_test(plan_it, max_iterations, epsilon, description, 1, project_path)
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
    
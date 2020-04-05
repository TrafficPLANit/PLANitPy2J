from unittest import TestCase
from planit.test_utils import Helper
from planit.enums import OutputType
from planit.PLANit import PLANit
from planit.gateway import GatewayState

class TestSuite(TestCase):
    
    def test_route_choice_2_initial_costs_one_iteration_three_time_periods(self):
        print("Running test_route_choice_2_initial_costs_one_iteration_three_time_periods")
        plan_it = PLANit()  
        if (GatewayState.gateway_is_running):    
            plan_it.stop_java()
        plan_it.start_java()
        project_path = "C:\\springsource\\PythonPlanItRunner\\testcases\\route_choice\\xml\\test2initialCostsOneIterationThreeTimePeriods"
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
        initial_link_segment_locations_per_time_period[0] = "C:\\springsource\\PythonPlanItRunner\\testcases\\route_choice\\xml\\test2initialCostsOneIterationThreeTimePeriods\\initial_link_segment_costs_time_period_1.csv"
        initial_link_segment_locations_per_time_period[1] = "C:\\springsource\\PythonPlanItRunner\\testcases\\route_choice\\xml\\test2initialCostsOneIterationThreeTimePeriods\\initial_link_segment_costs_time_period_2.csv"
        initial_link_segment_locations_per_time_period[2] = "C:\\springsource\\PythonPlanItRunner\\testcases\\route_choice\\xml\\test2initialCostsOneIterationThreeTimePeriods\\initial_link_segment_costs_time_period_3.csv"
        epsilon = 0.001
        Helper.run_test(plan_it, project_path, max_iterations, epsilon, description, 1, None, None, 0, initial_link_segment_locations_per_time_period, 2)
        Helper.delete_file(OutputType.LINK, project_path, description, xml_file_name1)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.LINK, project_path, description, csv_file_name1))
        Helper.delete_file(OutputType.LINK, project_path, description, xml_file_name2)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.LINK, project_path, description, csv_file_name2))
        Helper.delete_file(OutputType.LINK, project_path, description, xml_file_name3)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.LINK, project_path, description, csv_file_name3))
        Helper.delete_file(OutputType.PATH, project_path, description, xml_file_name1)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.PATH, project_path, description, csv_file_name1))
        Helper.delete_file(OutputType.PATH, project_path, description, xml_file_name2)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.PATH, project_path, description, csv_file_name2))
        Helper.delete_file(OutputType.PATH, project_path, description, xml_file_name3)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.PATH, project_path, description, csv_file_name3))
        Helper.delete_file(OutputType.OD, project_path, description, xml_file_name1)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.OD, project_path, description, od_csv_file_name1))
        Helper.delete_file(OutputType.OD, project_path, description, xml_file_name2)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.OD, project_path, description, od_csv_file_name2))
        Helper.delete_file(OutputType.OD, project_path, description, xml_file_name3)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.OD, project_path, description, od_csv_file_name3))
        plan_it.stop_java()

    def test_basic_shortest_path_algorithm_a_to_c(self):
        print("Running test_basic_shortest_path_algorithm_a_to_c")
        plan_it = PLANit()      
        if (GatewayState.gateway_is_running):    
            plan_it.stop_java()
        plan_it.start_java()
        project_path = "C:\\springsource\\PythonPlanItRunner\\testcases\\basic\\xml\\test2";
        description = "testBasic2";
        csv_file_name = "Time Period 1_2.csv";
        od_csv_file_name = "Time Period 1_1.csv";
        xml_file_name = "Time Period 1.xml";
        max_iterations = 500
        epsilon = 0.001
        Helper.run_test(plan_it, project_path, max_iterations, epsilon, description, 1, None, None, 0, None, 1)
        Helper.delete_file(OutputType.LINK, project_path, description, xml_file_name)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.LINK, project_path, description, csv_file_name))
        Helper.delete_file(OutputType.PATH, project_path, description, xml_file_name)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.PATH, project_path, description, csv_file_name))
        Helper.delete_file(OutputType.OD, project_path, description, xml_file_name)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.OD, project_path, description, od_csv_file_name))
        plan_it.stop_java()
        
    def test_basic_shortest_path_algorithm_a_to_d(self):
        print("Running test_basic_shortes_path_algorithm_a_to_d")
        plan_it = PLANit()      
        if (GatewayState.gateway_is_running):    
            plan_it.stop_java()
        plan_it.start_java()
        project_path = "C:\\springsource\\PythonPlanItRunner\\testcases\\basic\\xml\\test3";
        description = "testBasic3";
        csv_file_name = "Time Period 1_2.csv";
        od_csv_file_name = "Time Period 1_1.csv";
        xml_file_name = "Time Period 1.xml";
        max_iterations = 500
        epsilon = 0.001
        Helper.run_test(plan_it, project_path, max_iterations, epsilon, description, 1, None, None, 0, None, 1)
        Helper.delete_file(OutputType.LINK, project_path, description, xml_file_name)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.LINK, project_path, description, csv_file_name))
        Helper.delete_file(OutputType.PATH, project_path, description, xml_file_name)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.PATH, project_path, description, csv_file_name))
        Helper.delete_file(OutputType.OD, project_path, description, xml_file_name)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.OD, project_path, description, od_csv_file_name))
        plan_it.stop_java()
    
    def test_basic_three_time_periods(self):
        print("Running test_basic_three_time_periods")
        plan_it = PLANit()      
        if (GatewayState.gateway_is_running):    
            plan_it.stop_java()
        plan_it.start_java()
        project_path = "C:\\springsource\\PythonPlanItRunner\\testcases\\basic\\xml\\test13"
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
        Helper.run_test(plan_it, project_path, max_iterations, epsilon, description, 1, None, None, 0, None, 1)
        Helper.delete_file(OutputType.LINK, project_path, description, xml_file_name1)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.LINK, project_path, description, csv_file_name1))
        Helper.delete_file(OutputType.LINK, project_path, description, xml_file_name2)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.LINK, project_path, description, csv_file_name2))
        Helper.delete_file(OutputType.LINK, project_path, description, xml_file_name3)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.LINK, project_path, description, csv_file_name3))
        Helper.delete_file(OutputType.PATH, project_path, description, xml_file_name1)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.PATH, project_path, description, csv_file_name1))
        Helper.delete_file(OutputType.PATH, project_path, description, xml_file_name2)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.PATH, project_path, description, csv_file_name2))
        Helper.delete_file(OutputType.PATH, project_path, description, xml_file_name3)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.PATH, project_path, description, csv_file_name3))
        Helper.delete_file(OutputType.OD, project_path, description, xml_file_name1)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.OD, project_path, description, od_csv_file_name1))
        Helper.delete_file(OutputType.OD, project_path, description, xml_file_name2)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.OD, project_path, description, od_csv_file_name2))
        Helper.delete_file(OutputType.OD, project_path, description, xml_file_name3)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.OD, project_path, description, od_csv_file_name3))
        plan_it.stop_java()
        
    def test_route_choice_compare_with_OmniTRANS4_using_two_time_periods(self):
        print("Running test_route_choice_compare_with_OmniTRANS4_using_two_time_periods")
        plan_it = PLANit()      
        if (GatewayState.gateway_is_running):    
            plan_it.stop_java()
        plan_it.start_java()
        project_path = "C:\\springsource\\PythonPlanItRunner\\testcases\\route_choice\\xml\\test42"
        description = "testRouteChoice42"
        csv_file_name1 = "Time Period 1_500.csv"
        od_csv_file_name1 = "Time Period 1_499.csv"
        csv_file_name2 = "Time Period 2_500.csv"
        od_csv_file_name2 = "Time Period 2_499.csv"
        xml_file_name1 = "Time Period 1.xml"
        xml_file_name2 = "Time Period 2.xml"
        max_iterations = 500
        epsilon = 0.0
        Helper.run_test(plan_it, project_path, max_iterations, epsilon, description, 1, None, None, 0, None, 1)
        Helper.delete_file(OutputType.LINK, project_path, description, xml_file_name1)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.LINK, project_path, description, csv_file_name1))
        Helper.delete_file(OutputType.LINK, project_path, description, xml_file_name2)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.LINK, project_path, description, csv_file_name2))
        Helper.delete_file(OutputType.PATH, project_path, description, xml_file_name1)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.PATH, project_path, description, csv_file_name1))
        Helper.delete_file(OutputType.PATH, project_path, description, xml_file_name2)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.PATH, project_path, description, csv_file_name2))
        Helper.delete_file(OutputType.OD, project_path, description, xml_file_name1)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.OD, project_path, description, od_csv_file_name1))
        Helper.delete_file(OutputType.OD, project_path, description, xml_file_name2)
        self.assertTrue(Helper.compare_csv_files_and_clean_up(OutputType.OD, project_path, description, od_csv_file_name2))
        plan_it.stop_java()
    
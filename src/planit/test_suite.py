import gc
from unittest import TestCase
from planit.test_utils import Helper
from planit.enums import OutputType

class TestSuite(TestCase):
    
    def test_route_choice_2_initial_costs_one_iteration_three_time_periods(self):
        print("Running test_route_choice_2_initial_costs_one_iteration_three_time_periods")
        project_path = "C:\\springsource\\PLANitPy2J\\testcases\\route_choice\\xml\\test2initialCostsOneIterationThreeTimePeriods"
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
        initial_link_segment_locations_per_time_period[0] = "C:\\springsource\\PLANitPy2J\\testcases\\route_choice\\xml\\test2initialCostsOneIterationThreeTimePeriods\\initial_link_segment_costs_time_period_1.csv"
        initial_link_segment_locations_per_time_period[1] = "C:\\springsource\\PLANitPy2J\\testcases\\route_choice\\xml\\test2initialCostsOneIterationThreeTimePeriods\\initial_link_segment_costs_time_period_2.csv"
        initial_link_segment_locations_per_time_period[2] = "C:\\springsource\\PLANitPy2J\\testcases\\route_choice\\xml\\test2initialCostsOneIterationThreeTimePeriods\\initial_link_segment_costs_time_period_3.csv"
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
        print("Running test_basic_shortest_path_algorithm_a_to_c")
        project_path = "C:\\springsource\\PLANitPy2J\\testcases\\basic\\xml\\test2";
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
        print("Running test_basic_shortes_path_algorithm_a_to_d")
        project_path = "C:\\springsource\\PLANitPy2J\\testcases\\basic\\xml\\test3";
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
        print("Running test_basic_three_time_periods")
        project_path = "C:\\springsource\\PLANitPy2J\\testcases\\basic\\xml\\test13"
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
        print("Running test_route_choice_compare_with_OmniTRANS4_using_two_time_periods")
        project_path = "C:\\springsource\\PLANitPy2J\\testcases\\route_choice\\xml\\test42"
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
    
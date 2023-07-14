import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'src'))

import gc
import unittest
import math
from test_utils import PlanItHelper
from planit import *


class TestSuiteAssignment(unittest.TestCase):

    def test_explanatory_report_zero_outputs(self):
        project_path = os.path.join('explanatory', 'reportZeroOutputs')
        plan_it = Planit()
        assignment_project = plan_it.create_project(project_path)

        description = "explanatory"
        csv_file_name = "Time_Period_1_2.csv"
        od_csv_file_name = "Time_Period_1_1.csv"
        xml_file_name = "Time_Period_1.xml"
        max_iterations = 500
        epsilon = 0.0000000001

        PlanItHelper.run_test_with_zero_flow_outputs(assignment_project, max_iterations, epsilon, description, 1,
                                                     project_path)

        PlanItHelper.delete_file(OutputType.LINK, description, xml_file_name, project_path)
        self.assertTrue(
            PlanItHelper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name, project_path))
        PlanItHelper.delete_file(OutputType.PATH, description, xml_file_name, project_path)
        self.assertTrue(
            PlanItHelper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name, project_path))
        PlanItHelper.delete_file(OutputType.OD, description, xml_file_name, project_path)
        self.assertTrue(
            PlanItHelper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name, project_path))
        gc.collect()

    def test_explanatory_with_memory_output(self):
        # Explanatory unit test, which saves results to memory only and not to file, to test contents of memory
        # output formatter are correct

        print("Running test_explanatory with results only stored in memory")
        description = "explanatory"
        max_iterations = 2
        epsilon = 0.001
        plan_it = Planit()
        assignment_project = plan_it.project()

        PlanItHelper.run_test(assignment_project, max_iterations, epsilon, description, 1, deactivate_file_output=True)

        mode_xml_id = "1"
        time_period_xml_id = "0"

        flow_position = assignment_project.memory.get_position_of_output_value_property(OutputType.LINK,
                                                                                        OutputProperty.FLOW)
        cost_position = assignment_project.memory.get_position_of_output_value_property(OutputType.LINK,
                                                                                        OutputProperty.LINK_SEGMENT_COST)
        speed_position = assignment_project.memory.get_position_of_output_value_property(OutputType.LINK,
                                                                                         OutputProperty.CALCULATED_SPEED)

        memory_output_iterator_link = assignment_project.memory.iterator(mode_xml_id, time_period_xml_id,
                                                                         max_iterations, OutputType.LINK)
        while memory_output_iterator_link.has_next():
            memory_output_iterator_link.next()
            keys = memory_output_iterator_link.get_keys()
            values = memory_output_iterator_link.get_values()
            self.assertEqual(values[flow_position], 1)
            self.assertTrue(math.isclose(values[cost_position], 10, rel_tol=0.001))

        path_position = assignment_project.memory.get_position_of_output_value_property(OutputType.PATH,
                                                                                        OutputProperty.PATH_STRING)
        key1_position = assignment_project.memory.get_position_of_output_key_property(OutputType.PATH,
                                                                                      OutputProperty.ORIGIN_ZONE_XML_ID)
        key2_position = assignment_project.memory.get_position_of_output_key_property(OutputType.PATH,
                                                                                      OutputProperty.DESTINATION_ZONE_XML_ID)
        memory_output_iterator_path = assignment_project.memory.iterator(mode_xml_id, time_period_xml_id,
                                                                         max_iterations, OutputType.PATH)
        while memory_output_iterator_path.has_next():
            memory_output_iterator_path.next()
            keys = memory_output_iterator_path.get_keys()
            self.assertTrue(keys[key1_position] in ["1", "2"])
            self.assertTrue(keys[key2_position] in ["1", "2"])
            values = memory_output_iterator_path.get_values()
            value = values[path_position]
            if (keys[key1_position] == "1") and (keys[key2_position] == "2"):
                self.assertEqual(value, "[1,2]")
            else:
                self.assertEqual(value, "")

        od_position = assignment_project.memory.get_position_of_output_value_property(OutputType.OD,
                                                                                      OutputProperty.OD_COST)
        key1_position = assignment_project.memory.get_position_of_output_key_property(OutputType.OD,
                                                                                      OutputProperty.ORIGIN_ZONE_XML_ID)
        key2_position = assignment_project.memory.get_position_of_output_key_property(OutputType.OD,
                                                                                      OutputProperty.DESTINATION_ZONE_XML_ID)
        memory_output_iterator_od = assignment_project.memory.iterator(mode_xml_id, time_period_xml_id,
                                                                       max_iterations - 1, OutputType.OD)
        while memory_output_iterator_od.has_next():
            memory_output_iterator_od.next()
            keys = memory_output_iterator_od.get_keys()
            self.assertTrue(keys[key1_position] in ["1", "2"])
            self.assertTrue(keys[key2_position] in ["1", "2"])
            values = memory_output_iterator_od.get_values()
            value = values[od_position]
            if ((keys[key1_position] == "1") and (keys[key2_position] == "2")):
                self.assertEqual(value, 10)
            else:
                self.assertEqual(value, "")

        gc.collect()

    def test_explanatory(self):
        # corresponds to testExplanatory() in Java

        print("Running test_explanatory with default project path")
        description = "explanatory"
        csv_file_name = "Time_Period_1_2.csv"
        od_csv_file_name = "Time_Period_1_1.csv"
        xml_file_name = "Time_Period_1.xml"
        max_iterations = 500
        epsilon = 0.001
        plan_it = Planit()
        assignment_project = plan_it.project()
        PlanItHelper.run_test(assignment_project, max_iterations, epsilon, description, 1)

        PlanItHelper.delete_file(OutputType.LINK, description, xml_file_name)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name))
        PlanItHelper.delete_file(OutputType.PATH, description, xml_file_name)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name))
        PlanItHelper.delete_file(OutputType.OD, description, xml_file_name)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name))
        gc.collect()

    def test_explanatory_without_activating_outputs(self):
        # Explanatory unit test, which does not activate the output type configurations directly, but relies on the
        # code to do this automatically (corresponds to testExplanatory() in Java) Includes test that OD csv output
        # file has not been created, since this OutputType.OD was deactivated

        print("Running test_explanatory with default project path")
        description = "explanatory"
        csv_file_name = "Time_Period_1_2.csv"
        od_csv_file_name = "Time_Period_1_1.csv"
        xml_file_name = "Time_Period_1.xml"
        max_iterations = 500
        epsilon = 0.001
        plan_it = Planit()
        assignment_project = plan_it.project()
        PlanItHelper.run_test_without_activating_outputs(assignment_project, max_iterations, epsilon, description, 1)

        output_type = OutputType.OD
        output_type_instance = GatewayState.python_2_java_gateway.entry_point.createEnum(output_type.java_class_name(),
                                                                                         output_type.value)
        self.assertTrue(assignment_project.assignment.is_output_type_active(output_type_instance))
        assignment_project.assignment.deactivate_output(OutputType.OD)
        self.assertFalse(assignment_project.assignment.is_output_type_active(output_type_instance))
        PlanItHelper.delete_file(OutputType.LINK, description, xml_file_name)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name))
        PlanItHelper.delete_file(OutputType.PATH, description, xml_file_name)
        self.assertTrue(PlanItHelper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name))
        project_path = os.getcwd()
        od_file_name = PlanItHelper.create_full_file_name(OutputType.OD, project_path, description, od_csv_file_name)
        self.assertFalse(os.path.exists(od_file_name))
        gc.collect()

    def test_2_SIMO_MISO_route_choice_single_mode_with_initial_costs_and_one_iteration_and_three_time_periods(self):
        # corresponds to
        # test_2_SIMO_MISO_route_choice_single_mode_with_initial_costs_and_one_iteration_and_three_time_periods() in
        # Java)

        print(
            "Running test_2_SIMO_MISO_route_choice_single_mode_with_initial_costs_and_one_iteration_and_three_time_periods")
        project_path = os.path.join('route_choice', 'xml',
                                    'SIMOMISOrouteChoiceInitialCostsOneIterationThreeTimePeriods')
        plan_it = Planit()
        assignment_project = plan_it.create_project(project_path)

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
        timePeriod0XmlId = "0"
        timePeriod1XmlId = "1"
        timePeriod2XmlId = "2"
        epsilon = 0.001

        assignment_project.initial_cost.set(
            os.path.join("route_choice", "xml", "SIMOMISOrouteChoiceInitialCostsOneIterationThreeTimePeriods",
                         "initial_link_segment_costs_time_period_1.csv"), timePeriod0XmlId)
        assignment_project.initial_cost.set(
            os.path.join("route_choice", "xml", "SIMOMISOrouteChoiceInitialCostsOneIterationThreeTimePeriods",
                         "initial_link_segment_costs_time_period_2.csv"), timePeriod1XmlId)
        assignment_project.initial_cost.set(
            os.path.join("route_choice", "xml", "SIMOMISOrouteChoiceInitialCostsOneIterationThreeTimePeriods",
                         "initial_link_segment_costs_time_period_3.csv"), timePeriod2XmlId)

        PlanItHelper.run_test(assignment_project, max_iterations, epsilon, description, 1, project_path)

        PlanItHelper.delete_file(OutputType.LINK, description, xml_file_name1, project_path)
        self.assertTrue(
            PlanItHelper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name1, project_path))
        PlanItHelper.delete_file(OutputType.LINK, description, xml_file_name2, project_path)
        self.assertTrue(
            PlanItHelper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name2, project_path))
        PlanItHelper.delete_file(OutputType.LINK, description, xml_file_name3, project_path)
        self.assertTrue(
            PlanItHelper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name3, project_path))
        PlanItHelper.delete_file(OutputType.PATH, description, xml_file_name1, project_path)
        self.assertTrue(
            PlanItHelper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name1, project_path))
        PlanItHelper.delete_file(OutputType.PATH, description, xml_file_name2, project_path)
        self.assertTrue(
            PlanItHelper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name2, project_path))
        PlanItHelper.delete_file(OutputType.PATH, description, xml_file_name3, project_path)
        self.assertTrue(
            PlanItHelper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name3, project_path))
        PlanItHelper.delete_file(OutputType.OD, description, xml_file_name1, project_path)
        self.assertTrue(
            PlanItHelper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name1, project_path))
        PlanItHelper.delete_file(OutputType.OD, description, xml_file_name2, project_path)
        self.assertTrue(
            PlanItHelper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name2, project_path))
        PlanItHelper.delete_file(OutputType.OD, description, xml_file_name3, project_path)
        self.assertTrue(
            PlanItHelper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name3, project_path))
        gc.collect()

    def test_5_SIMO_MISO_route_choice_two_modes(self):
        # corresponds to test_5_SIMO_MISO_route_choice_two_modes() in Java

        # prep
        project_path = os.path.join('route_choice', 'xml', 'SIMOMISOrouteChoiceTwoModes')
        description = "testRouteChoice5"
        csv_file_name = "Time_Period_1_500.csv"
        od_csv_file_name = "Time_Period_1_499.csv"
        xml_file_name = "Time_Period_1.xml"
        max_iterations = 500
        epsilon = 0.0000000001
        output_type_configuration_option = 1

        plan_it = Planit()
        assignment_project = plan_it.create_project(project_path)

        # setup
        assignment_project.set(TrafficAssignment.TRADITIONAL_STATIC)
        assignment_project.assignment.physical_cost.set_default_parameters(0.8, 4.5, "2", "1")

        assignment_project.assignment.output_configuration.set_persist_only_final_Iteration(True)
        assignment_project.assignment.activate_output(OutputType.LINK)
        assignment_project.assignment.link_configuration.remove(OutputProperty.TIME_PERIOD_XML_ID)
        assignment_project.assignment.link_configuration.remove(OutputProperty.TIME_PERIOD_ID)
        assignment_project.assignment.link_configuration.remove(OutputProperty.MAXIMUM_SPEED)

        assignment_project.assignment.activate_output(OutputType.OD)
        assignment_project.assignment.od_configuration.deactivate(OdSkimSubOutputType.NONE)
        assignment_project.assignment.od_configuration.remove(OutputProperty.TIME_PERIOD_XML_ID)
        assignment_project.assignment.od_configuration.remove(OutputProperty.RUN_ID)
        assignment_project.assignment.activate_output(OutputType.PATH)
        assignment_project.assignment.path_configuration.set_path_id_type(PathIdType.NODE_XML_ID)
        assignment_project.assignment.gap_function.stop_criterion.set_max_iterations(max_iterations)
        assignment_project.assignment.gap_function.stop_criterion.set_epsilon(epsilon)

        # test log settings option
        assignment_project.assignment.set_log_settings(False)
        assignment_project.assignment.set_log_settings(True)

        # change desired units to veh/h
        assignment_project.assignment.link_configuration.override_output_property_units(OutputProperty.FLOW,
                                                                                        [UnitType.VEH], [UnitType.HOUR])

        assignment_project.output.set_xml_name_root(description)
        assignment_project.output.set_csv_name_root(description)
        assignment_project.output.set_output_directory(project_path)
        assignment_project.run()

        # compare
        PlanItHelper.delete_file(OutputType.LINK, description, xml_file_name, project_path)
        self.assertTrue(
            PlanItHelper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name, project_path))
        PlanItHelper.delete_file(OutputType.PATH, description, xml_file_name, project_path)
        self.assertTrue(
            PlanItHelper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name, project_path))
        PlanItHelper.delete_file(OutputType.OD, description, xml_file_name, project_path)
        self.assertTrue(
            PlanItHelper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name, project_path))
        gc.collect()

    def test_2_SIMO_MISO_route_choice_single_mode_with_initial_costs_and_500_iterations(self):
        # Unit test for route 2 with initial costs and 500 iterations (corresponds to test_2_SIMO_MISO_route_choice_single_mode_with_initial_costs_and_500_iterations() in Java)

        project_path = os.path.join('route_choice', 'xml', 'SIMOMISOrouteChoiceSingleModeWithInitialCosts500Iterations')
        description = "testRouteChoice2initialCosts"
        csv_file_name = "Time_Period_1_500.csv"
        od_csv_file_name = "Time_Period_1_499.csv"
        xml_file_name = "Time_Period_1.xml"
        max_iterations = 500
        epsilon = 0.0000000001

        plan_it = Planit()
        assignment_project = plan_it.create_project(project_path)
        assignment_project.initial_cost.set(
            os.path.join("route_choice", "xml", "SIMOMISOrouteChoiceSingleModeWithInitialCosts500Iterations",
                         "initial_link_segment_costs.csv"))

        PlanItHelper.run_test(assignment_project, max_iterations, epsilon, description, 1, project_path)

        PlanItHelper.delete_file(OutputType.LINK, description, xml_file_name, project_path)
        self.assertTrue(
            PlanItHelper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name, project_path))
        PlanItHelper.delete_file(OutputType.PATH, description, xml_file_name, project_path)
        self.assertTrue(
            PlanItHelper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name, project_path))
        PlanItHelper.delete_file(OutputType.OD, description, xml_file_name, project_path)
        self.assertTrue(
            PlanItHelper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name, project_path))
        gc.collect()

    def test_4_bi_directional_links_route_choice_single_mode_with_two_time_periods(self):
        # corresponds to test_4_bi_directional_links_route_choice_single_mode_with_two_time_periods() in Java

        print("Running test_route_choice_compare_with_OmniTRANS4_using_two_time_periods")
        project_path = os.path.join('route_choice', 'xml', 'biDirectionalLinksRouteChoiceSingleModeWithTwoTimePeriods')
        description = "testRouteChoice42"
        csv_file_name1 = "Time_Period_1_500.csv"
        od_csv_file_name1 = "Time_Period_1_499.csv"
        csv_file_name2 = "Time_Period_2_500.csv"
        od_csv_file_name2 = "Time_Period_2_499.csv"
        xml_file_name1 = "Time_Period_1.xml"
        xml_file_name2 = "Time_Period_2.xml"
        max_iterations = 500
        epsilon = 0.0

        plan_it = Planit()
        assignment_project = plan_it.create_project(project_path)
        PlanItHelper.run_test(assignment_project, max_iterations, epsilon, description, 1, project_path)

        PlanItHelper.delete_file(OutputType.LINK, description, xml_file_name1, project_path)
        self.assertTrue(
            PlanItHelper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name1, project_path))
        PlanItHelper.delete_file(OutputType.LINK, description, xml_file_name2, project_path)
        self.assertTrue(
            PlanItHelper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name2, project_path))
        PlanItHelper.delete_file(OutputType.PATH, description, xml_file_name1, project_path)
        self.assertTrue(
            PlanItHelper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name1, project_path))
        PlanItHelper.delete_file(OutputType.PATH, description, xml_file_name2, project_path)
        self.assertTrue(
            PlanItHelper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name2, project_path))
        PlanItHelper.delete_file(OutputType.OD, description, xml_file_name1, project_path)
        self.assertTrue(
            PlanItHelper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name1, project_path))
        PlanItHelper.delete_file(OutputType.OD, description, xml_file_name2, project_path)
        self.assertTrue(
            PlanItHelper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name2, project_path))
        gc.collect()

    def test_mode_test(self):
        # corresponds to test_mode_test() in Java

        project_path = os.path.join('mode_test', 'xml', 'simple')
        description = "mode_test"
        csv_file_name = "Time_Period_1_2.csv"
        od_csv_file_name = "Time_Period_1_1.csv"
        xml_file_name = "Time_Period_1.xml"
        max_iterations = 2
        epsilon = 0.0000000001

        plan_it = Planit()
        assignment_project = plan_it.create_project(project_path)

        # setup
        assignment_project.set(TrafficAssignment.TRADITIONAL_STATIC)
        assignment_project.set(GapFunction.LINK_BASED_RELATIVE)
        assignment_project.assignment.output_configuration.set_persist_only_final_Iteration(True)
        assignment_project.assignment.activate_output(OutputType.LINK)
        assignment_project.assignment.link_configuration.remove(OutputProperty.TIME_PERIOD_XML_ID)
        assignment_project.assignment.link_configuration.remove(OutputProperty.TIME_PERIOD_ID)
        assignment_project.assignment.link_configuration.remove(OutputProperty.MAXIMUM_SPEED)

        assignment_project.assignment.activate_output(OutputType.OD)
        assignment_project.assignment.od_configuration.deactivate(OdSkimSubOutputType.NONE)
        assignment_project.assignment.od_configuration.remove(OutputProperty.TIME_PERIOD_XML_ID)
        assignment_project.assignment.od_configuration.remove(OutputProperty.RUN_ID)
        assignment_project.assignment.activate_output(OutputType.PATH)
        assignment_project.assignment.path_configuration.set_path_id_type(PathIdType.NODE_XML_ID)
        assignment_project.assignment.gap_function.stop_criterion.set_max_iterations(max_iterations)
        assignment_project.assignment.gap_function.stop_criterion.set_epsilon(epsilon)

        assignment_project.output.set_xml_name_root(description)
        assignment_project.output.set_csv_name_root(description)
        assignment_project.output.set_output_directory(project_path)

        assignment_project.assignment.physical_cost.set_default_parameters(0.8, 4.5, "1", "1")
        link_segment_xml_id = "3"
        mode_xml_id = "1"
        assignment_project.assignment.physical_cost.set_parameters(1.0, 5.0, mode_xml_id, link_segment_xml_id)

        assignment_project.run()

        # tests
        PlanItHelper.delete_file(OutputType.LINK, description, xml_file_name, project_path)
        self.assertTrue(
            PlanItHelper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name, project_path))
        PlanItHelper.delete_file(OutputType.PATH, description, xml_file_name, project_path)
        self.assertTrue(
            PlanItHelper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name, project_path))
        PlanItHelper.delete_file(OutputType.OD, description, xml_file_name, project_path)
        self.assertTrue(
            PlanItHelper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name, project_path))
        gc.collect()

    def test_basic_shortest_path_algorithm_a_to_c(self):
        # corresponds to test_basic_shortest_path_algorithm_a_to_c() in Java)

        print("Running test_basic_shortest_path_algorithm_a_to_c")
        project_path = os.path.join('basicShortestPathAlgorithm', 'xml', 'AtoC')

        description = "testBasic2"
        csv_file_name = "Time_Period_1_2.csv"
        od_csv_file_name = "Time_Period_1_1.csv"
        xml_file_name = "Time_Period_1.xml"
        max_iterations = 500
        epsilon = 0.001

        plan_it = Planit()
        assignment_project = plan_it.create_project(project_path)
        PlanItHelper.run_test(assignment_project, max_iterations, epsilon, description, 1, project_path)

        PlanItHelper.delete_file(OutputType.LINK, description, xml_file_name, project_path)
        self.assertTrue(
            PlanItHelper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name, project_path))
        PlanItHelper.delete_file(OutputType.PATH, description, xml_file_name, project_path)
        self.assertTrue(
            PlanItHelper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name, project_path))
        PlanItHelper.delete_file(OutputType.OD, description, xml_file_name, project_path)
        self.assertTrue(
            PlanItHelper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name, project_path))
        gc.collect()

    def test_basic_shortest_path_algorithm_a_to_d(self):
        # corresponds to test_basic_shortest_path_algorithm_a_to_d() in Java

        print("Running test_basic_shortes_path_algorithm_a_to_d")
        project_path = os.path.join('basicShortestPathAlgorithm', 'xml', 'AtoD')
        description = "testBasic3"
        csv_file_name = "Time_Period_1_2.csv"
        od_csv_file_name = "Time_Period_1_1.csv"
        xml_file_name = "Time_Period_1.xml"
        max_iterations = 500
        epsilon = 0.001

        plan_it = Planit()
        assignment_project = plan_it.create_project(project_path)
        PlanItHelper.run_test(assignment_project, max_iterations, epsilon, description, 1, project_path)

        PlanItHelper.delete_file(OutputType.LINK, description, xml_file_name, project_path)
        self.assertTrue(
            PlanItHelper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name, project_path))
        PlanItHelper.delete_file(OutputType.PATH, description, xml_file_name, project_path)
        self.assertTrue(
            PlanItHelper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name, project_path))
        PlanItHelper.delete_file(OutputType.OD, description, xml_file_name, project_path)
        self.assertTrue(
            PlanItHelper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name, project_path))
        gc.collect()

    def test_basic_shortest_path_algorithm_three_time_periods(self):
        # corresponds to test_basic_shortest_path_algorithm_three_time_periods() in Java)

        print("Running test_basic_three_time_periods")
        project_path = os.path.join('basicShortestPathAlgorithm', 'xml', 'ThreeTimePeriods')
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

        plan_it = Planit()
        assignment_project = plan_it.create_project(project_path)
        PlanItHelper.run_test(assignment_project, max_iterations, epsilon, description, 1, project_path)

        PlanItHelper.delete_file(OutputType.LINK, description, xml_file_name1, project_path)
        self.assertTrue(
            PlanItHelper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name1, project_path))
        PlanItHelper.delete_file(OutputType.LINK, description, xml_file_name2, project_path)
        self.assertTrue(
            PlanItHelper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name2, project_path))
        PlanItHelper.delete_file(OutputType.LINK, description, xml_file_name3, project_path)
        self.assertTrue(
            PlanItHelper.compare_csv_files_and_clean_up(OutputType.LINK, description, csv_file_name3, project_path))
        PlanItHelper.delete_file(OutputType.PATH, description, xml_file_name1, project_path)
        self.assertTrue(
            PlanItHelper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name1, project_path))
        PlanItHelper.delete_file(OutputType.PATH, description, xml_file_name2, project_path)
        self.assertTrue(
            PlanItHelper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name2, project_path))
        PlanItHelper.delete_file(OutputType.PATH, description, xml_file_name3, project_path)
        self.assertTrue(
            PlanItHelper.compare_csv_files_and_clean_up(OutputType.PATH, description, csv_file_name3, project_path))
        PlanItHelper.delete_file(OutputType.OD, description, xml_file_name1, project_path)
        self.assertTrue(
            PlanItHelper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name1, project_path))
        PlanItHelper.delete_file(OutputType.OD, description, xml_file_name2, project_path)
        self.assertTrue(
            PlanItHelper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name2, project_path))
        PlanItHelper.delete_file(OutputType.OD, description, xml_file_name3, project_path)
        self.assertTrue(
            PlanItHelper.compare_csv_files_and_clean_up(OutputType.OD, description, od_csv_file_name3, project_path))
        gc.collect()


if __name__ == '__main__':
    unittest.main()

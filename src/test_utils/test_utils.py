import os, sys
this_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(this_path + "\\..")
import pandas as pd
from planit import TrafficAssignment
from planit import PhysicalCost
from planit import VirtualCost
from planit import Smoothing
from planit import OutputType
from planit import OutputProperty
from planit import RouteIdType
from planit import OutputFormatter
from planit import ODSkimSubOutputType
from planit import PLANit
from builtins import staticmethod

class Helper:
    
    @staticmethod
    def dictionary_register_initial_costs(plan_it, initial_link_segment_locations_per_time_period):
        """Read in initial cost files for each time period from an input dictionary
        :param plan_it the PLANit object to be updated with the initial costs
        :param initial_link_segment_locations_per_time_period dictionary of locations of initial cost files per time period
        """
        time_periods_external_ids = plan_it.project.get_time_period_external_ids()
        for time_period_external_id in time_periods_external_ids:
            initial_costs_file_location = initial_link_segment_locations_per_time_period[time_period_external_id]
            plan_it.initial_cost.set(initial_costs_file_location, time_period_external_id)
  
    @staticmethod
    def default_register_initial_costs(plan_it, initial_costs_file_location1, initial_costs_file_location2, init_costs_file_pos):
        """Read in one or two initial cost files which are to be used for all time periods
        :param plan_it the PLANit object to be updated with the initial costs
        :param initial_costs_file_location1 location of the first initial cost file (None if initial costs not being used)
        :param  initial_costs_file_location2 location of the second initial cost file (None if only one or zero initial cost files being used)
        :param init_costs_file_pos indicates which initial costs file is to be used (if 0 use the first, otherwise use the second) 
        """      
        if initial_costs_file_location1 != None:
            initial_costs_file_location = None
            if initial_costs_file_location2 != None:
                if init_costs_file_pos == 0:
                    initial_costs_file_location =  initial_costs_file_location1
                else:
                    initial_costs_file_location =  initial_costs_file_location2
            else:
                initial_costs_file_location =  initial_costs_file_location1
            plan_it.initial_cost.set(initial_costs_file_location)
            
    @staticmethod
    def run_test(max_iterations, epsilon, 
                           description, output_type_configuration_option, initial_costs_file_location1, 
                           initial_costs_file_location2, init_costs_file_pos,  
                           initial_link_segment_locations_per_time_period, register_initial_costs_option, 
                           project_path=None, deactivate_file_output=False):
        """Top-level method which runs unit testsX
        :param max_iterations the maximum number of iterations for the current unit test
        :param epsilon the convergence epsilon for the current unit test
        :param description the name to be used to identify input and output files
        :param output_type_configuration_option used to specify which properties to remove from link output type configuration
        :param initial_costs_file_location1 location of first initial costs file, if used (None if not required)
        :param initial_costs_file_location2 location of second initial costs file, if used (None if not required)
        :param init_costs_file_pos position of which initial costs file is being used, if required
        :param initial_link_segment_locations_per_time_period dictionary of initial link cost files per time period, if required
        :param register_initial_costs_option used to specify which method of the selecting initial cost (default or dictionary) is being used
        :param project_path directory of XML input file (if omitted, defaults to None which will make methods use the current directory)
        :param deactivate_file_output if True, deactivate the file output formatter and store results in memory only
        """
        
        if project_path == None:
            plan_it = PLANit()
        else:
            plan_it = PLANit(project_path)
        plan_it.set(TrafficAssignment.TRADITIONAL_STATIC)
        
        plan_it.assignment.set(PhysicalCost.BPR)
        # TODO : Add a unit test which testsX plan_it.assigment.physical_cost.set_default_parameters()
        # testRouteChoiceCompareWithOmniTRANS5() is a  good one for this
        plan_it.assignment.set(VirtualCost.FIXED)
        plan_it.assignment.set(Smoothing.MSA)
        plan_it.assignment.output_configuration.set_persist_only_final_Iteration(True)
        plan_it.assignment.activate_output(OutputType.LINK)
        plan_it.assignment.link_configuration.remove(OutputProperty.TIME_PERIOD_EXTERNAL_ID)
        plan_it.assignment.link_configuration.remove(OutputProperty.TIME_PERIOD_ID)

        if output_type_configuration_option == 1:
            plan_it.assignment.link_configuration.remove(OutputProperty.MAXIMUM_SPEED)
            plan_it.assignment.link_configuration.remove(OutputProperty.TOTAL_COST_TO_END_NODE)
        elif output_type_configuration_option == 2:
            plan_it.assignment.link_configuration.remove(OutputProperty.TOTAL_COST_TO_END_NODE)
            plan_it.assignment.link_configuration.remove(OutputProperty.DOWNSTREAM_NODE_EXTERNAL_ID)
            plan_it.assignment.link_configuration.remove(OutputProperty.UPSTREAM_NODE_EXTERNAL_ID)

        plan_it.assignment.activate_output(OutputType.OD)
        plan_it.assignment.od_configuration.deactivate(ODSkimSubOutputType.NONE)
        plan_it.assignment.od_configuration.remove(OutputProperty.TIME_PERIOD_EXTERNAL_ID)
        plan_it.assignment.od_configuration.remove(OutputProperty.RUN_ID)
        plan_it.assignment.activate_output(OutputType.PATH)
        plan_it.assignment.path_configuration.set_path_id_type(RouteIdType.NODE_EXTERNAL_ID)
        plan_it.assignment.gap_function.stop_criterion.set_max_iterations(max_iterations)
        plan_it.assignment.gap_function.stop_criterion.set_epsilon(epsilon)
        
        plan_it.activate(OutputFormatter.MEMORY)
        if deactivate_file_output:
            plan_it.deactivate(OutputFormatter.PLANIT_IO)
        else:
            plan_it.output.set_xml_name_root(description)                
            plan_it.output.set_csv_name_root(description)     
            if (project_path is not None):  
                plan_it.output.set_output_directory(project_path)

        if register_initial_costs_option == 1:
            Helper.default_register_initial_costs(plan_it, initial_costs_file_location1, initial_costs_file_location2, init_costs_file_pos)
        elif register_initial_costs_option == 2:
            Helper.dictionary_register_initial_costs(plan_it, initial_link_segment_locations_per_time_period)
        
        plan_it.run()
        return plan_it
    
    @staticmethod
    def delete_file(output_type : OutputType, description, file_name, project_path=None):
        """Delete an output file
        :param output_type type of the output file (link, origin-destination or path)
        :param description root name of the output file
        :param project_path directory of the output file
        """
        if project_path == None:
            project_path = os.getcwd()
        full_file_name = Helper.create_full_file_name(output_type, project_path, description, file_name)
        os.remove(full_file_name)
        
    @staticmethod
    def create_full_file_name(output_type : OutputType, project_path, description, file_name):
        """Create the long name of the output file (containing results created by the current test run)
        :param output_type type of the output file (link, origin-destination or path)
        :param description root name of the output file
        :param project_path directory of the output file
        :param file_name name of the file of standard results
        :return the name of the file containing the test results
        """
        type_name = None
        if output_type.value == "LINK":
            type_name = 'Link'
        elif output_type.value == "OD":
            type_name = 'Origin-Destination'
        else:
            type_name = "Path"
            
        full_file_name = project_path 
        full_file_name += "\\" 
        full_file_name +=  type_name
        full_file_name +=  "_" 
        full_file_name +=  "RunId 0_"
        full_file_name +=  description 
        full_file_name +=  "_" 
        full_file_name += file_name
        return full_file_name
    
    @staticmethod
    def create_short_file_name(output_type : OutputType, project_path, file_name):
        """Create the short name of the output file (containing standard results)
        :param output_type type of the output file (link, origin-destination or path)
        :param project_path directory of the output file
        :param file_name name of the file of standard results
        :return the name of the file containing the standard results
        """
        if output_type.value == "LINK":
            type_name = 'Link'
        elif output_type.value == "OD":
            type_name = 'Origin-Destination'
        else:
            type_name = "Path"
            
        short_file_name = project_path 
        short_file_name += "\\" 
        short_file_name +=  type_name
        short_file_name +=  "_" 
        short_file_name += file_name
        return short_file_name
    
    @staticmethod
    def compare_csv_files(csv_file_location1, csv_file_location2):
        """Compare the contents of two CSV files, returning true if they are equal, false otherwise
        :param csv_file_location1 first CSV file to be compared
        :param csv_file_location2 second CSV file to be compared
        :return true if the files have equal contents, false otherwise
        """
        df1 = pd.read_csv(csv_file_location1)
        df2 = pd.read_csv(csv_file_location2)
        return df1.equals(df2)
    
    @staticmethod
    def compare_csv_files_and_clean_up(output_type : OutputType, description, file_name, project_path=None):
        """Compare the file of test results with the file of standard results, and delete the test results file if they are equal
        :param output_type type of the output file (link, origin-destination or path)
        :param description root name of the output file
        :param project_path directory of the output file
        :param file_name name of the file of standard results
        :return true if the files have equal contents and the results file has been deleted, false otherwise
        """
        if project_path == None:
            project_path = os.getcwd()
        full_file_name = Helper.create_full_file_name(output_type, project_path, description, file_name)
        short_file_name = Helper.create_short_file_name(output_type, project_path, file_name)
        comparison_result = Helper.compare_csv_files(short_file_name, full_file_name)
        if (comparison_result):
            os.remove(full_file_name)
        return comparison_result
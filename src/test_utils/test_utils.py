import os
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
    def run_test(max_iterations, epsilon, description, output_type_configuration_option, initial_costs_file_location1, initial_costs_file_location2, init_costs_file_pos,  initial_link_segment_locations_per_time_period, register_initial_costs_option, project_path=None):
        
        if project_path == None:
            plan_it = PLANit()
        else:
            plan_it = PLANit(project_path)
        plan_it.set(TrafficAssignment.TRADITIONAL_STATIC)
        
        plan_it.assignment.set(PhysicalCost.BPR)
        plan_it.assignment.set(VirtualCost.FIXED)
        plan_it.assignment.set(Smoothing.MSA)
        plan_it.assignment.output_configuration.set_persist_only_final_Iteration(True)
        plan_it.assignment.activate_output(OutputType.LINK)

        if output_type_configuration_option == 1:
            plan_it.assignment.link_output_type_configuration.remove(OutputProperty.TIME_PERIOD_EXTERNAL_ID)
            plan_it.assignment.link_output_type_configuration.remove(OutputProperty.TIME_PERIOD_ID)
            plan_it.assignment.link_output_type_configuration.remove(OutputProperty.MAXIMUM_SPEED)
            plan_it.assignment.link_output_type_configuration.remove(OutputProperty.TOTAL_COST_TO_END_NODE)
        elif output_type_configuration_option == 2:
            plan_it.assignment.link_output_type_configuration.remove(OutputProperty.TIME_PERIOD_EXTERNAL_ID)
            plan_it.assignment.link_output_type_configuration.remove(OutputProperty.TIME_PERIOD_ID)
            plan_it.assignment.link_output_type_configuration.remove(OutputProperty.TOTAL_COST_TO_END_NODE)
            plan_it.assignment.link_output_type_configuration.remove(OutputProperty.DOWNSTREAM_NODE_EXTERNAL_ID)
            plan_it.assignment.link_output_type_configuration.remove(OutputProperty.UPSTREAM_NODE_EXTERNAL_ID)

        plan_it.assignment.activate_output(OutputType.OD)
        plan_it.assignment.origin_destination_output_type_configuration.deactivate(ODSkimSubOutputType.NONE)
        plan_it.assignment.origin_destination_output_type_configuration.remove(OutputProperty.TIME_PERIOD_EXTERNAL_ID)
        plan_it.assignment.origin_destination_output_type_configuration.remove(OutputProperty.RUN_ID)
        plan_it.assignment.activate_output(OutputType.PATH)
        plan_it.assignment.path_output_type_configuration.set_path_id_type(RouteIdType.NODE_EXTERNAL_ID)
        plan_it.assignment.gap_function.stop_criterion.set_max_iterations(max_iterations)
        plan_it.assignment.gap_function.stop_criterion.set_epsilon(epsilon)
        
        plan_it.set(OutputFormatter.PLANIT_IO)
        plan_it.set(OutputFormatter.MEMORY)
        plan_it.assignment.set_xml_name_root(description)
                
        plan_it.assignment.set_csv_name_root(description)
        
        plan_it.assignment.set_output_directory(project_path)

        if register_initial_costs_option == 1:
            plan_it.default_register_initial_costs(initial_costs_file_location1, initial_costs_file_location2, init_costs_file_pos)
        elif register_initial_costs_option == 2:
            plan_it.dictionary_register_initial_costs(initial_link_segment_locations_per_time_period)
        
        plan_it.run()
    
    @staticmethod
    def delete_file(output_type : OutputType, description, file_name, project_path=None):
        if project_path == None:
            project_path = os.getcwd()
        full_file_name = Helper.create_full_file_name(output_type, project_path, description, file_name)
        os.remove(full_file_name)
        
    @staticmethod
    def create_full_file_name(output_type : OutputType, project_path, description, file_name):
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
        df1 = pd.read_csv(csv_file_location1)
        df2 = pd.read_csv(csv_file_location2)
        return df1.equals(df2)
    
    @staticmethod
    def compare_csv_files_and_clean_up(output_type : OutputType, description, file_name, project_path=None):
        if project_path == None:
            project_path = os.getcwd()
        full_file_name = Helper.create_full_file_name(output_type, project_path, description, file_name)
        short_file_name = Helper.create_short_file_name(output_type, project_path, file_name)
        comparison_result = Helper.compare_csv_files(short_file_name, full_file_name)
        if (comparison_result):
            os.remove(full_file_name)
        return comparison_result
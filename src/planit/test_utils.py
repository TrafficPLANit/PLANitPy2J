import os
import pandas as pd
from planit.enums import TrafficAssignment
from planit.enums import PhysicalCost
from planit.enums import VirtualCost
from planit.enums import Smoothing
from planit.enums import OutputType
from planit.enums import OutputProperty
from planit.enums import RouteIdType
from planit.enums import OutputFormatter
from planit.enums import ODSkimSubOutputType
from planit.wrappers import TimePeriodWrapper
from planit.wrappers import InitialCostWrapper
from planit.PLANit import PLANit
from builtins import staticmethod

class Helper:
    
    @staticmethod
    def default_register_initial_costs(initial_costs_file_location1, 
                                       initial_costs_file_location2, 
                                       init_costs_file_pos,
                                       plan_it):
        if initial_costs_file_location1 != None:
            initial_cost_counterpart = None
            if initial_costs_file_location2 != None:
                if init_costs_file_pos == 0:
                    initial_cost_counterpart = plan_it.project.create_and_register_initial_link_segment_cost(plan_it.network.java, initial_costs_file_location1)
                else:
                    initial_cost_counterpart = plan_it.project.create_and_register_initial_link_segment_cost(plan_it.network.java, initial_costs_file_location2)
            else:
                initial_cost_counterpart = plan_it.project.create_and_register_initial_link_segment_cost(plan_it.network.java, initial_costs_file_location1)
            initial_cost_wrapper = InitialCostWrapper(initial_cost_counterpart)
            plan_it.assignment.register_initial_link_segment_cost(initial_cost_wrapper.java)

    @staticmethod
    def dictionary_register_initial_costs(initial_link_segment_locations_per_time_period, plan_it):
        for time_period_id in initial_link_segment_locations_per_time_period.keys():
            initial_costs_file_location = initial_link_segment_locations_per_time_period[time_period_id]
            initial_cost_counterpart = plan_it.project.create_and_register_initial_link_segment_cost(plan_it.network.java, initial_costs_file_location)
            initial_cost_wrapper = InitialCostWrapper(initial_cost_counterpart)
            time_period_counterpart = plan_it.demands.get_time_period_by_id(time_period_id)
            time_period_wrapper = TimePeriodWrapper(time_period_counterpart)
            plan_it.assignment.register_initial_link_segment_cost(time_period_wrapper.java, initial_cost_wrapper.java)

    @staticmethod
    def run_test(
                 project_path, 
                 max_iterations, 
                 epsilon, 
                 description, 
                 output_type_configuration_option, 
                 initial_costs_file_location1, 
                 initial_costs_file_location2, 
                 init_costs_file_pos,
                 initial_link_segment_locations_per_time_period,
                 register_initial_costs_option):
        
        plan_it = PLANit(project_path)
        plan_it.set(TrafficAssignment.TRADITIONAL_STATIC)
        
        plan_it.assignment.set(PhysicalCost.BPR)
        plan_it.assignment.set(VirtualCost.FIXED)
        plan_it.assignment.set(Smoothing.MSA)
        plan_it.assignment.output_configuration.set_persist_only_final_Iteration(True)
        plan_it.assignment.activate(OutputType.LINK)

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

        plan_it.assignment.activate(OutputType.OD)
        plan_it.assignment.origin_destination_output_type_configuration.deactivate_od_skim_output_type(ODSkimSubOutputType.NONE)
        plan_it.assignment.origin_destination_output_type_configuration.remove(OutputProperty.TIME_PERIOD_EXTERNAL_ID)
        plan_it.assignment.origin_destination_output_type_configuration.remove(OutputProperty.RUN_ID)
        plan_it.assignment.activate(OutputType.PATH)
        plan_it.assignment.path_output_type_configuration.set_path_id_type(RouteIdType.NODE_EXTERNAL_ID)
        plan_it.assignment.gap_function.stop_criterion.set_max_iterations(max_iterations)
        plan_it.assignment.gap_function.stop_criterion.set_epsilon(epsilon)
        
        plan_it.set(OutputFormatter.PLANIT_IO)
        plan_it.set(OutputFormatter.MEMORY)
        plan_it.assignment.set_xml_name_root(description)
                
        plan_it.assignment.set_csv_name_root(description)
        
        plan_it.assignment.set_output_directory(project_path)

        if register_initial_costs_option == 1:
            Helper.default_register_initial_costs(initial_costs_file_location1, initial_costs_file_location2, init_costs_file_pos, plan_it)
        elif register_initial_costs_option == 2:
            Helper.dictionary_register_initial_costs(initial_link_segment_locations_per_time_period, plan_it)
        
        plan_it.run()
    
    @staticmethod
    def delete_file(output_type : OutputType, project_path, description, file_name):
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
    def compare_csv_files_and_clean_up(output_type : OutputType, project_path, description, file_name):
        full_file_name = Helper.create_full_file_name(output_type, project_path, description, file_name)
        short_file_name = Helper.create_short_file_name(output_type, project_path, file_name)
        comparison_result = Helper.compare_csv_files(short_file_name, full_file_name)
        if (comparison_result):
            os.remove(full_file_name)
        return comparison_result
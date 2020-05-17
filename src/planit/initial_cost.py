"""This class exists to take the logic for setting up the initial costs out of the PLANit class.  It does not wrap any Java object.  
This class is instantiated as a member of the PLANit object.  It allows top level calls to have the signature "plan_it.initial_cost.set(..."
"""
import os, sys
this_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(this_path + "\\..")
from planit import InitialCostWrapper
from planit import TimePeriodWrapper
from planit import TimePeriodsWrapper

class InitialCost:
    
    def __init__(self, network, demands):
        """Initializer for the InitialCosts class
        :param network the network being used
        :param demands the demands object being used
        """
        self._network_instance = network
        self._demands_instance = demands
    
    def __register_costs__(self, project, assignment, initial_costs_file_location, time_period_external_id=None):
        """Set the initial costs 
        :param project the project instance
        :param assignment the assignment builder
        :param initial_costs_file_location the location of the initial cost file, if initial costs being set
        :param time_period_external_id the id of the time period, if initial costs being set for each time period
        """
        initial_cost_counterpart = project.create_and_register_initial_link_segment_cost(self._network_instance.java, initial_costs_file_location)
        initial_cost_wrapper = InitialCostWrapper(initial_cost_counterpart)
        if (time_period_external_id is None):
            assignment.register_initial_link_segment_cost(initial_cost_wrapper.java)
        else:
            time_periods_counterpart = self._demands_instance.get_time_periods()
            time_periods = TimePeriodsWrapper(time_periods_counterpart)
            time_period_counterpart = time_periods.get_time_period_by_external_id(time_period_external_id)
            time_period = TimePeriodWrapper(time_period_counterpart)           
            assignment.register_initial_link_segment_cost(time_period.java, initial_cost_wrapper.java)

    def dictionary_register_initial_costs(self, project, assignment, initial_link_segment_locations_per_time_period):
        """Read in initial cost files for each time period from an input dictionary
        :param project the project object being used
        :param assignment the traffic assignment builder object
        :param plan_it the PLANit object to be updated with the initial costs
        :param initial_link_segment_locations_per_time_period dictionary of locations of initial cost files per time period
        """
        time_period_counterparts = self._demands_instance.get_registered_time_periods()
        for time_period_counterpart in time_period_counterparts:
            time_period = TimePeriodWrapper(time_period_counterpart)
            time_period_external_id = time_period.get_external_id()
            initial_costs_file_location = initial_link_segment_locations_per_time_period[time_period_external_id]
            self.__register_costs__(project, assignment, initial_costs_file_location, time_period_external_id)
            
    def default_register_initial_costs(self, project, assignment, initial_costs_file_location1, initial_costs_file_location2, init_costs_file_pos):
        """Read in one or two initial cost files which are to be used for all time periods
        :param project the project object being used
        :param assignment the traffic assignment builder object
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
            self.__register_costs__(project, assignment, initial_costs_file_location)            

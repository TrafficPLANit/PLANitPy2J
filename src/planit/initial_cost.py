"""This class exists to take the logic for setting up the initial costs out of the PLANit class.  It does not wrap any Java object.  
This class is instantiated as a member of the PLANit object.  It allows top level calls to have the signature "plan_it.initial_cost.set(..."
"""
import os, sys
this_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(this_path + "\\..")
from planit import InitialCostWrapper
from planit import TimePeriodWrapper

class InitialCost:
    
    def __init__(self, network, demands):
        """Initializer for the InitialCosts class
        :param network the network being used
        :param demands the demands object being used
        """
        self._network_instance = network
        self._demands_instance = demands
        self._default_initial_cost_file_location = None
        self._initial_cost_location_dictionary = {}
        
    def set(self, initial_cost_file_location, time_period_external_id=None):
        """Set an initial cost file location
        :param initial_cost_file_location location of an initial cost file
        :param time_period_external_id external id of the time period for which these initial costs apply
        """
        if (time_period_external_id == None):
            self._default_initial_cost_file_location = initial_cost_file_location
        else:
            self._initial_cost_location_dictionary[time_period_external_id] = initial_cost_file_location
            
    def register_costs(self, project, assignment):
        """Register the initial costs on the assignment
        :param project the project object for the current run
        :param assignment the traffic assignment builder object
        """
        time_periods_external_id_set = self._initial_cost_location_dictionary.keys()
        
        if self._default_initial_cost_file_location != None:
            default_initial_cost_counterpart = project.create_and_register_initial_link_segment_cost(self._network_instance.java, self._default_initial_cost_file_location)
            default_initial_cost_wrapper = InitialCostWrapper(default_initial_cost_counterpart)
            assignment.register_initial_link_segment_cost(default_initial_cost_wrapper.java)
            
        if len(time_periods_external_id_set) > 0:
            time_period_counterparts = self._demands_instance.get_registered_time_periods()
            for time_period_counterpart in time_period_counterparts:
                time_period = TimePeriodWrapper(time_period_counterpart)
                time_period_external_id = time_period.get_external_id()
                if (time_period_external_id in time_periods_external_id_set):
                    initial_cost_file_location = self._initial_cost_location_dictionary[time_period_external_id]
                    initial_cost_counterpart = project.create_and_register_initial_link_segment_cost(self._network_instance.java, initial_cost_file_location, time_period_counterpart)
                    initial_cost_wrapper = InitialCostWrapper(initial_cost_counterpart)
                    assignment.register_initial_link_segment_cost(time_period.java, initial_cost_wrapper.java)
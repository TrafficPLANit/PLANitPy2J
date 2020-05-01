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
    
    def __init__(self, assignment, project, network, demands):
        """Initializer for the InitialCosts class
        :param assignment the traffic assignment being used
        :param project the project being used
        :param network the network being used
        :param demands the demands object being used
        """
        self._assignment_instance = assignment
        self._project_instance = project
        self._network_instance = network
        self._demands_instance = demands
    
    def set(self, initial_costs_file_location, time_period_external_id=None):
        """Set the initial costs 
        :param initial_costs_file_location the location of the initial cost file, if initial costs being set
        :param time_period_external_id the id of the time period, if initial costs being set for each time period
        """
        if (time_period_external_id is None):
            initial_cost_counterpart = self._project_instance.create_and_register_initial_link_segment_cost(self._network_instance.java, initial_costs_file_location)
            initial_cost_wrapper = InitialCostWrapper(initial_cost_counterpart)
            self._assignment_instance.register_initial_link_segment_cost(initial_cost_wrapper.java)
        else:
            initial_cost_counterpart = self._project_instance.create_and_register_initial_link_segment_cost(self._network_instance.java, initial_costs_file_location)
            initial_cost_wrapper = InitialCostWrapper(initial_cost_counterpart)
            time_periods_counterpart = self._demands_instance.get_time_periods()
            time_periods = TimePeriodsWrapper(time_periods_counterpart)
            time_period_counterpart = time_periods.get_time_period_by_external_id(time_period_external_id);
            time_period = TimePeriodWrapper(time_period_counterpart)           
            self._assignment_instance.register_initial_link_segment_cost(time_period.java, initial_cost_wrapper.java)

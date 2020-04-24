import os, sys
this_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(this_path + "\\..")

from py4j.java_gateway import get_field
from planit import GatewayUtils
from planit import GatewayState
from planit import OutputType
from planit import RouteIdType
from planit import OutputProperty
from planit import PhysicalCost
from planit import VirtualCost
from planit import Smoothing

class BaseWrapper(object):
    """ Base wrapper class which always holds a java counter part instance and a generic way to pass on method calls to the encapsulated 
        Java instance. This allows one to use the Python naming conventions, i.e. get_x instead of getX() this is automatically catered for
        in these wrappers.
    """

    def __init__(self, java_counterpart):
        """Top-level constructor which defines the Java counterpart to each wrapper
            :param   the Java counterpart to the current object
        """
        self._java_counterpart = java_counterpart

    def __getattr__(self, name):
        """All methods invoked on the assignment wrapper are passed on to the Java equivalent class after transforming the method to
        Java style coding convention
        """            
        def method(*args): #collects the arguments of the function 'name' (wrapper function within getattr)    
            java_name = GatewayUtils.to_camelcase(name)
            # pass all calls on to the underlying PLANit project java class which is obtained via the entry_point.getProject call
            if( args ):
                return getattr(self._java_counterpart, java_name)(*args)
            else:
                return getattr(self._java_counterpart, java_name)()               
        return method
    
    @property
    def java(self):
        """ access to the underlying Java object if required
        """
        if (self._java_counterpart == None):
            raise Exception("No Java counterpart has been found for " + self.__class__.__name__)
        return self._java_counterpart 
    
    def field(self, fieldName):
        """ collect a publicly available member on the java object
        """
        return get_field(self.java, fieldName)


class AssignmentWrapper(BaseWrapper):
    """ Wrapper around the Java traffic assignment builder class instance
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
        self._output_configuration = OutputConfigurationWrapper(self.get_output_configuration()) # collect the output configuration from Java
        self._gap_function = GapFunctionWrapper(self.get_gap_function()) # collect the gap function from Java
        self._physical_cost_instance = None
        self._virtual_cost_instance = None    
        self._smoothing = None
        self._link_output_type_configuration = None
        self._origin_destination_output_type_configuration = None   
        self._path_output_type_configuration = None
     
    def set(self, assignment_component):
        """ Configure an assignment component on this assignment instance. Note that all these go via the traffic assignment builder in Java
            although we hide that on the Python side to not over-complicate things for the average user. Hence, the use of the self._builder in
            the method calls
        """    
        
        if isinstance(assignment_component, PhysicalCost):
            self._physical_cost_instance = PhysicalCostWrapper(self.create_and_register_physical_cost(assignment_component.value)) 
        elif isinstance(assignment_component, VirtualCost):
            self._virtual_cost_instance = VirtualCostWrapper(self.create_and_register_virtual_cost(assignment_component.value))
        elif isinstance(assignment_component, Smoothing):
            self._smoothing_instance = SmoothingWrapper(self.create_and_register_smoothing(assignment_component.value))
        else:
            raise Exception('Unrecognized component ' + assignment_component.type + ' cannot be set on assignment instance')
         
    def activate_output(self, output_type : OutputType):
        """ pass on to Java not as an Enum as Py4J does not seem to properly handle this at this stage
            instead we pass on the enum string which on the Java side is converted into the proper enum instead
            
            :param output_type Python enum of available output types
        """ 
        # collect an enum instance by collecting the <package>.<class_name> string from the Output type enum
        output_type_instance = GatewayState.python_2_java_gateway.entry_point.createEnum(output_type.java_class_name(), output_type.value)
        if output_type.value == "LINK":
            self._link_output_type_configuration = LinkOutputTypeConfigurationWrapper(self._java_counterpart.activateOutput(output_type_instance))
        elif output_type.value == "OD":
            self._origin_destination_output_type_configuration = OriginDestinationOutputTypeConfigurationWrapper(self._java_counterpart.activateOutput(output_type_instance))
        elif output_type.value == 'PATH':
            self._path_output_type_configuration = PathOutputTypeConfigurationWrapper(self._java_counterpart.activateOutput(output_type_instance))
        else:
            raise ValueError("Attempted to activate unknown output type " + output_type.value)

    @property
    def output_configuration(self):
        """Access to current output configuration
        """
        return self._output_configuration
    
    @property
    def gap_function(self):
        """Access to current gap function
        """
        return self._gap_function
    
    @property
    def link_configuration(self):
        """Access to current link output type configuration
        """
        return self._link_output_type_configuration
    
    @property
    def od_configuration(self):
        """Access to current origin-destination output type configuration
        """
        return self._origin_destination_output_type_configuration
    
    @property
    def path_configuration(self):
        """Access to current path output type configuration
        """
        return self._path_output_type_configuration
           
    @property
    def physical_cost(self):
        """Access to the physical cost wrapper
        """
        return self._physical_cost_instance
    
    @property
    def virtual_cost(self):
        """Access to the virtual cost wrapper
        """
        return self._virtual_cost_instance
    
    @property
    def smoothing(self):
        """Access to the smoothing wrapper
        """
        return self._smoothing_instance
    
class DemandsWrapper(BaseWrapper):
    """ Wrapper around the Java Demands class instance
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)    

class GapFunctionWrapper(BaseWrapper):
    """ Wrapper around the Java GapFunction class instance
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
        self._stop_criterion = StopCriterionWrapper(self.get_stop_criterion())  # collect the stop criterion from Java
        
    @property
    def stop_criterion(self):
        return self._stop_criterion

class ModeWrapper(BaseWrapper):
    """ Wrapper around the Java physical cost class instance
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
 
class OutputConfigurationWrapper(BaseWrapper):
    """ Wrapper around the Java output configuration class instance
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
 
class OutputFormatterWrapper(BaseWrapper):
    """ Wrapper around the Java OutputFormatter wrapper class instance
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)

class PlanItOutputFormatterWrapper(OutputFormatterWrapper):
    """ Wrapper around the Java PlanItOutputFormatter class instance
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
        # Initialize the output project path to the current run directory
        # Modellers may overwrite this default later
        project_path = os.getcwd()
        self.set_output_directory(project_path)

class MemoryOutputFormatterWrapper(OutputFormatterWrapper):
    """ Wrapper around the Java PlanItOutputFormatter class instance
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
        
class OutputTypeConfigurationWrapper(BaseWrapper): 
    """ Wrapper around the Java link output type configuration class instance
    """
     
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
        
    def add(self, output_property : OutputProperty):
        """Add an output type property to the current output type configuration
        """
        output_property_instance = GatewayState.python_2_java_gateway.entry_point.createEnum(output_property.java_class_name(), output_property.value)
        self._java_counterpart.addProperty(output_property_instance)
        
    def remove(self, output_property : OutputProperty):
        """Remove an output type property from the current output type configuration
        """
        output_property_instance = GatewayState.python_2_java_gateway.entry_point.createEnum(output_property.java_class_name(), output_property.value)
        return self._java_counterpart.removeProperty(output_property_instance)
        
    def remove_all_properties(self):
        self._java_counterpart.removeAllProperties()

class LinkOutputTypeConfigurationWrapper(OutputTypeConfigurationWrapper):
    """ Wrapper around the Java link output type configuration class instance
    """
     
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
        
class OriginDestinationOutputTypeConfigurationWrapper(OutputTypeConfigurationWrapper):
    """ Wrapper around the Java origin-destination output type configuration class instance
    """
     
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)

    def activate(self, od_skim_sub_output_type):
        """Activate an OD skim output type
        """
        od_skim_sub_output_type_instance = GatewayState.python_2_java_gateway.entry_point.createEnum(od_skim_sub_output_type.java_class_name(), od_skim_sub_output_type.value)
        self._java_counterpart.activateOdSkimOutputType(od_skim_sub_output_type_instance)
 
    def deactivate(self, od_skim_sub_output_type):
        """Deactivate an OD skim output type
        """
        od_skim_sub_output_type_instance = GatewayState.python_2_java_gateway.entry_point.createEnum(od_skim_sub_output_type.java_class_name(), od_skim_sub_output_type.value)
        self._java_counterpart.deactivateOdSkimOutputType(od_skim_sub_output_type_instance)
        
class PathOutputTypeConfigurationWrapper(OutputTypeConfigurationWrapper):
    """ Wrapper around the Java path output type configuration class instance
    """
     
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
        
    def set_path_id_type(self,  route_id_type : RouteIdType):
        route_id_type_instance = GatewayState.python_2_java_gateway.entry_point.createEnum(route_id_type.java_class_name(), route_id_type.value)
        self._java_counterpart.setPathIdType(route_id_type_instance)
        
class PhysicalCostWrapper(BaseWrapper):
    """ Wrapper around the Java physical cost class instance
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
        
class InitialCostWrapper(BaseWrapper):
    """ Wrapper around the Java initial cost class instance
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
        
class PhysicalNetworkWrapper(BaseWrapper):
    """ Wrapper around the Java physical network class instance
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
        
class PlanItInputBuilderWrapper(BaseWrapper):
    """ Wrapper around the Java InputBuilderListener class instance
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)    

class SmoothingWrapper(BaseWrapper):
    """ Wrapper around the Java Smoothing class instance
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
        
class StopCriterionWrapper(BaseWrapper):
    """ Wrapper around the Java StopCriterion class instance
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
    
class TimePeriodWrapper(BaseWrapper):
    """ Wrapper around the Java physical cost class instance
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)

class VirtualCostWrapper(BaseWrapper):
    """ Wrapper around the Java assignment class instance
    """    
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)

class ZoningWrapper(BaseWrapper):
    """ Wrapper around the Java Zoning class instance
    """    
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
                
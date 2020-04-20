from enum import Enum

class Network(Enum):
    """ Enum for the different virtual costs the user can choose, they map to the Java equivalent class name for easy mapping
    """
    MACROSCOPIC = "org.planit.network.physical.macroscopic.MacroscopicNetwork"
    PHYSICAL = "org.planit.network.physical.PhysicalNetwork"
    VIRTUAL = "org.planit.network.virtual.VirtualNetwork"
    
class OutputFormatter(Enum):
    """ Enum for the different output formatters the user can choose, they map to the Java equivalent class name for easy mapping
        Only the output formatters available in the PLANitIO project have been defined here
    """
    
    MEMORY = "org.planit.output.formatter.MemoryOutputFormatter"
    PLANIT_IO = "org.planit.io.output.formatter.PlanItOutputFormatter"
    
class OutputProperty(Enum):    
    """ Enum for the different output properties the user can configure in the output files 
        Equivalent of Java enumeration org.planit.output.property.OutputProperty
    """
    DENSITY = "DENSITY"
    LINK_SEGMENT_ID = "LINK_SEGMENT_ID"
    LINK_SEGMENT_EXTERNAL_ID = "LINK_SEGMENT_EXTERNAL_ID"
    MODE_ID = "MODE_ID"
    MODE_EXTERNAL_ID = "MODE_EXTERNAL_ID"
    MAXIMUM_SPEED = "MAXIMUM_SPEED"
    CALCULATED_SPEED = "CALCULATED_SPEED"
    FLOW = "FLOW"
    LENGTH = "LENGTH"
    UPSTREAM_NODE_ID = "UPSTREAM_NODE_ID"
    UPSTREAM_NODE_EXTERNAL_ID = "UPSTREAM_NODE_EXTERNAL_ID"
    DOWNSTREAM_NODE_ID = "DOWNSTREAM_NODE_ID"
    DOWNSTREAM_NODE_EXTERNAL_ID = "DOWNSTREAM_NODE_EXTERNAL_ID"
    CAPACITY_PER_LANE = "CAPACITY_PER_LANE"
    NUMBER_OF_LANES = "NUMBER_OF_LANES"
    LINK_COST = "LINK_COST"
    OD_COST = "OD_COST"
    DOWNSTREAM_NODE_LOCATION = "DOWNSTREAM_NODE_LOCATION"
    UPSTREAM_NODE_LOCATION = "UPSTREAM_NODE_LOCATION"
    ITERATION_INDEX = "ITERATION_INDEX" 
    ORIGIN_ZONE_ID = "ORIGIN_ZONE_ID"
    ORIGIN_ZONE_EXTERNAL_ID = "ORIGIN_ZONE_EXTERNAL_ID"
    DESTINATION_ZONE_ID = "DESTINATION_ZONE_ID"
    DESTINATION_ZONE_EXTERNAL_ID = "DESTINATION_ZONE_EXTERNAL_ID"
    TIME_PERIOD_ID = "TIME_PERIOD_ID"
    TIME_PERIOD_EXTERNAL_ID = "TIME_PERIOD_EXTERNAL_ID"
    RUN_ID = "RUN_ID"
    TOTAL_COST_TO_END_NODE = "TOTAL_COST_TO_END_NODE" 
    PATH = "PATH"
    VC_RATIO = "VC_RATIO"
    COST_TIMES_FLOW = "COST_TIMES_FLOW"
    LINK_TYPE = "LINK_TYPE"
    
    def java_class_name(self) -> str:
        return "org.planit.output.property.OutputProperty"     
    
class OutputType(Enum):
    """ Enum for the different output types the user can choose to activate, 
         Equivalent of Java enumeration org.planit.output.OutputType
    """
    LINK = "LINK"
    GENERAL = "GENERAL"
    SIMULATION = "SIMULATION"
    OD = "OD"
    PATH = "PATH"
    
    def java_class_name(self) -> str:
        return "org.planit.output.enums.OutputType"   
    
class InitialCost(Enum):  
    """Enum for Initial Cost types.  There is only one type, but defining this enum allows the PLANit.set() method to define initial costs
    """
    LINK_SEGMENT = "LINK_SEGMENT"

class PhysicalCost(Enum):
    """ Enum for the different physical costs the user can choose, they map to the Java equivalent class name for easy mapping
    """
    BPR = "org.planit.cost.physical.BPRLinkTravelTimeCost"
    LINK = "org.planit.cost.physical.LinkTravelTimeCost"

class RouteIdType(Enum):

    LINK_SEGMENT_EXTERNAL_ID = "LINK_SEGMENT_EXTERNAL_ID"
    LINK_SEGMENT_ID = "LINK_SEGMENT_ID"
    NODE_EXTERNAL_ID = "NODE_EXTERNAL_ID"
    NODE_ID = "NODE_ID"

    def java_class_name(self) -> str:
        return "org.planit.output.enums.RouteIdType"     
   
class Smoothing(Enum):
    """ Enum for the different smoothing options the user can choose, they map to the Java equivalent class name for easy mapping
    """
    MSA = "org.planit.sdinteraction.smoothing.MSASmoothing"

class TrafficAssignment(Enum):
    """ Enum for the different assignment the user can choose, they map to the Java equivalent class name for easy mapping
    """
    TRADITIONAL_STATIC = "org.planit.trafficassignment.TraditionalStaticAssignment"
    ETLM = "org.planit.ltm.trafficassignment.ETLM"

class VirtualCost(Enum):
    """ Enum for the different virtual costs the user can choose, they map to the Java equivalent class name for easy mapping
    """
    FIXED = "org.planit.cost.virtual.FixedConnectoidTravelTimeCost"
    
class ODSkimSubOutputType(Enum):
    
    NONE = "NONE"
    COST = "COST"

    def java_class_name(self) -> str:
        return "org.planit.output.enums.ODSkimSubOutputType"     

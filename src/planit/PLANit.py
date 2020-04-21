import os, sys
this_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(this_path + "\\..")
import subprocess
import traceback
from py4j.java_gateway import JavaGateway
from planit import GatewayUtils
from planit import GatewayState
from planit import GatewayConfig
from planit import BaseWrapper 
from planit import PhysicalNetworkWrapper 
from planit import DemandsWrapper
from planit import AssignmentWrapper
from planit import ZoningWrapper
from planit import PlanItOutputFormatterWrapper
from planit import MemoryOutputFormatterWrapper
from planit import TrafficAssignment
from planit import OutputFormatter
from planit import InitialCost
#===============================================================================
# from planit import InitialCostWrapper
# from planit import TimePeriodWrapper
#===============================================================================
from builtins import isinstance

class PLANit:
            
    def __init__(self, project_path=None, standalone=True):
        """Constructor of PLANit python wrapper which acts as an interface to the underlying PLANit Java code
        :param project_path: the path location of the XML input file(s) to be used by PLANitIO
        :param standalone: when true this PLANit instance bootstraps a java gateway and closes it upon completion of the scripts when false <to be implemented>
        """  
        # explicitly set uninitialized member variables to None
        self._assignment_instance = None
        self._input_builder_instance = None
        self._network_instance = None
        self._zoning_instance = None
        self._demands_instance = None
        self._project_instance = None
        self._io_output_formatter_instance = None
        self._memory_output_formatter_instance = None
        self._initial_cost_instance = None
        
        if not standalone:
            raise Exception('Standalone argument can only be true at this time, server mode not yet supported')  
        self.__start_java__()
        self.__initialize_project__(project_path)
       
    def __start_java__(self):            
        """Start the gateway to Java 
        """  
        
        #find the location of this file, so that other directories can be located relative to it    
        dir_path = os.path.dirname(os.path.realpath(__file__))
        # Bootstrap the java gateway server
        if not GatewayState.gateway_is_running:
            # register dependencies
            dependencySet = {
                dir_path + "\\" + GatewayConfig.JAVA_P4J_JAR_PATH,
                dir_path + "\\" + GatewayConfig.JAVA_PLANIT_WRAPPER_PATH,
                dir_path + "\\" + GatewayConfig.JAVA_PLANIT_JAR_PATH,
                dir_path + "\\" + GatewayConfig.JAVA_PLANIT_IO_JAR_PATH}
            dependencySeparator = ';'
            fullString = dependencySeparator.join(dependencySet)
            
            cmd = ['java', '-classpath', fullString, GatewayConfig.JAVA_GATEWAY_WRAPPER_CLASS]            
            GatewayState.planit_java_process = subprocess.Popen(cmd)           
             
            # now we  connect to the gateway
            GatewayState.python_2_java_gateway = JavaGateway()
            GatewayState.gateway_is_running = True            
                
            #TODO: Note we are not waiting for it to setup properly --> possibly considering some mechanism to wait for this to ensure proper connection!
            print('Java interface running with PID: '+ str(GatewayState.planit_java_process.pid))            
        else:
            raise Exception('PLANit java interface already running, only a single instance allowed at this point')
    
    def __initialize_project__(self, project_path):
        """Initialize the project using the input file in the directory specified by project_path
        """
        if project_path == None:
            project_path = os.getcwd()
        self._project_instance = BaseWrapper(GatewayState.python_2_java_gateway.entry_point.initialiseSimpleProject(project_path))

        # The one macroscopic network, zoning, demand is created and populated and wrapped in a Python object
        # (Note1: to access public members in Java, we must collect it via the field method in the wrapper)
        # (Note2: since we only have a single network, demand, zoning, we do not have a wrapper for the fields, so we must access the methods directly
        self._network_instance = PhysicalNetworkWrapper(self._project_instance.field("physicalNetworks").getFirstNetwork())
        # the one zoning is created and populated
        self._zoning_instance = ZoningWrapper(self._project_instance.field("zonings").getFirstZoning())
        # the one demands is created and populated
        self._demands_instance = DemandsWrapper(self._project_instance.field("demands").getFirstDemands())
        
    def __del__(self):
        """Destructor of PLANit object which shuts down the connection to Java
        """
        self.__stop_java__()
        
    def __stop_java__(self):        
        """Cleans up the gateway in Java in case this has not been done yet. It assumes a single instance available in Python tied
        to a particular self. Only that instance is allowed to terminate the gateway.
        """          
        # Let the instance that instantiated the connection also terminate it automatically
        if GatewayState.gateway_is_running:
            # Check if the process has really terminated & force kill if not.           
            try:
                GatewayState.python_2_java_gateway.shutdown()
                GatewayState.planit_java_process.terminate()
                if (GatewayState.planit_java_process.poll() != None):
                    os.kill(GatewayState.planit_java_process.pid, 0)
                    GatewayState.planit_java_process.kill()
                GatewayState.gateway_is_running = False
                GatewayState.python_2_java_gateway = None
                print ("Forced kill of PLANitJava interface")
            except OSError:
                print ("Terminated PLANitJava interface")   
            except:
                traceback.print_exc()         
        
    #def set(self, assignment_component, initial_costs_file_location=None, time_period_id=None):
    def set(self, assignment_component):
        """Set the traffic assignment component
        :param assignment_component the  assignment component, can be TrafficAssignment or InitialCost
        :param initial_costs_file_location the location of the initial cost file, if initial costs being set
        :param time_period_id the id of the time period, if initial costs being set for each time period
        """
        if isinstance(assignment_component, TrafficAssignment):
            assignment_counterpart = self._project_instance.create_and_register_traffic_assignment(assignment_component.value)
            self._assignment_instance = AssignmentWrapper(assignment_counterpart)
            self._initial_cost_instance = InitialCost(self._assignment_instance, self._project_instance, self._network_instance, self._demands_instance)
            
    def activate(self, formatter_component):
        """Activate an output formatter
        :param formatter_component the formatter being set up
        """
        if formatter_component == OutputFormatter.PLANIT_IO:
            io_output_formatter_counterpart = self._project_instance.create_and_register_output_formatter(formatter_component.value)
            io_output_formatter = PlanItOutputFormatterWrapper(io_output_formatter_counterpart)
            self._io_output_formatter_instance = io_output_formatter
        elif formatter_component == OutputFormatter.MEMORY:
            memory_output_formatter_counterpart =  self._project_instance.create_and_register_output_formatter(formatter_component.value)
            memory_output_formatter = MemoryOutputFormatterWrapper(memory_output_formatter_counterpart)
            self._memory_output_formatter_instance = memory_output_formatter

    def run(self):  
        """Run the traffic assignment.  Register any output formatters which have been set up
        """
        if (self._io_output_formatter_instance is not None):
            project_path_set = self._io_output_formatter_instance.is_xml_directory_set()
            if (not project_path_set):
                project_path = os.getcwd()
                self._io_output_formatter_instance.set_output_directory(project_path)
            self._assignment_instance.register_output_formatter(self._io_output_formatter_instance.java);
        if (self._memory_output_formatter_instance is not None):
            self._assignment_instance.register_output_formatter(self._memory_output_formatter_instance.java);
        self._project_instance.execute_all_traffic_assignments()      
        
    def __getattr__(self, name):
        """ all methods invoked on the PLANit Java gateway wrapper as passed on to it without the user seeing the actual gateway. This is to be
        replaced by a more intricate interface which exposes only the properties users are allowed to configure to create a PLANit instance
        """        
        def method(*args): #collects the arguments of the function 'name' (wrapper function within getattr)                
            if GatewayState.gateway_is_running:
                java_name = GatewayUtils.to_camelcase(name)
                # pass all calls on to the underlying PLANit project java class which is obtained via the entry_point.getProject call
                return getattr(GatewayState.planit_project, java_name)(*args) # invoke without arguments
            else:
                raise Exception('PLANit java interface not available')      
        return method
                                        
    @property
    def assignment(self):
        """ access to the assignment builder 
        """
        return self._assignment_instance  
    
    @property
    def project(self):
        """access to the project
        """
        return self._project_instance
    
    @property
    def network(self):
        """access to the network
        """
        return self._network_instance
    
    @property
    def demands(self):
        """access to the demands
        """
        return self._demands_instance
    
    @property
    def io_output_formatter(self):
        #def output(self):
        """access to PLANitIO output formatter
        """
        return self._io_output_formatter_instance
    
    @property
    def memory_output_formatter(self):
        #def memory
        """access to memory output formatter
        """
        return self._memory_output_formatter_instance
    
    @property
    def initial_cost(self):
        """access to initial cost
        """
        return self._initial_cost_instance
    
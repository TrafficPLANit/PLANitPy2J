import os
import subprocess
import traceback

from py4j.java_gateway import JavaGateway

from planit.wrappers import BaseWrapper 
from planit.gateway import GatewayUtils
from planit.gateway import GatewayState
from planit.gateway import GatewayConfig
from planit.wrappers import PhysicalNetworkWrapper 
from planit.wrappers import DemandsWrapper
from planit.wrappers import AssignmentWrapper
from planit.wrappers import ZoningWrapper
from planit.wrappers import PlanItOutputFormatterWrapper
from planit.wrappers import MemoryOutputFormatterWrapper
from planit.enums import TrafficAssignment
from planit.enums import OutputFormatter
from builtins import isinstance

class PLANit:
            
    def __init__(self, project_path, standalone=True):
        """Constructor of PLANit python wrapper which acts as an interface to the underlying PLANit Java code
        :param standalone: when true this PLANit instance bootstraps a java gateway and closes it upon completion of the scripts when false <to be implemented>
        :param project_path: the path location of the XML input file(s) to be used by PLANitIO
        """  
        # explicitly set uninitialized member variables to None
        self._assignment_instance = None
        self._input_builder_instance = None
        self._network_instance = None
        self._zoning_instance = None
        self._demands_instance = None
        self._project_instance = None
        
        if not standalone:
            raise Exception('Standalone argument can only be true at this time, server mode not yet supported')  
        self.start_java()
        self.initialize_project(project_path)
       
    def start_java(self):            
        """Start the gateway to Java 
        """  
        
        # Bootstrap the java gateway server
        if not GatewayState.gateway_is_running:
            # register dependencies
            dependencySet = {
                GatewayConfig.JAVA_P4J_JAR_PATH,
                GatewayConfig.JAVA_PLANIT_WRAPPER_PATH,
                GatewayConfig.JAVA_PLANIT_JAR_PATH,
                GatewayConfig.JAVA_PLANIT_IO_JAR_PATH}
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
    
    def initialize_project(self, project_path):
        self._project_instance = BaseWrapper(GatewayState.python_2_java_gateway.entry_point.initialiseSimpleProject2(project_path))
        # The one macroscopic network, zoning, demand is created and populated and wrapped in a Python object
        # (Note1: to access public members in Java, we must collect it via the field method in the wrapper)
        # (Note2: since we only have a single network, demand, zoning, we do not have a wrapper for the fields, so we must access the methods directly
        self._network_instance = PhysicalNetworkWrapper(self._project_instance.field("physicalNetworks").getFirstNetwork())
        # the one zoning is created and populated
        self._zoning_instance = ZoningWrapper(self._project_instance.field("zonings").getFirstZoning())
        # the one demands is created and populated
        self._demands_instance = DemandsWrapper(self._project_instance.field("demands").getFirstDemands())
        
    def set(self, assignment_component):
        if isinstance(assignment_component, TrafficAssignment):
            assignment_counterpart = self._project_instance.create_and_register_traffic_assignment(assignment_component.value)
            self._assignment_instance = AssignmentWrapper(assignment_counterpart)
        elif isinstance(assignment_component, OutputFormatter):
            if assignment_component == OutputFormatter.PLANIT_IO:
                xml_output_formatter_counterpart = self._project_instance.create_and_register_output_formatter(assignment_component.value)
                xml_output_formatter = PlanItOutputFormatterWrapper(xml_output_formatter_counterpart)
                self._assignment_instance.set(xml_output_formatter)
            elif assignment_component == OutputFormatter.MEMORY:
                memory_output_formatter_counterpart =  self._project_instance.create_and_register_output_formatter(assignment_component.value)
                memory_output_formatter = MemoryOutputFormatterWrapper(memory_output_formatter_counterpart)
                self._assignment_instance.set(memory_output_formatter)

        
    def __del__(self):
        self.stop_java()
        
    def stop_java(self):        
        """the destructor cleans up the gateway in Java in case this has not been done yet. It assumes a single instance available in Python tied
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
    
    def run(self):  
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
    
    @assignment.setter
    def assignment(self, assignment):
        self._assignment_instance = assignment
    
    @property
    def network(self):
        """ access to the network instance
        """
        return self._network_instance
    
    @network.setter
    def network(self, network):
        self._network_instance = network
    
    @property
    def zoning(self):
        """ access to the zoning instance
        """
        return self._zoning_instance
    
    @zoning.setter
    def zoning(self, zoning):
        self._zoning_instance = zoning
       
    @property
    def demands(self):
        """ access to the demands instance
        """
        return self._demands_instance 
    
    @demands.setter
    def demands(self, demands):
        self._demands_instance = demands
       
    @property
    def project(self):   
        return self._project_instance          
    
    @project.setter     
    def project(self, project):     
        self._project_instance = project
        
import re
import os
from planit import Version

class GatewayConfig(object):   
    # jar class path entries since the java install might not have them on their class path (even if Python does)
    JAVA_PY4J_JAR_PATH =  '..\\..\\rsc\\py4j'+str(Version.py4j)+'.jar'
    # jar for the PLANit code
    JAVA_PLANIT_JAR_PATH = '..\\..\\rsc\\PLANit-'+str(Version.planit)+'.jar'
    # jar for the default I/O implementation of the PLANit core used by simple project implementation
    JAVA_PLANIT_IO_JAR_PATH = '..\\..\\rsc\\PLANitIO-'+str(Version.planit)+'.jar'

    # the main entry point of the Java gateway implementation for PLANit
    JAVA_GATEWAY_WRAPPER_CLASS =  'org.planit.python.PLANitJ2Py'
    # jar for the gateway server wrapper
    JAVA_PLANIT_PY2J_PATH = '..\\..\\rsc\\PLANitJ2Py-'+str(Version.planit)+'.jar'
    
class GatewayState(object):
    #Create a static variable which flags if the java server already is running or not
    gateway_is_running = False
    planit_java_process = None
    # The actual gateway to pass on requests to once the gateway server is known to be running
    python_2_java_gateway = None
    # will contain reference to the Java project instance once the gateway is up and running        
    planit_project = None 


class GatewayUtils(object):
 
    @staticmethod
    def to_camelcase(s):
            """ convert a Python style string into a Java style string regarding method calls and variable names. Especially useful to avoid
            having to call Java functions as Java functions but one can call them as Python functions which are dynamically changed to their
            Java counterparts
            """
            return re.sub(r'(?!^)_([a-zA-Z])', lambda m: m.group(1).upper(), s) 


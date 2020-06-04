import re
import os
import sys

from planit import Version

class GatewayConfig(object):   

    # Currently we provide the paths for the local environment AND production environment
    # TODO there should be a mechanism such that we only need one type of definition
    
    RELEASE_SHARE_PATH = os.path.split(sys.executable)[0]+'\\share'
    IDE_SHARE_PATH = '..\\..\\share'
    
    PLANIT_SHARE = '\\planit'
    PY4J_SHARE = '\\py4j'
    
    # IDE
    # jar for the PLANit code
    JAVA_PLANIT_PATH_IDE =          IDE_SHARE_PATH+PLANIT_SHARE+'\\PLANit-'+str(Version.planit)+'.jar'
    # jar for the default I/O implementation of the PLANit core used by simple project implementation
    JAVA_PLANIT_IO_PATH_IDE =       IDE_SHARE_PATH+PLANIT_SHARE+'\\PLANitIO-'+str(Version.planit)+'.jar'
    # jar for the gateway server wrapper
    JAVA_PLANIT_PY2J_PATH_IDE =         IDE_SHARE_PATH+PLANIT_SHARE+'\\PLANitJ2Py-'+str(Version.planit)+'.jar'
    # jar for py4j jar dependency
    JAVA_PY4J_PATH_IDE =                IDE_SHARE_PATH+PY4J_SHARE+'\\py4j'+str(Version.py4j)+'.jar'
    
    # PRODUCTION
    # jar for the PLANit code
    JAVA_PLANIT_PATH_RELEASE =      RELEASE_SHARE_PATH+PLANIT_SHARE+'\\PLANit-'+str(Version.planit)+'.jar'
    # jar for the default I/O implementation of the PLANit core used by simple project implementation
    JAVA_PLANIT_IO_PATH_RELEASE =   RELEASE_SHARE_PATH+PLANIT_SHARE+'\\PLANitIO-'+str(Version.planit)+'.jar'
    # jar for the gateway server wrapper
    JAVA_PLANIT_PY2J_PATH_RELEASE =     RELEASE_SHARE_PATH+PLANIT_SHARE+'\\PLANitJ2Py-'+str(Version.planit)+'.jar'
        # jar for py4j jar dependency
    JAVA_PY4J_PATH_RELEASE =            RELEASE_SHARE_PATH+PY4J_SHARE+'\\py4j'+str(Version.py4j)+'.jar'

    # the main entry point of the Java gateway implementation for PLANit
    JAVA_GATEWAY_WRAPPER_CLASS =  'org.planit.python.PLANitJ2Py'
    
    
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


import datetime
import re
import os
import sys
from enum import Enum

from py4j.java_collections import SetConverter, MapConverter, ListConverter

from planit import Version
from builtins import staticmethod

class GatewayConfig(object):   

    # Currently we provide the paths for the local environment AND production environment
    # TODO there should be a mechanism such that we only need one type of definition
    
    RELEASE_SHARE_PATH = os.path.join(os.path.split(sys.executable)[0], 'share')
    IDE_SHARE_PATH = os.path.join('..', '..', 'share')
    # VENV (virtual environment) for Python erroneously results in sys.executable pointing NOT to the root
    # directory of the virtual environment, but to ./Scripts. Hence, we must account for that by alos looking
    # one directory upward.
    # This (as far as I know) is a bug in venv!
    VENV_RELEASE_SHARE_PATH = os.path.join(os.path.split(sys.executable)[0], '..', 'share')
    
    PLANIT_SHARE = os.path.join('planit', '*')
    PY4J_SHARE = os.path.join('py4j', '*')
    
    # the main entry point of the Java gateway implementation for PLANit
    JAVA_GATEWAY_WRAPPER_CLASS =  'org.goplanit.python.PLANitJ2Py'
    
    
class GatewayState(object):
    """ the access to the Java side 
    """
    
    #Create a static variable which flags if the java server already is running or not
    gateway_is_running = False
    planit_java_process = None
    # The actual gateway to pass on requests to once the gateway server is known to be running
    python_2_java_gateway = None
    # will contain reference to the Java project instance once the gateway is up and running        
    planit_project = None 


class GatewayUtils(object):
    """ Utilities for the Java gateway
    """
 
    @staticmethod
    def to_camelcase(s):
            """ convert a Python style string into a Java style string regarding method calls and variable names. Especially useful to avoid
            having to call Java functions as Java functions but one can call them as Python functions which are dynamically changed to their
            Java counterparts
            """
            return re.sub(r'(?!^)_([a-zA-Z])', lambda m: m.group(1).upper(), s) 

    @staticmethod
    def convert_args_to_java(args):
        """ convert passed in arguments to java versions if needed. Required for containers which cannot be mapped one on
        one to Java. 1) Python List is converted to Java ArrayList.

        :param args: to convert where needed, assumed iterable
        :return converted args to use  
        """
        converted_args = []
        for arg in args:
            
            # convert Python List to Java ArrayList. For some reason the built-in converter does not work properly,
            # so we do it ourselves but along the same lines. Main difference is instantiation of the array list via
            # gateway
            if isinstance(arg, list):
                java_list = GatewayState.python_2_java_gateway.jvm.java.util.ArrayList()
                for element in arg:
                    java_list.add(element)
                arg = java_list
            if isinstance(arg, datetime.time):
                arg = GatewayUtils.to_java_local_time(arg)
            converted_args.append(arg)
        return converted_args
    
    @staticmethod
    def to_java_array(object_class, python_list):
        """ convert a Python list to a Java array
        :param object_class the Java class type to use for the array instances
        :param python_list to populate the array with
        :return java array created in Python with the contents of the Python list
        """ 
        java_array = GatewayState.python_2_java_gateway.new_array(object_class, len(python_list))
        for i in range(len(python_list)):
            java_array[i]=python_list[i]
        return java_array

    @staticmethod
    def to_java_local_time(time: datetime.time):
        """ convert a Python datetime.time to a Java LocalTime
        :param time: the python time instance
        :return java LocalTime instance representing the same time as time
        """
        return GatewayState.python_2_java_gateway.jvm.java.time.LocalTime.of(
            time.hour, time.minute, time.second, time.microsecond * 1000)

    @staticmethod
    def to_java_enum(python_planit_enum: Enum):
        """ convert Python predefined enum to Java counterpart.

        :param python_planit_enum: type to convert
        :return java counterpart
        """
        return GatewayState.python_2_java_gateway.entry_point.createEnum(
            python_planit_enum.java_class_name(), python_planit_enum.value)
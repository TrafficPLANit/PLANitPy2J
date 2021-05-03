import os

from py4j.java_gateway import get_field
from planit import GatewayUtils
from planit import GatewayState
from planit import BaseWrapper
from _decimal import Decimal
from numpy import string_

    
class ConverterWrapper(BaseWrapper):
    """ Wrapper around a Java Converter class instance which in turn has more specific implementations for which
    we also provide wrapper classes, e.g. Network, Zoning, Intermodal etc.
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart) 
    
            
class ReaderSettingsWrapper(BaseWrapper):
    """ Wrapper around settings for a reader used by converter
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
        
class ReaderWrapper(BaseWrapper):
    """ Wrapper around a Java Reader class instance which in turn has more specific implementations for which
    we also provide wrapper classes, e.g. NetworkReader, ZoningReader, IntermodalReader etc.
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart) 
        
        # wrap the java settings that we expose as a property for this reader in a "ReaderSettingsWrapper"
        # this way we have a general wrapper for all settings instances exposed to the user, while not having to create
        # separate wrapper classes for each specific implementation (as long as the settings themselves do not expose any other
        # classes that need to be wrapper this will work
        self._settings = ReaderSettingsWrapper(self.get_settings())
        
    @property
    def settings(self) -> ReaderSettingsWrapper:
        """ access to the settings of this reader wrapper 
        """
        return self._settings                                     
             
class WriterSettingsWrapper(BaseWrapper):
    """ Wrapper around settings for a reader used by converter
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)      
        
class WriterWrapper(BaseWrapper):
    """ Wrapper around a Java Writer class instance which in turn has more specific implementations for which
    we also provide wrapper classes, e.g. NetworkWriter, ZoningWriter, IntermodalWriter etc.
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
        # wrap the java settings that we expose as a property for this writer in a "WriterSettingsWrapper"
        # this way we have a general wrapper for all settings instances exposed to the user, while not having to create
        # separate wrapper classes for each specific implementation (as long as the settings themselves do not expose any other
        # classes that need to be wrapper this will work
        self._settings = WriterSettingsWrapper(self.get_settings())
        
    @property
    def settings(self) -> WriterSettingsWrapper:
        """ access to the settings of this writer wrapper 
        """
        return self._settings                               
        
##########################################################
# Double derived wrappers
##########################################################
        
        
class IntermodalConverterWrapper(ConverterWrapper):
    """ Wrapper around the Java IntermodalConverter class instance
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)  
        
class IntermodalReaderWrapper(ReaderWrapper):
    """ Wrapper around the Java IntermodalReader class instance, derived implementation are more specific, e.g. OsmIntermodalReaderWrapper
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
            
class IntermodalWriterWrapper(WriterWrapper):
    """ Wrapper around the Java IntermodalWriter class instance, derived implementations are more specific, e.g. MatsimIntermodalWriterWrapper
    """  
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)          
   
class NetworkConverterWrapper(ConverterWrapper):
    """ Wrapper around the Java NetworkConverter class instance
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)    
    
class NetworkReaderWrapper(ReaderWrapper):
    """ Wrapper around the Java NetworkReader class instance, derived implementation are more specific, e.g. OsmNetworkReaderWrapper
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
    
class NetworkWriterWrapper(WriterWrapper):
    """ Wrapper around the Java NetworkWriter class instance, derived implementations are more specific, e.g. MatsimNetworkWriterWrapper
    """  
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)            
                
        
##########################################################
# Triple derived wrappers
##########################################################

class MatsimIntermodalWriterSettingsWrapper(WriterSettingsWrapper):
    """ Wrapper around settings for an intermodal Matsim writer used by converter
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
        
        # Matsim intermodal writer settings allow access to network and zoning settings component
        # which in turns are settings 
        self._network_settings = WriterSettingsWrapper(self.get_network_settings())
        self._zoning_settings = WriterSettingsWrapper(self.get_zoning_settings())
    
    @property
    def network_settings(self):
        return self._network_settings
    
    @property
    def zoning_settings(self):
        return self._zoning_settings

class MatsimIntermodalWriterWrapper(IntermodalWriterWrapper):
    """ Wrapper around the Java PlanitMatsimNetworkWriter class
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
        
         # replace regular reader settings by Matsim intermodal reader settings
        self._settings = MatsimIntermodalWriterSettingsWrapper(self._settings.java)       

class MatsimNetworkWriterWrapper(NetworkWriterWrapper):
    """ Wrapper around the Java PlanitMatsimNetworkWriter class
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
        
class OsmIntermodalReaderSettingsWrapper(ReaderSettingsWrapper):
    """ Wrapper around settings for an OSM intermodal reader used by converter
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
        
        # OSM intermodal reader settings allow access to network and pt settings component
        # which in turns are settings 
        self._network_settings = ReaderSettingsWrapper(self.get_network_settings())
        self._pt_settings = ReaderSettingsWrapper(self.get_public_transport_settings())
    
    @property
    def network_settings(self):
        return self._network_settings
    
    @property
    def pt_settings(self):
        return self._pt_settings         
        
class OsmIntermodalReaderWrapper(IntermodalReaderWrapper):
    """ Wrapper around the Java PlanitOsmIntermodalReader class
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)     
        
         # replace regular reader settings by planit intermodal reader settings
        self._settings = OsmIntermodalReaderSettingsWrapper(self._settings.java)
        
class OsmNetworkReaderSettingsWrapper(ReaderSettingsWrapper):
    """ Wrapper around settings for an OSM network reader used by converter
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
        
        # OSM intermodal reader settings allow access to network and pt settings component
        # which in turns are settings 
        self._highway_settings = ReaderSettingsWrapper(self.get_highway_settings())
        self._railway_settings = ReaderSettingsWrapper(self.get_railway_settings())
    
    @property
    def highway_settings(self):
        return self._highway_settings
    
    @property
    def railway_settings(self):
        return self._railway_settings           

class OsmNetworkReaderWrapper(NetworkReaderWrapper):
    """ Wrapper around the Java PlanitOsmNetworkReader class
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
        
        # OSM network reader settings allow access to highway and railway settings component
        # requiring a dedicated wrapper -> use this wrapper instead of generic settings wrapper
        self._settings = OsmNetworkReaderSettingsWrapper(self.settings.java)
        
class PlanitIntermodalReaderSettingsWrapper(ReaderSettingsWrapper):
    """ Wrapper around settings for a planit intermodal reader (native format) used by converter
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
        
        # planit intermodal reader settings allow access to network and zoning settings component
        # which in turns are settings 
        self._network_settings = ReaderSettingsWrapper(self.get_network_settings())
        self._zoning_settings = ReaderSettingsWrapper(self.get_zoning_settings())
    
    @property
    def network_settings(self):
        return self._network_settings
    
    @property
    def zoning_settings(self):
        return self._zoning_settings 
        
class PlanitIntermodalReaderWrapper(IntermodalReaderWrapper):
    """ Wrapper around the Java native format based PlanitIntermodalReader class
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
        
        # replace regular reader settings by planit intermodal reader settings
        self._settings = PlanitIntermodalReaderSettingsWrapper(self._settings.java) 
               
class PlanitIntermodalWriterSettingsWrapper(WriterSettingsWrapper):
    """ Wrapper around settings for a intermodal planit writer (native format) used by converter
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
        
        # planit intermodal writer settings allow access to network and zoning settings component
        # which in turns are settings 
        self._network_settings = WriterSettingsWrapper(self.get_network_settings())
        self._zoning_settings = WriterSettingsWrapper(self.get_zoning_settings())
    
    @property
    def network_settings(self):
        return self._network_settings
    
    @property
    def zoning_settings(self):
        return self._zoning_settings
        
class PlanitIntermodalWriterWrapper(IntermodalWriterWrapper):
    """ Wrapper around the Java native format based PlanitIntermodalWriter class
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
        
         # replace regular writer settings by Planit intermodal reader settings
        self._settings = MatsimIntermodalWriterSettingsWrapper(self._settings.java)  
        
class PlanitNetworkReaderWrapper(NetworkReaderWrapper):
    """ Wrapper around the Java native format based PlanitNetworkReader class
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
        
class PlanitNetworkWriterWrapper(NetworkWriterWrapper):
    """ Wrapper around the Java native format based PlanitNetworkWriter class
    """
    
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)
from planit import ConverterType
from planit import GatewayState
from planit import MatsimNetworkWriterWrapper
from planit import NetworkReaderType
from planit import NetworkReaderWrapper
from planit import NetworkWriterType
from planit import NetworkWriterWrapper
from planit import OsmNetworkReaderWrapper


class _ConverterBase:
    """ Base converter class on python side exposing the convert functionality
    """  
    
    def __create_java_converter(self, readerWrapper, writerWrapper):
        """ create java converter based on reader and writer wrapper provided in derived class implementation 
        :param readerWrapper: to use
        :param writerWrapper: to use
        :return created java converter
        """
        raise NotImplementedError('subclasses must override __create_java_converter()') 
    
    def convert(self, reader, writer ):
        """ each converter should be able to convert from a reader to a writer
        :param readerWrapper: to use
        :param writerWrapper: to use
        """
                
        # construct java converter and perform conversion
        __create_java_converter(reader, writer).convert()
        

class _NetworkConverter(_ConverterBase):
    """ Expose the options to create network reader and writers of supported types and perform conversion between them
    """
    
    def __init__(self):
        super().__init__()   
        
    def __create_java_converter(self, readerWrapper, writerWrapper):
        """ create java network converter with reader and writer wrapper provided
        :param readerWrapper: to use
        :param writerWrapper: to use
        :return created java network converter
        """
        return GatewayState.python_2_java_gateway.jvm.org.planit.converter.network.NetworkConverterFactory.create(readerWrapper.java, writerWrapper.java)
    
    #####################################
    #     READER FACTORY METHODS
    #####################################
   
        
    def __create_osm_network_reader(self, country: str):
        java_network_reader = GatewayState.python_2_java_gateway.jvm.org.planit.osm.converter.reader.PlanitOsmNetworkReaderFactory.create(country)
        return OsmNetworkReaderWrapper(java_network_reader)
    
    def __create_planit_network_reader(self):
        #TODO
        return None
        
    #####################################
    #     WRITER FACTORY METHODS
    #####################################
        
    def __create_matsim_network_writer(self):
        java_network_reader = GatewayState.python_2_java_gateway.jvm.org.planit.matsim.converter.PlanitMatsimNetworkWriterFactory.create()
        return OsmNetworkReaderWrapper(java_network_reader)
        
    def __create_planit_network_writer(self):
        #TODO
        return None
    
        
    def create_reader(self, network_reader_type: NetworkReaderType, country="Global") -> NetworkReaderWrapper:
        """ factory method to create a network reader compatible with this converter
        :param network_reader_type: the type of reader to create
        :param country: optional argument specifying the country of the source network. Used by some readers to initialise default settings. If absent
         it defaults to "Global", i.e., no country specific information is used in initialising defaults if applicable
        """
        if  network_reader_type == NetworkReaderType.OSM:
            # OSM requires country to initialise default settings
            return self.__create_osm_network_reader(country)
        elif network_reader_type == NetworkReaderType.PLANIT:
            # PLANit does not utilise country information
            return self.__create_planit_network_reader() 
        else:
            raise Exception("unsupported network reader type provided, unable to instantiate")
    
    def create_writer(self, network_writer_type: NetworkWriterType) -> NetworkWriterWrapper:
        """ factory method to create a network writer compatible with this converter
        :param network_writer_type: the type of writer to create
        """
        if  network_writer_type == NetworkWriterType.MATSIM:
            return self.__create_matsim_network_writer()
        elif network_writer_type == NetworkWriterType.PLANIT:
            self.__create_planit_network_writer() 
        else:
            raise Exception("unsupported network reader type provided, unable to instantiate")    
        
class _ZoningConverter(_ConverterBase):
    """ Expose the options to create zoning reader and writers of supported types and perform conversion between them
    """
    
    def __init__(self):
        super().__init__()
        
class _IntermodalConverter(_ConverterBase):
    """ Expose the options to create inetermodal reader and writers of supported types and perform conversion between them
    """
        
    def __init__(self):
        super().__init__()
        
class _ConverterFactory:
    """ Access point for all things related to converting planit inputs via the planit predefined way of performing conversions (using a compatible reader and writer and providing
    them to the apropriate converter. For example one can convert an Open Street Map network to a Planit network using this functionality
    """
    
    def __init__(self):
        """ initialise the converter, requires gateway to be up and running, if not throw exception
        """
    
    def __create_network_converter(self) -> _NetworkConverter:
        """ Factory method to create a network converter proxy that allows the user to create readers and writers and exposes a convert method
        that performs the actual conversion 
        """
        return _NetworkConverter()
    
    def __create_zoning_converter(self) -> _ZoningConverter:
        """ Factory method to create a zoning converter proxy that allows the user to create readers and writers and exposes a convert method
        that performs the actual conversion 
        """
        return _ZoningConverter()
    
    def __create_intermodal_converter(self) -> _IntermodalConverter:
        """ Factory method to create an intermodal converter proxy that allows the user to create readers and writers and exposes a convert method
        that performs the actual conversion 
        """
        return _IntermodalConverter()
        
    def create(self, converter_type: ConverterType) -> _ConverterBase:        
        """ factory method to create a converter of a given type
        :param converter_type: the convert type to create
        :param reader: to use in the converter
        :param writer: to use in the converter 
        """
        if not GatewayState.gateway_is_running:
            raise Exception('A ConverterFactory can only be used when connection to JVM present, it appears not to be')
        
        if converter_type == ConverterType.NETWORK:
            return self.__create_network_converter()
        elif converter_type == ConverterType.ZONING:
            return self.__create_zoning_converter()
        elif converter_type == ConverterType.INTERMODAL:
            return self.__create_intermodal_converter()
        else :
             raise Exception("Invalid converter type {} provided, no converter could be created".format(converter_type))
     
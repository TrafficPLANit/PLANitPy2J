
class ConverterBase:
    """ Base converter class on python side exposing the convert functionality
    """
    
    #TODO

class _ConverterFactory:
    """ Access point for all things related to converting planit inputs via the planit predefined way of performing conversions (using a compatible reader and writer and providing
    them to the apropriate converter. For example one can convert an Open Street Map network to a Planit network using this functionality
    """
    
    def __init__(self):
        """ initialise the converter, requires gateway to be up and running, if not throw exception
        """
        if not GatewayState.gateway_is_running:
            raise Exception('A ConverterFactory can only be used when instantiated from a PLANit instance, no connection to JVM present in standalone fashion')
    
    def __create_network_converter(self, reader: NetworkReaderWrapper, writer: NetworkWriterWrapper) -> NetworkConverterWrapper:
        """ Factory method to create a network converter proxy that allows the user to create readers and writers and exposes a convert method
        that performs the actual conversion
        :param reader: to use
        :param writer: to use 
        """
        return NetworkConverterWrapper()
    
    def __create_zoning_converter(self, reader, writer) -> ZoningConverterWrapper:
       #TODO
       return None
    
    def __create_intermodal_converter(self, reader, writer) -> IntermodalConverterWrapper:
        #TODO
       return None
    
    def __invalid_converter(self):
        """ default case called when no mapping to converter could be found
        """
        raise Exception('Invalid converter type provided, no converter could be created')
    
    def create(self, converter_type=ConverterType) -> ConverterWrapper:
        """ factory method to create a converter of a given type
        :param converter_type: the convert type to create
        :param reader: to use in the converter
        :param writer: to use in the converter 
        """
        switcher = {
            ConverterType.NETWORK: self.__create_network_converter(),
            ConverterType.ZONING: self.__create_zoning_converter(),
            ConverterType.INTERMODAL: self.__create_intermodal_converter() 
        }
        func = switcher.get(converter_type, self.__invalid_converter())
        
        # create the converter wrapper which in turn (based on its type) acts as a factory for creating appropriate readers and writers
        return func()

class NetworkConverter(ConverterBase):
    """ Expose the options to create network reader and writers of supported types
    """
    #TODO do the same for zoning and intermodal wrappers
    
    #####################################
    #     READER FACTORY METHODS
    #####################################
    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)       
        
    def __create_osm_network_reader(self, country: string):
        java_network_reader = GatewayState.python_2_java_gateway.jvm.org.planit.osm.converter.reader.PlanitOsmNetworkReaderFactory.create(country)
        return OsmNetworkReaderWrapper(java_network_reader)
    
    def __create_planit_network_reader(self):
        #TODO
        return None
    
    def __invalid_network_reader(self):
        raise Exception("unsupported network reader type provided, unable to instantiate")
    
    #####################################
    #     WRITER FACTORY METHODS
    #####################################
        
    def __create_matsim_network_writer(self):
        #TODO
        return None
        
    def __create_planit_network_writer(self):
        #TODO
        return None
    
    def __invalid_network_writer(self):
        raise Exception("unsupported network reader type provided, unable to instantiate")
        
        
    def createReader(self, network_reader_type: NetworkReaderType, country="Global") -> NetworkReaderWrapper:
        """ factory method to create a network reader compatible with this converter
        :param network_reader_type: the type of reader to create
        :param country: optional argument specifying the country of the source network. Used by some readers to initialise default settings. If absent
         it defaults to GLOBAL, i.e., no country specific information is used in initialising defaults if applicable
        """
        switcher = {
            # OSM requires country to initialise default settings
            NetworkReaderType.OSM: self.__create_osm_network_reader(country),
            # PLANit does not utilise country information
            NetworkReaderType.PLANIT: self.__create_planit_network_reader(), 
        }
        func = switcher.get(converter_type, self.__invalid_network_reader())
        return func()
    
    def createWriter(self, network_reader_type: NetworkWriterType) -> NetworkWriterWrapper:
        """ factory method to create a network writer compatible with this converter
        :param network_writer_type: the type of writer to create
        """
        switcher = {
            NetworkWriterType.MATSIM: self.__create_matsim_network_writer(),
            NetworkWriterType.PLANIT: self.__create_planit_network_writer(), 
        }
        func = switcher.get(converter_type, self.__invalid_network_writer())
        return func()      
from abc import abstractmethod
from ctypes import Union

from planit import ConverterType, TntpNetworkReaderWrapper, GatewayUtils, ZoningReaderType, ZoningReaderWrapper, \
    PlanitZoningReaderWrapper, TntpZoningReaderWrapper, ZoningWriterType, ZoningWriterWrapper, \
    PlanitZoningWriterWrapper, DemandsReaderType, DemandsWriterType, PlanitDemandsReaderWrapper, \
    TntpDemandsReaderWrapper, PlanitDemandsWriterWrapper, DemandsReaderWrapper, DemandsWriterWrapper, \
    NetworkReaderWrapper, GeometryZoningWriterWrapper, GeometryNetworkWriterWrapper
from planit import GatewayState
from planit import IntermodalConverterWrapper
from planit import IntermodalReaderType
from planit import IntermodalReaderWrapper
from planit import IntermodalWriterType
from planit import IntermodalWriterWrapper
from planit import MatsimIntermodalWriterWrapper
from planit import MatsimNetworkWriterWrapper
from planit import NetworkReaderType
from planit import ZoningReaderWrapper
from planit import NetworkWriterType
from planit import NetworkWriterWrapper
from planit import OsmIntermodalReaderWrapper
from planit import GtfsIntermodalReaderWrapper
from planit import OsmNetworkReaderWrapper
from planit import PlanitIntermodalReaderWrapper
from planit import PlanitIntermodalWriterWrapper
from planit import PlanitNetworkReaderWrapper
from planit import PlanitNetworkWriterWrapper
from planit import GeometryIntermodalWriterWrapper


class _ConverterBase():
    """ Base converter class on python side exposing the convert functionality
    """

    @abstractmethod
    def _create_java_converter(self, readerWrapper, writerWrapper):
        """ create java converter based on reader and writer wrapper provided in derived class implementation 
        :param readerWrapper: to use
        :param writerWrapper: to use
        :return created java converter
        """
        pass

    def convert(self, reader_wrapper, writer_wrapper):
        """ Each converter should be able to convert from a reader to a writer
        :param reader_wrapper: to use
        :param writer_wrapper: to use
        """

        # construct java converter and perform conversion
        self._create_java_converter(reader_wrapper, writer_wrapper).convert()


class NetworkConverter(_ConverterBase):
    """ Expose the options to create network reader and writers of supported types and perform conversion between them
    """

    def __init__(self):
        super().__init__()

    def _create_java_converter(self, reader_wrapper, writer_wrapper):
        """ create java network converter with reader and writer wrapper provided
        :param reader_wrapper: to use
        :param writer_wrapper: to use
        :return created java network converter
        """
        return GatewayUtils.get_package_jvm().org.goplanit.converter.network.NetworkConverterFactory.create(
            reader_wrapper.java, writer_wrapper.java)

    #####################################
    #     NETWORK READER FACTORY METHODS
    #####################################

    def __create_osm_network_reader(self, country: str) -> OsmNetworkReaderWrapper:
        java_network_reader = \
            GatewayUtils.get_package_jvm().org.goplanit.osm.converter.network.OsmNetworkReaderFactory.create(country)
        return OsmNetworkReaderWrapper(java_network_reader)

    def __create_planit_network_reader(self) -> PlanitNetworkReaderWrapper:
        java_network_reader = \
            GatewayUtils.get_package_jvm().org.goplanit.io.converter.network.PlanitNetworkReaderFactory.create()
        return PlanitNetworkReaderWrapper(java_network_reader)

    def __create_tntp_network_reader(self) -> TntpNetworkReaderWrapper:
        java_network_reader = \
            GatewayUtils.get_package_jvm().org.goplanit.tntp.converter.network.TntpNetworkReaderFactory.create()
        return TntpNetworkReaderWrapper(java_network_reader)

    #####################################
    #     NETWORK WRITER FACTORY METHODS
    #####################################

    def __create_matsim_network_writer(self) -> MatsimNetworkWriterWrapper:
        java_network_writer = \
            GatewayUtils.get_package_jvm().org.goplanit.matsim.converter.MatsimNetworkWriterFactory.create()
        return MatsimNetworkWriterWrapper(java_network_writer)

    def __create_geoio_network_writer(self) -> GeometryNetworkWriterWrapper:
        java_network_writer = \
            GatewayUtils.get_package_jvm().org.goplanit.geoio.converter.network.GeometryNetworkWriterFactory.create()
        return GeometryNetworkWriterWrapper(java_network_writer)

    def __create_planit_network_writer(self) -> PlanitNetworkWriterWrapper:
        java_network_writer = \
            GatewayUtils.get_package_jvm().org.goplanit.io.converter.network.PlanitNetworkWriterFactory.create()
        return PlanitNetworkWriterWrapper(java_network_writer)

    def create_reader(self, network_reader_type: NetworkReaderType, country: str = "Global") -> ZoningReaderWrapper:
        """ factory method to create a network reader compatible with this converter :param network_reader_type: the
        type of reader to create :param country: optional argument specifying the country of the source network. Used
        by some readers to initialise default settings. If absent but required it defaults to "Global", i.e.,
        no country specific information is used in initialising defaults if applicable
        """
        if not isinstance(network_reader_type, NetworkReaderType): raise Exception(
            "Network reader type provided is not of NetworkReaderType, unable to instantiate")

        if network_reader_type == NetworkReaderType.OSM:
            # OSM requires country to initialise default settings
            return self.__create_osm_network_reader(country)
        elif network_reader_type == NetworkReaderType.PLANIT:
            # PLANit does not utilise country information
            return self.__create_planit_network_reader()
        elif network_reader_type == NetworkReaderType.TNTP:
            # TNTP does not utilise country information
            return self.__create_tntp_network_reader()
        else:
            raise Exception("Unsupported network reader type provided, unable to instantiate")

    def create_writer(self, network_writer_type: NetworkWriterType) -> NetworkWriterWrapper:
        """ factory method to create a network writer compatible with this converter
        :param network_writer_type: the type of writer to create
        :return the created writer
        """
        if not isinstance(network_writer_type, NetworkWriterType): raise Exception(
            "Network writer type provided is not of NetworkWriterType, unable to instantiate")

        if network_writer_type == NetworkWriterType.MATSIM:
            return self.__create_matsim_network_writer()
        if network_writer_type == NetworkWriterType.SHAPE:
            return self.__create_geoio_network_writer()
        elif network_writer_type == NetworkWriterType.PLANIT:
            return self.__create_planit_network_writer()
        else:
            raise Exception("Unsupported network writer type provided, unable to instantiate")


class ZoningConverter(_ConverterBase):
    """ Expose the options to create zoning reader and writers of supported types and perform conversion between them
    """

    def __init__(self):
        super().__init__()

    def _create_java_converter(self, reader_wrapper, writer_wrapper):
        """ create java network converter with reader and writer wrapper provided
        :param reader_wrapper: to reader use
        :param writer_wrapper: to writer use
        :return created java network converter
        """
        return GatewayUtils.get_package_jvm().org.goplanit.converter.zoning.ZoningConverterFactory.create(
            reader_wrapper.java, writer_wrapper.java)

    #####################################
    #     ZONING READER FACTORY METHODS
    #####################################

    @staticmethod
    def __create_planit_zoning_reader(reference_reader: ZoningReaderWrapper) -> PlanitZoningReaderWrapper:
        java_zoning_reader = \
            GatewayUtils.get_package_jvm().org.goplanit.io.converter.zoning.PlanitZoningReaderFactory.create(
                reference_reader.java)
        return PlanitZoningReaderWrapper(java_zoning_reader)

    @staticmethod
    def __create_tntp_zoning_reader(reference_reader: ZoningReaderWrapper) -> TntpZoningReaderWrapper:
        java_zoning_reader = \
            GatewayUtils.get_package_jvm().org.goplanit.tntp.converter.zoning.TntpZoningReaderFactory.create(
                reference_reader.java)
        return TntpZoningReaderWrapper(java_zoning_reader)

    #####################################
    #     ZONING WRITER FACTORY METHODS
    #####################################

    @staticmethod
    def __create_planit_zoning_writer() -> PlanitZoningWriterWrapper:
        java_zoning_writer = \
            GatewayUtils.get_package_jvm().org.goplanit.io.converter.zoning.PlanitZoningWriterFactory.create()
        return PlanitZoningWriterWrapper(java_zoning_writer)

    @staticmethod
    def __create_geoio_zoning_writer() -> GeometryZoningWriterWrapper:
        java_zoning_writer = \
            GatewayUtils.get_package_jvm().org.goplanit.geoio.converter.zoning.GeometryZoningWriterFactory.create()
        return GeometryZoningWriterWrapper(java_zoning_writer)

    def create_reader(self,
                      zoning_reader_type: ZoningReaderType,
                      reference_reader: NetworkReaderWrapper = None) -> ZoningReaderWrapper:
        """ factory method to create a zoning reader compatible with this converter.

        :param zoning_reader_type: the type of reader to create
        :param reference_reader: specifying a reference reader that is used to construct network from
        a different source than its own to be used when constructing the zoning
        :return created reader
        """
        if not isinstance(zoning_reader_type, ZoningReaderType):
            raise Exception(
                "Zoning reader type provided is not of ZoningReaderType, unable to instantiate")

        elif zoning_reader_type == ZoningReaderType.PLANIT:
            return ZoningConverter.__create_planit_zoning_reader(reference_reader)
        elif zoning_reader_type == ZoningReaderType.TNTP:
            return ZoningConverter.__create_tntp_zoning_reader(reference_reader)
        else:
            raise Exception("Unsupported zoning reader type provided, unable to instantiate")

    def create_writer(self, zoning_writer_type: ZoningWriterType) -> ZoningWriterWrapper:
        """ factory method to create a zoning reader compatible with this converter.

        :param zoning_writer_type: the type of writer to create
        :return created writer
        """
        if not isinstance(zoning_writer_type, ZoningWriterType):
            raise Exception(
                "Zoning reader type provided is not of ZoningReaderType, unable to instantiate")

        elif zoning_writer_type == ZoningWriterType.PLANIT:
            return ZoningConverter.__create_planit_zoning_writer()
        elif zoning_writer_type == ZoningWriterType.SHAPE:
            return ZoningConverter.__create_geoio_zoning_writer()
        else:
            raise Exception("Unsupported zoning writer type provided, unable to instantiate")


class DemandsConverter(_ConverterBase):
    """ Expose the options to create demand reader and writers of supported types and perform conversion between them
    """

    def __init__(self):
        super().__init__()

    def _create_java_converter(self, reader_wrapper, writer_wrapper):
        """ create java network converter with reader and writer wrapper provided
        :param reader_wrapper: reader to use
        :param writer_wrapper: writer to use
        :return created java network converter
        """
        return GatewayUtils.get_package_jvm().org.goplanit.converter.demands.DemandsConverterFactory.create(
            reader_wrapper.java, writer_wrapper.java)

    #####################################
    #     DEMANDS READER FACTORY METHODS
    #####################################

    @staticmethod
    def __create_planit_demands_reader(reference_zoning_reader: ZoningReaderWrapper) -> PlanitDemandsReaderWrapper:
        java_reader = \
            GatewayUtils.get_package_jvm().org.goplanit.io.converter.demands.PlanitDemandsReaderFactory.create(
                reference_zoning_reader.java)
        return PlanitDemandsReaderWrapper(java_reader)

    @staticmethod
    def __create_tntp_demands_reader(reference_zoning_reader: ZoningReaderWrapper) -> TntpDemandsReaderWrapper:
        java_reader = \
            GatewayUtils.get_package_jvm().org.goplanit.tntp.converter.demands.TntpDemandsReaderFactory.create(
                reference_zoning_reader.java)
        return TntpDemandsReaderWrapper(java_reader)

    #####################################
    #     DEMANDS WRITER FACTORY METHODS
    #####################################

    @staticmethod
    def __create_planit_demands_writer() -> PlanitDemandsWriterWrapper:
        java_writer = \
            GatewayUtils.get_package_jvm().org.goplanit.io.converter.demands.PlanitDemandsWriterFactory.create()
        return PlanitDemandsWriterWrapper(java_writer)

    def create_reader(self,
                      demands_reader_type: DemandsReaderType, reference_zoning_reader: ZoningReaderWrapper = None) \
            -> DemandsReaderWrapper:
        """ factory method to create a demands reader compatible with this converter

        :param demands_reader_type: the type of reader to create
        :param reference_zoning_reader: the zoning reader related to these demands
        """
        if not isinstance(demands_reader_type, DemandsReaderType): raise Exception(
            "Demands reader type provided is not of DemandsReaderType, unable to instantiate")
        elif demands_reader_type == DemandsReaderType.PLANIT:
            return DemandsConverter.__create_planit_demands_reader(reference_zoning_reader)
        elif demands_reader_type == DemandsReaderType.TNTP:
            return DemandsConverter.__create_tntp_demands_reader(reference_zoning_reader)
        else:
            raise Exception("Unsupported demands reader type provided, unable to instantiate")

    def create_writer(self, demands_writer_type: DemandsWriterType) -> DemandsWriterWrapper:
        """ factory method to create a demands writer compatible with this converter

        :param demands_writer_type: the type of writer to create
        :return the created writer
        """
        if not isinstance(demands_writer_type, DemandsWriterType): raise Exception(
            "Demands writer type provided is not of DemandsWriterType, unable to instantiate")
        elif demands_writer_type == DemandsWriterType.PLANIT:
            return DemandsConverter.__create_planit_demands_writer()
        else:
            raise Exception("Unsupported demands writer type provided, unable to instantiate")


class IntermodalConverter(_ConverterBase):
    """ Expose the options to create intermodal reader and writers of supported types and perform conversion between
    them
    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def _create_java_converter(reader_wrapper, writer_wrapper) -> IntermodalConverterWrapper:
        """ create java intermodal converter with reader and writer wrapper provided
        :param reader_wrapper: the reader to use
        :param writer_wrapper: the writer to use
        :return created java intermodal converter
        """
        return IntermodalConverterWrapper(GatewayState.python_2_java_gateway.jvm.org.goplanit.converter.intermodal.
                                          IntermodalConverterFactory.create(reader_wrapper.java, writer_wrapper.java))

    def convert_with_services(self, reader_wrapper: IntermodalReaderWrapper, writer_wrapper: IntermodalWriterWrapper):
        """ Each intermodal converter is expected to be able to convert from a reader to a writer including services
        :param reader_wrapper: the reader to use
        :param writer_wrapper: the writer to use
        """

        # construct java converter and perform conversion
        self._create_java_converter(reader_wrapper, writer_wrapper).convert_with_services()

    #####################################
    #     READER FACTORY METHODS
    #####################################

    @staticmethod
    def __create_osm_intermodal_reader(country: str) -> OsmIntermodalReaderWrapper:
        java_intermodal_reader = GatewayState.python_2_java_gateway.jvm.org.goplanit.osm.converter.intermodal. \
            OsmIntermodalReaderFactory.create(country)
        return OsmIntermodalReaderWrapper(java_intermodal_reader)

    @staticmethod
    def __create_planit_intermodal_reader() -> PlanitIntermodalReaderWrapper:
        java_intermodal_reader = GatewayState.python_2_java_gateway.jvm.org.goplanit.io.converter.intermodal. \
            PlanitIntermodalReaderFactory.create()
        return PlanitIntermodalReaderWrapper(java_intermodal_reader)

    @staticmethod
    def __create_gtfs_intermodal_reader(country: str,
                                        reference_reader: IntermodalReaderWrapper) -> PlanitIntermodalReaderWrapper:
        if not reference_reader:
            raise Exception(
                "GTFS intermodal reader expects a reference reader to be able to construct network and zoning")

        java_intermodal_reader = GatewayState.python_2_java_gateway.jvm.org.goplanit.gtfs.converter.intermodal. \
            GtfsIntermodalReaderFactory.create(country, reference_reader.java)
        return GtfsIntermodalReaderWrapper(java_intermodal_reader)

    #####################################
    #     WRITER FACTORY METHODS
    #####################################

    @staticmethod
    def __create_matsim_intermodal_writer() -> MatsimIntermodalWriterWrapper:
        java_network_writer = GatewayState.python_2_java_gateway.jvm.org.goplanit.matsim.converter. \
            MatsimIntermodalWriterFactory.create()
        return MatsimIntermodalWriterWrapper(java_network_writer)

    @staticmethod
    def __create_planit_intermodal_writer() -> PlanitIntermodalWriterWrapper:
        java_network_writer = GatewayState.python_2_java_gateway.jvm.org.goplanit.io.converter.intermodal. \
            PlanitIntermodalWriterFactory.create()
        return PlanitIntermodalWriterWrapper(java_network_writer)

    @staticmethod
    def __create_geoio_intermodal_writer() -> GeometryIntermodalWriterWrapper:
        java_network_writer = GatewayState.python_2_java_gateway.jvm.org.goplanit.geoio.converter.intermodal. \
            GeometryIntermodalWriterFactory.create()
        return GeometryIntermodalWriterWrapper(java_network_writer)

    def create_reader(self,
                      intermodal_reader_type: IntermodalReaderType,
                      country: str = "Global",
                      reference_reader: IntermodalReaderWrapper = None) -> IntermodalReaderWrapper:
        """ factory method to create an intermodal  reader compatible with this converter.

        :param intermodal_reader_type: the type of reader to create
        :param country: optional argument specifying the country of the source network.
        Used by some readers to initialise default settings. If absent it defaults to "Global", i.e., no country
        specific information is used in initialising defaults if applicable
        :param reference_reader: specifying another intermodal reader that is used to construct network and zoning from
        a different source than its own (only relevant for GTFS based reader currently)
        """

        if not isinstance(intermodal_reader_type, IntermodalReaderType): raise Exception(
            "Reader type provided is not of IntermodalReaderType, unable to instantiate")

        if intermodal_reader_type == IntermodalReaderType.OSM:
            # OSM requires country to initialise default settings
            return IntermodalConverter.__create_osm_intermodal_reader(country)
        elif intermodal_reader_type == IntermodalReaderType.PLANIT:
            return IntermodalConverter.__create_planit_intermodal_reader()
        elif intermodal_reader_type == IntermodalReaderType.GTFS:
            return IntermodalConverter.__create_gtfs_intermodal_reader(country, reference_reader)
        else:
            raise Exception(f"Unsupported intermodal reader type provided {intermodal_reader_type}, "
                            f"unable to instantiate")

    def create_writer(self, intermodal_writer_type: IntermodalWriterType) -> IntermodalWriterWrapper:
        """ factory method to create an intermodal writer compatible with this converter
        :param intermodal_writer_type: the type of writer to create
        """

        if not isinstance(intermodal_writer_type, IntermodalWriterType): raise Exception(
            "writer type provided is not of IntermodalWriterType, unable to instantiate")

        if intermodal_writer_type == IntermodalWriterType.MATSIM:
            return IntermodalConverter.__create_matsim_intermodal_writer()
        elif intermodal_writer_type == IntermodalWriterType.PLANIT:
            return IntermodalConverter.__create_planit_intermodal_writer()
        elif intermodal_writer_type == IntermodalWriterType.SHAPE:
            return IntermodalConverter.__create_geoio_intermodal_writer()
        else:
            raise Exception("Unsupported intermodal writer type provided, unable to instantiate")


class ConverterFactory:
    """ Access point for all things related to converting PLANit inputs via the PLANit predefined way of performing
    conversions (using a compatible reader and writer and providing them to the appropriate converter). For example
    one can convert an Open Street Map network to a PLANit network using this functionality.
    """

    def __init__(self):
        """ initialise the converter, requires gateway to be up and running, if not throw exception
        """

    @staticmethod
    def __create_network_converter() -> NetworkConverter:
        """ Factory method to create a network converter proxy that allows the user to create readers and writers and
        exposes a convert method that performs the actual conversion
        """
        return NetworkConverter()

    @staticmethod
    def __create_zoning_converter() -> ZoningConverter:
        """ Factory method to create a zoning converter proxy that allows the user to create readers and writers and
        exposes a convert method that performs the actual conversion
        """
        return ZoningConverter()

    @staticmethod
    def __create_intermodal_converter() -> IntermodalConverter:
        """ Factory method to create an intermodal converter proxy that allows the user to create readers and writers
        and exposes a convert method that performs the actual conversion
        """
        return IntermodalConverter()

    @staticmethod
    def __create_demands_converter() -> IntermodalConverter:
        """ Factory method to create a demands converter proxy that allows the user to create readers and writers
        and exposes a convert method that performs the actual conversion
        """
        return DemandsConverter()

    def create(self, converter_type: ConverterType) -> _ConverterBase:
        """ factory method to create a converter of a given type
        :param converter_type: the convert type to create
        :param reader: to use in the converter
        :param writer: to use in the converter

        :return a network, zoning, or intermodal converter
        """
        if not GatewayState.gateway_is_running: raise Exception('A ConverterFactory can only be used when connection '
                                                                'to JVM present, connection not available')

        if not isinstance(converter_type, ConverterType): raise Exception("Converter type provided is not of "
                                                                          "ConverterType, unable to instantiate")

        if converter_type == ConverterType.NETWORK:
            return self.__create_network_converter()
        elif converter_type == ConverterType.ZONING:
            return self.__create_zoning_converter()
        elif converter_type == ConverterType.DEMANDS:
            return self.__create_demands_converter()
        elif converter_type == ConverterType.INTERMODAL:
            return self.__create_intermodal_converter()
        else:
            raise Exception(f"Invalid converter type {converter_type} provided, no converter could be created")

import datetime
from typing import Tuple, List, Set, Union, Any, Dict

from py4j import java_collections

from planit import DayOfWeek, IdMapperType, GatewayUtils, TntpFileColumnType, SpeedUnits, TimeUnits, LengthUnits
from planit import GatewayState
from planit import BaseWrapper


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

        # wrap the java settings that we expose as a property for this reader in a "ReaderSettingsWrapper" this way
        # we have a general wrapper for all settings instances exposed to the user, while not having to create
        # separate wrapper classes for each specific implementation (as long as the settings themselves do not expose
        # any other classes that need to be wrapper this will work
        self._settings = ReaderSettingsWrapper(java_counterpart.getSettings())

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
        # wrap the java settings that we expose as a property for this writer in a "WriterSettingsWrapper" this way
        # we have a general wrapper for all settings instances exposed to the user, while not having to create
        # separate wrapper classes for each specific implementation (as long as the settings themselves do not expose
        # any other classes that need to be wrapper this will work
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
    """ Wrapper around the Java IntermodalReader class instance, derived implementation are more specific,
    e.g. OsmIntermodalReaderWrapper
    """

    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)


class IntermodalWriterWrapper(WriterWrapper):
    """ Wrapper around the Java IntermodalWriter class instance, derived implementations are more specific,
    e.g. MatsimIntermodalWriterWrapper
    """

    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)

    def set_id_mapper_type(self, id_mapper_type: IdMapperType):
        self.setIdMapperType(GatewayUtils.to_java_enum(id_mapper_type))

    def get_id_mapper_type(self) -> IdMapperType:
        return IdMapperType.from_java(self.getIdMapperType())


class NetworkConverterWrapper(ConverterWrapper):
    """ Wrapper around the Java NetworkConverter class instance
    """

    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)

class NetworkReaderWrapper(ReaderWrapper):
    """ Wrapper around the Java NetworkReader class instance, derived implementations are more specific,
    e.g. PlanitNetworkReaderWrapper
    """

    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)


class NetworkWriterWrapper(WriterWrapper):
    """ Wrapper around the Java NetworkWriter class instance, derived implementations are more specific,
    e.g. MatsimNetworkWriterWrapper
    """

    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)


class ZoningConverterWrapper(ConverterWrapper):
    """ Wrapper around the Java ZoningConverter class instance
    """

    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)


class ZoningReaderWrapper(ReaderWrapper):
    """ Wrapper around the Java NetworkReader class instance, derived implementation are more specific,
    e.g. PlanitZoningReaderWrapper
    """

    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)


class ZoningWriterWrapper(WriterWrapper):
    """ Wrapper around the Java ZoningWriter class instance, derived implementations are more specific,
    e.g. TntpZoningWriterWrapper
    """

    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)


class DemandsReaderWrapper(ReaderWrapper):
    """ Wrapper around the Java DemandsReader class instance, derived implementation are more specific,
    e.g. TntpDemandsReaderWrapper
    """

    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)


class DemandsWriterWrapper(WriterWrapper):
    """ Wrapper around the Java DemandsWriter class instance, derived implementations are more specific,
    e.g. PlanitDemandsWriterWrapper
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
        self._pt_services_settings = WriterSettingsWrapper(self.get_pt_services_settings())

    @property
    def network_settings(self):
        return self._network_settings

    @property
    def zoning_settings(self):
        return self._zoning_settings

    @property
    def pt_services_settings(self):
        return self._pt_services_settings


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


class OsmIntermodalReaderWrapper(IntermodalReaderWrapper):
    """ Wrapper around the Java OsmIntermodalReader class, its settings made from settings files only
    """

    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)


class OsmNetworkReaderWrapper(ZoningReaderWrapper):
    """ Wrapper around the Java OsmNetworkReader class, its settings made from settings files only
    """

    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)


class GtfsIntermodalReaderWrapper(IntermodalReaderWrapper):
    """ Wrapper around the Java GtfsIntermodalReader class
    """

    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)

        # replace regular reader settings by Gtfs intermodal reader settings
        self._settings = GtfsIntermodalReaderSettingsWrapper(self._settings.java)


class GtfsServicesReaderSettingsWrapper(ReaderSettingsWrapper):
    """ Wrapper around settings for GTFS services used by converter
    """

    @staticmethod
    def __create_java_day_of_week(day_of_week: DayOfWeek):
        """ convert Python day of week enum to Java day of week enum.

        :param day_of_week: type to convert
        :return java counterpart
        """
        return GatewayState.python_2_java_gateway.entry_point.createEnum(
            day_of_week.java_class_name(), day_of_week.value)

    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)

    @property
    def day_of_week(self):
        return DayOfWeek.from_java(self.java.getDayOfWeek())

    @day_of_week.setter
    def day_of_week(self, value: DayOfWeek):
        self.java.setDayOfWeek(GtfsServicesReaderSettingsWrapper.__create_java_day_of_week(value))

    def get_time_period_filters(self):
        filters: java_collections.Set = self.java.getTimePeriodFilters()
        if not filters:
            return None
        python_filters: Set[Tuple[datetime.time(), datetime.time()]] = set()
        for entry in filters:
            # entry contains PLANit Pair of two Java LocalTime instances
            start_time: datetime.time = GatewayUtils.to_python_datetime_time(entry.first());
            end_time: datetime.time = GatewayUtils.to_python_datetime_time(entry.second());
            python_filters.add((start_time, end_time))
        return python_filters


class GtfsZoningReaderSettingsWrapper(ReaderSettingsWrapper):
    """ Wrapper around settings for GTFS zoning used by converter
    """

    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)

    def add_overwrite_gtfs_stop_transfer_zone_mapping(
            self, gtfs_stop_id: str, transfer_zone_id: Union[int, str], id_mapper_type: IdMapperType):
        self.java.addOverwriteGtfsStopTransferZoneMapping(
            gtfs_stop_id, transfer_zone_id, GatewayUtils.to_java_enum(id_mapper_type))

    def get_overwritten_gtfs_stop_transfer_zone_mapping(self, gtfs_stop_id: str) -> List[
        Tuple[Union[int, str], IdMapperType]]:
        java_collection: java_collections.JavaList = self.java.getOverwrittenGtfsStopTransferZoneMapping(gtfs_stop_id)
        python_list = []
        for entry in java_collection:
            # entry contains Java Planit Pair<object,IdMapperType>
            transfer_zone_id: Union[int, str] = entry.first()
            python_list.append((transfer_zone_id, IdMapperType.from_java(entry.second())))
        return python_list

    def get_overwritten_gtfs_stop_location(self, gtfs_stop_id: str) -> Tuple[float, float]:
        """ collect the overwritten stop location.

        :param gtfs_stop_id: stop id
        :return coordinate tuple (lat/lon or equivalent projected coord)
        """
        java_coord = self.java.getOverwrittenGtfsStopLocation(gtfs_stop_id)  # jts coord
        return java_coord.getY(), java_coord.getX()  # lat=Y,lon=X

    def overwrite_gtfs_stop_to_link_mapping(
            self, gtfs_stop_id: str, planit_link_id: Union[int, str], id_mapper_type: IdMapperType):
        self.java.overwriteGtfsStopToLinkMapping(
            gtfs_stop_id, planit_link_id, GatewayUtils.to_java_enum(id_mapper_type))

    def get_overwritten_gtfs_stop_to_link_mapping(self, gtfs_stop_id: str) -> Tuple[Union[int, str], IdMapperType]:
        java_planit_pair = self.java.getOverwrittenGtfsStopToLinkMapping(gtfs_stop_id)
        planit_link_id: Union[int, str] = java_planit_pair.first()
        id_mapper_type: IdMapperType = IdMapperType.from_java(java_planit_pair.second())
        return planit_link_id, id_mapper_type


class GtfsIntermodalReaderSettingsWrapper(ReaderSettingsWrapper):
    """ Wrapper around settings for a Gtfs intermodal reader used by converter
    """

    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)

        # Gtfs intermodal reader settings allow access to network and pt settings component
        # which in turns are settings
        self._services_settings = GtfsServicesReaderSettingsWrapper(self.getServiceSettings())
        self._zoning_settings = GtfsZoningReaderSettingsWrapper(self.getZoningSettings())

    @property
    def services_settings(self) -> GtfsServicesReaderSettingsWrapper:
        return self._services_settings

    @property
    def zoning_settings(self) -> GtfsZoningReaderSettingsWrapper:
        return self._zoning_settings


class PlanitIntermodalReaderSettingsWrapper(ReaderSettingsWrapper):
    """ Wrapper around settings for a PLANit intermodal reader (native format) used by converter
    """

    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)

        # PLANit intermodal reader settings allow access to network and zoning settings component
        # which in turns are settings 
        self._network_settings = ReaderSettingsWrapper(self.getNetworkSettings())
        self._zoning_settings = ReaderSettingsWrapper(self.getZoningSettings())
        self._service_network_settings = ReaderSettingsWrapper(self.getServiceNetworkSettings())
        self._routed_services_settings = ReaderSettingsWrapper(self.getRoutedServicesSettings())

    @property
    def network_settings(self):
        return self._network_settings

    @property
    def zoning_settings(self):
        return self._zoning_settings

    @property
    def service_network_settings(self):
        return self._service_network_settings

    @property
    def routed_services_settings(self):
        return self._routed_services_settings


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
        self._service_network_settings = WriterSettingsWrapper(self.get_service_network_settings())
        self._routed_services_settings = WriterSettingsWrapper(self.get_routed_services_settings())

    @property
    def network_settings(self):
        return self._network_settings

    @property
    def zoning_settings(self):
        return self._zoning_settings

    @property
    def service_network_settings(self):
        return self._service_network_settings

    @property
    def routed_services_settings(self):
        return self._routed_services_settings


class PlanitIntermodalWriterWrapper(IntermodalWriterWrapper):
    """ Wrapper around the Java native format based PlanitIntermodalWriter class
    """

    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)

        # replace regular writer settings by PLANit intermodal reader settings
        self._settings = PlanitIntermodalWriterSettingsWrapper(self._settings.java)


class PlanitNetworkReaderWrapper(ZoningReaderWrapper):
    """ Wrapper around the Java native format based PlanitNetworkReader class
    """

    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)


class PlanitNetworkWriterWrapper(NetworkWriterWrapper):
    """ Wrapper around the Java native format based PlanitNetworkWriter class.
    """

    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)


class PlanitZoningWriterWrapper(ZoningWriterWrapper):
    """ Wrapper around the Java native format based PlanitZoningWriter class.
    """

    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)


class PlanitZoningReaderWrapper(ZoningReaderWrapper):
    """ Wrapper around the Java native format based PlanitNetworkReader class
    """

    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)


class PlanitDemandsReaderWrapper(DemandsReaderWrapper):
    """ Wrapper around the Java native format based PlanitDemandsReader class
    """

    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)


class PlanitDemandsWriterWrapper(DemandsWriterWrapper):
    """ Wrapper around the Java native format based PlanitDemandsWriter class
    """

    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)


class TntpNetworkReaderSettingsWrapper(ReaderSettingsWrapper):
    """ Wrapper around settings for a TNTP network reader used by converter.
    """

    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)

    def set_network_file_columns(self, network_file_columns: Dict[TntpFileColumnType, int]):
        java_hash_map = GatewayUtils.get_package_jvm().java.util.HashMap()
        for column_type, column_index in network_file_columns.items():
            java_hash_map[GatewayUtils.to_java_enum(column_type)] = column_index
        self.java.setNetworkFileColumns(java_hash_map)

    def set_speed_units(self, speed_units: SpeedUnits):
        self.java.setSpeedUnits(GatewayUtils.to_java_enum(speed_units))

    def get_speed_units(self) -> SpeedUnits:
        return SpeedUnits.from_java(self.java.getSpeedUnits())

    def set_time_units(self, time_units: TimeUnits):
        self.java.setTimeUnits(GatewayUtils.to_java_enum(time_units))

    def get_time_units(self) -> TimeUnits:
        return TimeUnits.from_java(self.java.getTimeUnits())

    def set_length_units(self, length_units: LengthUnits):
        self.java.setLengthUnits(GatewayUtils.to_java_enum(length_units))

    def get_length_units(self) -> LengthUnits:
        return LengthUnits.from_java(self.java.getLengthUnits())

    def set_capacity_period(self, duration: float, time_units: TimeUnits):
        self.java.setCapacityPeriod(duration, GatewayUtils.to_java_enum(time_units))

    def get_capacity_period_units(self) -> TimeUnits:
        return TimeUnits.from_java(self.java.getCapacityPeriodUnits())

    def get_capacity_period_duration(self) -> float:
        return self.java.getCapacityPeriodDuration()

    def set_free_flow_travel_time_units(self, time_units: TimeUnits):
        self.java.setFreeFlowTravelTimeUnits(GatewayUtils.to_java_enum(time_units))


class TntpNetworkReaderWrapper(ZoningReaderWrapper):
    """ Wrapper around the Java native format based TntpNetworkReader class.
    """

    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)

        # replace regular writer settings by Tntp network reader settings
        self._settings = TntpNetworkReaderSettingsWrapper(self._settings.java)


class TntpZoningReaderWrapper(ZoningReaderWrapper):
    """ Wrapper around the Java native format based TntpZoningReader class.
    """

    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)


class TntpDemandsReaderSettingsWrapper(ReaderSettingsWrapper):
    """ Wrapper around settings for a TNTP demands reader used by converter.
    """

    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)

    def set_start_time_since_midnight(self, start_time: Union[float, int], time_units: TimeUnits):
        self.java.setStartTimeSinceMidnight(start_time, GatewayUtils.to_java_enum(time_units))

    def set_time_period_duration(self, duration: Union[float, int], time_units: TimeUnits):
        self.java.setTimePeriodDuration(duration, GatewayUtils.to_java_enum(time_units))


class TntpDemandsReaderWrapper(DemandsReaderWrapper):
    """ Wrapper around the Java native format based TntpDemandsReader class
    """

    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)

        # replace regular writer settings by Geometry intermodal writer settings
        self._settings = TntpDemandsReaderSettingsWrapper(self._settings.java)


class GeometryNetworkWriterWrapper(NetworkWriterWrapper):
    """ Wrapper around the Java native format based GeometryNetworkWriter class.
    """

    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)

class GeometryZoningWriterWrapper(ZoningWriterWrapper):
    """ Wrapper around the Shape file format based GeometryZoningWriter class.
    """

    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)


class GeometryIntermodalWriterWrapper(IntermodalWriterWrapper):
    """ Wrapper around the Geometry (GIS) based formats for persisting.
    """

    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)

        # replace regular writer settings by Geometry intermodal writer settings
        self._settings = GeometryIntermodalWriterSettingsWrapper(self._settings.java)


class GeometryIntermodalWriterSettingsWrapper(WriterSettingsWrapper):
    """ Wrapper around settings for an intermodal geometry writer used by converter
    """

    def __init__(self, java_counterpart):
        super().__init__(java_counterpart)

        # geometry intermodal writer settings allow access to network, zoning, service network and routed services
        # settings components which in turns are settings
        self._network_settings = WriterSettingsWrapper(self.get_network_settings())
        self._zoning_settings = WriterSettingsWrapper(self.get_zoning_settings())
        self._service_network_settings = WriterSettingsWrapper(self.get_service_network_settings())
        self._routed_services_settings = WriterSettingsWrapper(self.get_routed_services_settings())

    @property
    def network_settings(self):
        return self._network_settings

    @property
    def zoning_settings(self):
        return self._zoning_settings

    @property
    def service_network_settings(self):
        return self._service_network_settings

    @property
    def routed_services_settings(self):
        return self._routed_services_settings

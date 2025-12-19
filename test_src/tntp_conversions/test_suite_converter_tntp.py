import os
import sys
from pathlib import Path

from planit.converter import DemandsConverter

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../..', 'src'))

ABSOLUTE_PATH = os.path.dirname(__file__)
ABSOLUTE_PATH_TEST_DATA = os.path.join(ABSOLUTE_PATH, '..', '..', 'testdata')
ABSOLUTE_PATH_TEST_DATA_CONVERTER = os.path.join(ABSOLUTE_PATH_TEST_DATA, 'converter')

import gc
import unittest
from planit import *

AUSTRALIA = "Australia"


TNTP_PATH = os.path.join(ABSOLUTE_PATH_TEST_DATA_CONVERTER, 'tntp')
TNTP_INPUT_PATH = os.path.join(TNTP_PATH, 'input')


def create_tntp_network_file_cols() -> Dict[TntpFileColumnType, int]:
    return {
        TntpFileColumnType.UPSTREAM_NODE_ID: 0,
        TntpFileColumnType.DOWNSTREAM_NODE_ID: 1,
        TntpFileColumnType.CAPACITY_PER_LANE: 2,
        TntpFileColumnType.LENGTH: 3,
        TntpFileColumnType.FREE_FLOW_TRAVEL_TIME: 4,
        TntpFileColumnType.B: 5,
        TntpFileColumnType.POWER: 6,
        TntpFileColumnType.MAXIMUM_SPEED: 7,
        TntpFileColumnType.TOLL: 8,
        TntpFileColumnType.LINK_TYPE: 9}


class TestSuiteConverterTntp(unittest.TestCase):
    """ We are testing here if planit_conversions are runnable. We do not actually test the validity of the results
        as this is being done on the Java side. Here, we just make sure the properties can be set as expected and
        the run does not yield any errors/exceptions
    """

    def test_network_converter_tntp2planit(self):
        OUTPUT_PATH = os.path.join(TNTP_PATH, 'output', 'planit')
        DEFAULT_MAXIMUM_SPEED_KM_H = 25.0;

        NETWORK_FILE_PATH = (Path(TNTP_INPUT_PATH) / "SiouxFalls" / "SiouxFalls_net.tntp").as_posix()
        NODE_COORD_FILE_PATH = (Path(TNTP_INPUT_PATH) / "SiouxFalls" / "SiouxFalls_node.tntp").as_posix()

        # no correspondence to Java test as we explicitly test non-failure of Python code to instantiate converters
        planit = Planit()

        # network converter
        network_converter: NetworkConverter = planit.converter_factory.create(ConverterType.NETWORK)

        # TNTP reader
        tntp_reader: TntpNetworkReaderWrapper = network_converter.create_reader(NetworkReaderType.TNTP)

        network_settings: TntpNetworkReaderSettingsWrapper = tntp_reader.settings
        network_settings.set_network_file(NETWORK_FILE_PATH)
        network_settings.set_node_coordinate_file(NODE_COORD_FILE_PATH)

        network_settings.set_network_file_columns(create_tntp_network_file_cols())

        network_settings.set_speed_units(SpeedUnits.MILES_H)
        network_settings.set_length_units(LengthUnits.MILES)
        network_settings.set_capacity_period(1, TimeUnits.HOURS)
        network_settings.set_free_flow_travel_time_units(TimeUnits.MINUTES)
        network_settings.set_default_maximum_speed(DEFAULT_MAXIMUM_SPEED_KM_H)

        # PLANit writer
        planit_writer = network_converter.create_writer(NetworkWriterType.PLANIT)
        planit_writer.settings.set_output_directory(OUTPUT_PATH)
        planit_writer.settings.set_country(AUSTRALIA)

        # perform conversion
        network_converter.convert(tntp_reader, planit_writer)

        planit.force_stop_java()
        gc.collect()

    def test_network_zoning_demands_converter_tntp2planit(self):
        OUTPUT_PATH = os.path.join(TNTP_PATH, 'output', 'planit')
        DEFAULT_MAXIMUM_SPEED_KM_H = 25.0;

        NETWORK_FILE_PATH = (Path(TNTP_INPUT_PATH) / "Chicago" / "ChicagoSketch_net.tntp").as_posix()
        NODE_COORD_FILE_PATH = (Path(TNTP_INPUT_PATH) / "Chicago" / "ChicagoSketch_node.tntp").as_posix()
        DEMAND_FILE_PATH = (Path(TNTP_INPUT_PATH) / "Chicago" / "ChicagoSketch_trips.tntp").as_posix()

        # no correspondence to Java test as we explicitly test non-failure of Python code to instantiate converters
        planit = Planit()

        # demands converter
        demand_converter: DemandsConverter = planit.converter_factory.create(ConverterType.DEMANDS)

        # TNTP net reader - prep
        tntp_net_reader: TntpNetworkReaderWrapper = planit.converter_factory.create(ConverterType.NETWORK) \
            .create_reader(NetworkReaderType.TNTP)
        network_settings: TntpNetworkReaderSettingsWrapper = tntp_net_reader.settings

        network_settings.set_network_file(NETWORK_FILE_PATH)
        network_settings.set_node_coordinate_file(NODE_COORD_FILE_PATH)

        network_settings.set_network_file_columns(create_tntp_network_file_cols())

        network_settings.set_speed_units(SpeedUnits.MILES_H)
        network_settings.set_length_units(LengthUnits.MILES)
        network_settings.set_capacity_period(1, TimeUnits.HOURS)
        network_settings.set_free_flow_travel_time_units(TimeUnits.MINUTES)
        network_settings.set_default_maximum_speed(DEFAULT_MAXIMUM_SPEED_KM_H)
        network_settings.set_coordinate_reference_system("EPSG:26971")

        # TNTP zon reader - prep (pass in net_reader)
        tntp_zon_reader: TntpNetworkReaderWrapper = planit.converter_factory.create(ConverterType.ZONING) \
            .create_reader(ZoningReaderType.TNTP, tntp_net_reader)
        zoning_settings = tntp_zon_reader.settings
        zoning_settings.set_network_file_location(NETWORK_FILE_PATH)

        # TNTP demands reader (pass in zon_reader)
        tntp_dem_reader: TntpDemandsReaderWrapper = \
            demand_converter.create_reader(DemandsReaderType.TNTP, tntp_zon_reader)
        tntp_dem_settings: TntpDemandsReaderSettingsWrapper = tntp_dem_reader.settings
        tntp_dem_settings.set_demand_file_location(DEMAND_FILE_PATH)
        tntp_dem_settings.set_start_time_since_midnight(8.0, TimeUnits.HOURS)
        tntp_dem_settings.set_time_period_duration(1.0, TimeUnits.HOURS)

        # PLANit writer
        planit_writer = demand_converter.create_writer(DemandsWriterType.PLANIT)
        planit_writer.settings.set_output_directory(OUTPUT_PATH)
        planit_writer.settings.set_country(AUSTRALIA)

        # perform conversion
        demand_converter.convert(tntp_dem_reader, planit_writer)

        planit.force_stop_java()
        gc.collect()

    if __name__ == '__main__':
        unittest.main()

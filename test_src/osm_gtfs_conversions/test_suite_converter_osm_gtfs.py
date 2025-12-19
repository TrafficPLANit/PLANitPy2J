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
GERMANY = "Germany"

OSM_PATH = os.path.join(ABSOLUTE_PATH_TEST_DATA_CONVERTER, 'osm')
OSM_INPUT_PATH = os.path.join(OSM_PATH, 'input')
SYDNEY_OSM_PBF_FILE_PATH = os.path.join(OSM_INPUT_PATH, "sydneycbd_2023.osm.pbf")

GTFS_PATH = os.path.join(ABSOLUTE_PATH_TEST_DATA_CONVERTER, 'gtfs')
GTFS_INPUT_PATH = os.path.join(GTFS_PATH, 'input')
SYDNEY_GTFS_FILE_PATH = os.path.join(GTFS_INPUT_PATH, "greatersydneygtfsstaticnoshapes.zip")

PLANIT_PATH = os.path.join(ABSOLUTE_PATH_TEST_DATA_CONVERTER, 'planit')
PLANIT_INPUT_PATH = os.path.join(PLANIT_PATH, 'input')


def minimise_gtfs_sydney_warnings(zoning_settings: GtfsZoningReaderSettingsWrapper,
                                  services_settings: GtfsServicesReaderSettingsWrapper):
    """ access Java utility to minimise warnings for these specific test cases"""
    gtfs_test_package = GatewayUtils.get_package_jvm().org.goplanit.gtfs.util.test
    gtfs_test_package.SydneyGtfsZoningSettingsUtils.minimiseVerifiedWarnings(zoning_settings.java, True)
    gtfs_test_package.SydneyGtfsServicesSettingsUtils.minimiseVerifiedWarnings(services_settings.java)


def minimise_osm_sydney_warnings(network_settings: OsmNetworkReaderSettingsWrapper,
                                 pt_settings: OsmPublicTransportSettingsWrapper):
    """ access Java utility to minimise warnings for these specific test cases"""
    osm_test_package = GatewayUtils.get_package_jvm().org.goplanit.osm.test
    osm_test_package.OsmNetworkSettingsTestCaseUtils.sydney2023MinimiseVerifiedWarnings(network_settings.java)
    osm_test_package.OsmPtSettingsTestCaseUtils.sydney2023MinimiseVerifiedWarnings(pt_settings.java)

class TestSuiteConverterOsmGtfs(unittest.TestCase):
    """ We are testing here if planit_conversions are runnable. We do not actually test the validity of the results
        as this is being done on the Java side. Here, we just make sure the properties can be set as expected and
        the run does not yield any errors/exceptions
    """

    def test_network_converter_osm2matsim_cloud(self):
        OSM_URL = "https://api.openstreetmap.org/api/0.6/map?bbox=13.465661,52.504055,13.469817,52.506204"

        OUTPUT_PATH = os.path.join(OSM_PATH, 'output', 'matsim', 'cloud')

        # no correspondence to Java test as we explicitly test non-failure of Python code to instantiate converters
        planit = Planit()

        # network converter
        network_converter = planit.converter_factory.create(ConverterType.NETWORK)

        # OSM reader
        osm_reader = network_converter.create_reader(NetworkReaderType.OSM, GERMANY)
        osm_reader.settings.set_input_source(OSM_URL)
        osm_reader.settings.deactivate_all_osm_way_types_except(["footway"])
        osm_reader.settings.highway_settings.deactivate_all_osm_road_modes_except(["foot"])

        # MATSim writer
        matsim_writer = network_converter.create_writer(NetworkWriterType.MATSIM)
        matsim_writer.settings.set_output_directory(OUTPUT_PATH)
        matsim_writer.settings.set_country(GERMANY)

        # perform conversion
        network_converter.convert(osm_reader, matsim_writer)

        planit.force_stop_java()
        gc.collect()


    def test_network_converter_osm2matsim_file(self):
        OUTPUT_PATH = os.path.join(OSM_PATH, 'output', 'matsim', 'file')

        # no correspondence to Java test as we explicitly test non-failure of Python code to instantiate converters
        planit = Planit()

        # network converter
        network_converter = planit.converter_factory.create(ConverterType.NETWORK)

        # OSM reader
        osm_reader = network_converter.create_reader(NetworkReaderType.OSM, AUSTRALIA)
        osm_reader.settings.set_input_file(SYDNEY_OSM_PBF_FILE_PATH)

        # MATSim writer
        matsim_writer = network_converter.create_writer(NetworkWriterType.MATSIM)
        matsim_writer.settings.set_output_directory(OUTPUT_PATH)
        matsim_writer.settings.set_country(AUSTRALIA)

        # perform conversion
        network_converter.convert(osm_reader, matsim_writer)

        planit.force_stop_java()
        gc.collect()

    def test_network_converter_osm2planit(self):
        OUTPUT_PATH = os.path.join(OSM_PATH, 'output', 'planit')

        # no correspondence to Java test as we explicitly test non-failure of Python code to instantiate converters
        planit = Planit()

        # network converter
        network_converter = planit.converter_factory.create(ConverterType.NETWORK)

        # OSM reader
        osm_reader = network_converter.create_reader(NetworkReaderType.OSM, AUSTRALIA)
        osm_reader.settings.set_input_file(SYDNEY_OSM_PBF_FILE_PATH)

        # PLANit writer
        planit_writer = network_converter.create_writer(NetworkWriterType.PLANIT)
        planit_writer.settings.set_output_directory(OUTPUT_PATH)
        planit_writer.settings.set_country(AUSTRALIA)

        # perform conversion
        network_converter.convert(osm_reader, planit_writer)

        planit.force_stop_java()
        gc.collect()

    def test_intermodal_converter_osm2matsim(self):
        OUTPUT_PATH = os.path.join(OSM_PATH, 'output', 'matsim')

        # no correspondence to Java test as we explicitly test non-failure of Python code to instantiate converters
        planit = Planit()

        # intermodal converter
        intermodal_converter = planit.converter_factory.create(ConverterType.INTERMODAL)

        # OSM reader
        osm_reader = intermodal_converter.create_reader(IntermodalReaderType.OSM, AUSTRALIA)
        osm_reader.settings.set_input_file(SYDNEY_OSM_PBF_FILE_PATH)

        minimise_osm_sydney_warnings(osm_reader.settings.network_settings, osm_reader.settings.pt_settings)

        # MATSim writer
        matsim_writer = intermodal_converter.create_writer(IntermodalWriterType.MATSIM)
        # test if setting country and output path via separate settings works
        matsim_writer.settings.network_settings.set_output_directory(OUTPUT_PATH)
        matsim_writer.settings.network_settings.set_country(AUSTRALIA)
        matsim_writer.settings.zoning_settings.set_output_directory(OUTPUT_PATH)
        matsim_writer.settings.zoning_settings.set_country(AUSTRALIA)
        matsim_writer.settings.zoning_settings.set_generate_matrix_based_pt_router_files(True)
        # test if setting country and output path via intermodal settings directly works
        matsim_writer.settings.set_output_directory(OUTPUT_PATH)
        matsim_writer.settings.set_country(AUSTRALIA)

        #todo: add pt services settings

        # perform conversion
        intermodal_converter.convert(osm_reader, matsim_writer)

        planit.force_stop_java()
        gc.collect()

    def test_intermodal_converter_osm2planit(self):
        OUTPUT_PATH = os.path.join(OSM_PATH, 'output', 'planit')

        # no correspondence to Java test as we explicitly test non-failure of Python code to instantiate converters
        planit = Planit()

        # intermodal converter
        intermodal_converter = planit.converter_factory.create(ConverterType.INTERMODAL)

        # OSM reader
        osm_reader = intermodal_converter.create_reader(IntermodalReaderType.OSM, AUSTRALIA)
        osm_reader.settings.set_input_file(SYDNEY_OSM_PBF_FILE_PATH)

        minimise_osm_sydney_warnings(osm_reader.settings.network_settings, osm_reader.settings.pt_settings)

        # PLANit writer
        planit_writer = intermodal_converter.create_writer(IntermodalWriterType.PLANIT)
        planit_writer.settings.set_output_directory(OUTPUT_PATH)
        planit_writer.settings.set_country(AUSTRALIA)

        # perform conversion
        intermodal_converter.convert(osm_reader, planit_writer)

        planit.force_stop_java()
        gc.collect()


    def test_intermodal_converter_with_services_osmgtfs2planit(self):
        OUTPUT_PATH = os.path.join(GTFS_PATH, 'output', 'planit')

        # no correspondence to Java test as we explicitly test non-failure of Python code to instantiate converters
        planit = Planit()

        # intermodal converter
        intermodal_converter = planit.converter_factory.create(ConverterType.INTERMODAL)

        # OSM reader
        osm_reader = intermodal_converter.create_reader(IntermodalReaderType.OSM, AUSTRALIA)
        osm_reader.settings.set_input_file(SYDNEY_OSM_PBF_FILE_PATH)

        minimise_osm_sydney_warnings(osm_reader.settings.network_settings, osm_reader.settings.pt_settings)

        # GTFS reader
        gtfs_reader: GtfsIntermodalReaderWrapper = \
            intermodal_converter.create_reader(IntermodalReaderType.GTFS, AUSTRALIA, osm_reader)
        gtfs_reader.settings.set_input_file(SYDNEY_GTFS_FILE_PATH)

        gtfs_reader.settings.services_settings.day_of_week = DayOfWeek.THURSDAY
        assert gtfs_reader.settings.services_settings.day_of_week == DayOfWeek.THURSDAY

        gtfs_reader.settings.services_settings.add_time_period_filter(
            datetime.time(hour=6, minute=0, second=0),
            datetime.time(hour=9, minute=59, second=59)
        )

        minimise_gtfs_sydney_warnings(gtfs_reader.settings.zoning_settings, gtfs_reader.settings.services_settings)

        # PLANit writer
        planit_writer = intermodal_converter.create_writer(IntermodalWriterType.PLANIT)
        planit_writer.settings.set_output_directory(OUTPUT_PATH)
        planit_writer.settings.set_country(AUSTRALIA)

        # perform conversion
        intermodal_converter.convert_with_services(gtfs_reader, planit_writer)

        planit.force_stop_java()
        gc.collect()

    if __name__ == '__main__':
        unittest.main()

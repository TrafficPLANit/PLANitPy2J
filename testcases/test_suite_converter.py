import os
import sys
import datetime

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'src'))

import gc
import unittest
from planit import *

AUSTRALIA = "Australia"
GERMANY = "Germany"

OSM_PATH = os.path.join('converter', 'osm')
OSM_INPUT_PATH = os.path.join(OSM_PATH, 'input')
SYDNEY_OSM_PBF_FILE_PATH = os.path.join(OSM_INPUT_PATH, "sydneycbd.osm.pbf")

GTFS_PATH = os.path.join('converter', 'gtfs')
SYDNEY_GTFS_FILE_PATH = os.path.join(GTFS_PATH, "greatersydneygtfsstaticnoshapes.zip")

PLANIT_PATH = os.path.join('converter', 'planit')
PLANIT_INPUT_PATH = os.path.join(PLANIT_PATH, 'input')

class TestSuiteConverter(unittest.TestCase):
    """ We are testing here if conversions are runnable. We do not actually test the validity of the results
        as this is being done on the Java side. Here, we just make sure the properties can be set as expected and
        the run does not yield any errors/exceptions
    """

    def test_network_converter_osm_reader_all_properties(self):

        # no correspondence to Java test as we explicitly test non-failure of Python code to test all properties
        # are accessible on the OSM reader based on the documentation
        planit = Planit()

        # network converter
        network_converter = planit.converter_factory.create(ConverterType.NETWORK)

        # osm reader        
        osm_reader = network_converter.create_reader(NetworkReaderType.OSM, AUSTRALIA)

        # global settings
        osm_reader.settings.activate_highway_parser(True)
        osm_reader.settings.activate_railway_parser(True)
        osm_reader.settings.deactivate_all_osm_way_types_except(["primary"])
        osm_reader.settings.exclude_osm_ways_from_parsing([12345])
        osm_reader.settings.overwrite_mode_access_by_osm_way_id(123, ["foot"])
        osm_reader.settings.set_always_keep_largest_subnetwork(True)
        osm_reader.settings.set_discard_dangling_networks_above(20)
        osm_reader.settings.set_discard_dangling_networks_below(10)
        osm_reader.settings.set_input_file(SYDNEY_OSM_PBF_FILE_PATH)
        osm_reader.settings.set_remove_dangling_subnetworks(True)
        osm_reader.settings.set_bounding_box(1.2, 3, 4.5, 6)
        osm_reader.settings.set_keep_osm_ways_outside_bounding_box([1, 2, 3.4])

        # highway settings
        osm_reader.settings.highway_settings.activate_all_osm_highway_types()
        osm_reader.settings.highway_settings.activate_osm_highway_types(["primary"])
        osm_reader.settings.highway_settings.add_allowed_highway_modes("primary", ["bus", "foot"])
        osm_reader.settings.highway_settings.deactivate_all_osm_road_modes_except(["bus"])
        osm_reader.settings.highway_settings.deactivate_all_osm_highway_types_except(["primary"])
        osm_reader.settings.highway_settings.deactivate_osm_road_modes(["bus"])
        osm_reader.settings.highway_settings.activate_osm_road_mode("bus")
        osm_reader.settings.highway_settings.deactivate_osm_road_mode("bus")
        osm_reader.settings.highway_settings.deactivate_osm_highway_type("primary")
        osm_reader.settings.highway_settings.set_default_when_osm_highway_type_unsupported("primary")
        osm_reader.settings.highway_settings.overwrite_capacity_max_density_defaults("primary", 2000, 150)
        osm_reader.settings.highway_settings.set_speed_limit_defaults_based_on_urban_area(True)

        # railway settings
        osm_reader.settings.railway_settings.activate_all_osm_railway_types()
        osm_reader.settings.railway_settings.activate_osm_railway_types(["rail", "funicular"])
        osm_reader.settings.railway_settings.deactivate_all_osm_railway_types()
        osm_reader.settings.railway_settings.deactivate_all_osm_railway_types_except(["rail", "monorail"])
        osm_reader.settings.railway_settings.deactivate_all_osm_rail_modes_except(["train", "tram"])
        osm_reader.settings.railway_settings.deactivate_osm_railway_type("rail")
        osm_reader.settings.railway_settings.deactivate_osm_rail_modes(["train", "subway"])
        osm_reader.settings.railway_settings.overwrite_capacity_max_density_defaults("rail", 100000, 100)

        # lane configuration
        osm_reader.settings.lane_configuration.set_default_directional_lanes_by_highway_type("primary", 4)
        osm_reader.settings.lane_configuration.set_default_directional_railway_tracks(2)

        # ensure planit connection is reset
        gc.collect()

    def test_network_converter_matsim_writer_all_properties(self):
        OUTPUT_PATH = os.path.join(OSM_PATH, 'output', 'matsim')

        # no correspondence to Java test as we explicitly test non-failure of Python code to test all properties
        # are accessible on the OSM reader based on the documentation
        planit = Planit()

        # network converter
        network_converter = planit.converter_factory.create(ConverterType.NETWORK)

        # matsim writer
        matsim_writer = network_converter.create_writer(NetworkWriterType.MATSIM)
        matsim_writer.settings.set_output_directory(OUTPUT_PATH)
        matsim_writer.settings.set_country(AUSTRALIA)
        matsim_writer.settings.set_generate_detailed_link_geometry_file(True)
        matsim_writer.settings.set_file_name("my_network")

        # ensure planit connection is reset
        gc.collect()

    def test_intermodal_converter_osm_reader_all_properties(self):

        # no correspondence to Java test as we explicitly test non-failure of Python code to test all properties
        # are accessible on the OSM reader based on the documentation
        planit = Planit()

        # network converter
        intermodal_converter = planit.converter_factory.create(ConverterType.INTERMODAL)

        # osm reader        
        osm_reader = intermodal_converter.create_reader(IntermodalReaderType.OSM, AUSTRALIA)

        # global settings 
        osm_reader.settings.set_input_file(SYDNEY_OSM_PBF_FILE_PATH)

        # network settings (just test one, since it is the same as network reader settings
        osm_reader.settings.network_settings.highway_settings.set_default_when_osm_highway_type_unsupported("primary")

        # PT settings
        osm_reader.settings.pt_settings.exclude_osm_nodes_by_id([123, 12345678])
        osm_reader.settings.pt_settings.exclude_osm_ways_by_id([123, 12345678])
        osm_reader.settings.pt_settings.overwrite_waiting_area_of_stop_location(123, OsmEntityType.WAY, 12345678)
        osm_reader.settings.pt_settings.overwrite_waiting_area_nominated_osm_way_for_stop_location(123456789,
                                                                                                   OsmEntityType.NODE,
                                                                                                   123)
        osm_reader.settings.pt_settings.set_remove_dangling_transfer_zone_groups(True)
        osm_reader.settings.pt_settings.set_remove_dangling_zones(True)
        osm_reader.settings.pt_settings.set_station_to_waiting_area_search_radius_meters(100)
        osm_reader.settings.pt_settings.set_stop_to_waiting_area_search_radius_meters(1.45)
        osm_reader.settings.pt_settings.set_station_to_parallel_tracks_search_radius_meters(50)

        # ensure planit connection is reset
        gc.collect()

    def test_intermodal_converter_matsim_writer_all_properties(self):
        OUTPUT_PATH = os.path.join(OSM_PATH, 'output', 'matsim')

        # no correspondence to Java test as we explicitly test non-failure of Python code to test all properties
        # are accessible on the OSM reader based on the documentation
        planit = Planit()

        # intermodal converter
        intermodal_converter = planit.converter_factory.create(ConverterType.INTERMODAL)

        # matsim writer        
        matsim_writer = intermodal_converter.create_writer(IntermodalWriterType.MATSIM)

        # global settings 
        matsim_writer.settings.set_output_directory(OUTPUT_PATH)
        matsim_writer.settings.set_country(AUSTRALIA)

        # network settings (just test one, since it is the same as network reader settings
        matsim_writer.settings.network_settings.set_file_name("matsim_network")

        # zoning settings, see if collectable
        zoning_settings = matsim_writer.settings.zoning_settings
        zoning_settings.set_generate_matrix_based_pt_router_files(True)

        # ensure planit connection is reset
        gc.collect()

    def test_network_converter_planit_writer_reader_all_properties(self):
        OUTPUT_PATH = os.path.join(OSM_PATH, 'output', 'planit')

        # no correspondence to Java test as we explicitly test non-failure of Python code to test all properties
        # are accessible on the OSM reader based on the documentation
        planit = Planit()

        # network converter
        network_converter = planit.converter_factory.create(ConverterType.NETWORK)

        # PLANit reader       
        planit_reader = network_converter.create_reader(NetworkReaderType.PLANIT)
        planit_reader.settings.set_input_directory(OSM_PATH)
        planit_reader.settings.set_xml_file_extension(".not_xml")

        # PLANit writer        
        planit_writer = network_converter.create_writer(NetworkWriterType.PLANIT)

        # settings 
        planit_writer.settings.set_output_directory(OUTPUT_PATH)
        planit_writer.settings.set_file_name("test.xml")
        planit_writer.settings.set_country(AUSTRALIA)

        # ensure planit connection is reset
        gc.collect()

    def test_intermodal_converter_planit_writer_reader_all_properties(self):
        OUTPUT_PATH = os.path.join(OSM_PATH, 'output', 'planit')

        # no correspondence to Java test as we explicitly test non-failure of Python code to test all properties
        # are accessible on the OSM reader based on the documentation
        planit = Planit()

        # intermodal converter
        intermodal_converter = planit.converter_factory.create(ConverterType.INTERMODAL)

        # PLANit reader       
        planit_reader = intermodal_converter.create_reader(IntermodalReaderType.PLANIT)
        planit_reader.settings.set_input_directory(OSM_PATH)

        # network settings
        planit_reader.settings.network_settings.set_input_directory(OSM_PATH)
        planit_reader.settings.network_settings.set_xml_file_extension(".not_xml")

        # zoning settings
        planit_reader.settings.zoning_settings.set_input_directory(OSM_PATH)
        planit_reader.settings.zoning_settings.set_xml_file_extension(".not_xml")

        # PLANit writer        
        planit_writer = intermodal_converter.create_writer(IntermodalWriterType.PLANIT)

        # global settings 
        planit_writer.settings.set_output_directory(OUTPUT_PATH)
        planit_writer.settings.set_country(AUSTRALIA)

        # network settings
        planit_writer.settings.network_settings.set_output_directory(OUTPUT_PATH)
        planit_writer.settings.network_settings.set_file_name("test.xml")

        # zoning settings
        planit_writer.settings.zoning_settings.set_output_directory(OUTPUT_PATH)
        planit_writer.settings.zoning_settings.set_file_name("test.xml")

        # ensure planit connection is reset
        gc.collect()

    def test_network_converter_osm2matsim_cloud(self):
        OSM_URL = "https://api.openstreetmap.org/api/0.6/map?bbox=13.465661,52.504055,13.469817,52.506204"

        OUTPUT_PATH = os.path.join(OSM_PATH, 'output', 'matsim', 'cloud')

        # no correspondence to Java test as we explicitly test non-failure of Python code to instantiate converters
        planit = Planit()

        # network converter
        network_converter = planit.converter_factory.create(ConverterType.NETWORK)

        # osm reader        
        osm_reader = network_converter.create_reader(NetworkReaderType.OSM, GERMANY)
        osm_reader.settings.set_input_source(OSM_URL)
        osm_reader.settings.deactivate_all_osm_way_types_except(["footway"])
        osm_reader.settings.highway_settings.deactivate_all_osm_road_modes_except(["foot"])

        # matsim writer
        matsim_writer = network_converter.create_writer(NetworkWriterType.MATSIM)
        matsim_writer.settings.set_output_directory(OUTPUT_PATH)
        matsim_writer.settings.set_country(GERMANY)

        # perform conversion
        network_converter.convert(osm_reader, matsim_writer)
        gc.collect()

    def test_network_converter_osm2matsim_file(self):
        OUTPUT_PATH = os.path.join(OSM_PATH, 'output', 'matsim', 'file')

        # no correspondence to Java test as we explicitly test non-failure of Python code to instantiate converters
        planit = Planit()

        # network converter
        network_converter = planit.converter_factory.create(ConverterType.NETWORK)

        # osm reader        
        osm_reader = network_converter.create_reader(NetworkReaderType.OSM, AUSTRALIA)
        osm_reader.settings.set_input_file(SYDNEY_OSM_PBF_FILE_PATH)

        # matsim writer
        matsim_writer = network_converter.create_writer(NetworkWriterType.MATSIM)
        matsim_writer.settings.set_output_directory(OUTPUT_PATH)
        matsim_writer.settings.set_country(AUSTRALIA)

        # perform conversion
        network_converter.convert(osm_reader, matsim_writer)
        gc.collect()

    def test_network_converter_osm2planit(self):
        OUTPUT_PATH = os.path.join(OSM_PATH, 'output', 'planit')

        # no correspondence to Java test as we explicitly test non-failure of Python code to instantiate converters
        planit = Planit()

        # network converter
        network_converter = planit.converter_factory.create(ConverterType.NETWORK)

        # osm reader        
        osm_reader = network_converter.create_reader(NetworkReaderType.OSM, AUSTRALIA)
        osm_reader.settings.set_input_file(SYDNEY_OSM_PBF_FILE_PATH)

        # planit writer
        planit_writer = network_converter.create_writer(NetworkWriterType.PLANIT)
        planit_writer.settings.set_output_directory(OUTPUT_PATH)
        planit_writer.settings.set_country(AUSTRALIA)

        # perform conversion
        network_converter.convert(osm_reader, planit_writer)
        gc.collect()

    def test_intermodal_converter_osm2matsim(self):
        OUTPUT_PATH = os.path.join(OSM_PATH, 'output', 'matsim')

        # no correspondence to Java test as we explicitly test non-failure of Python code to instantiate converters
        planit = Planit()

        # intermodal converter
        intermodal_converter = planit.converter_factory.create(ConverterType.INTERMODAL)

        # osm reader        
        osm_reader = intermodal_converter.create_reader(IntermodalReaderType.OSM, AUSTRALIA)
        osm_reader.settings.set_input_file(SYDNEY_OSM_PBF_FILE_PATH)

        # matsim writer
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

        # perform conversion
        intermodal_converter.convert(osm_reader, matsim_writer)
        gc.collect()

    def test_intermodal_converter_osm2planit(self):
        OUTPUT_PATH = os.path.join(OSM_PATH, 'output', 'planit')

        # no correspondence to Java test as we explicitly test non-failure of Python code to instantiate converters
        planit = Planit()

        # intermodal converter
        intermodal_converter = planit.converter_factory.create(ConverterType.INTERMODAL)

        # osm reader        
        osm_reader = intermodal_converter.create_reader(IntermodalReaderType.OSM, AUSTRALIA)
        osm_reader.settings.set_input_file(SYDNEY_OSM_PBF_FILE_PATH)

        # planit writer
        planit_writer = intermodal_converter.create_writer(IntermodalWriterType.PLANIT)
        planit_writer.settings.set_output_directory(OUTPUT_PATH)
        planit_writer.settings.set_country(AUSTRALIA)

        # perform conversion
        intermodal_converter.convert(osm_reader, planit_writer)
        gc.collect()

    # TODO: the gtfs_Reader portion of the below test is not yet operational, this is to be created as part of v0.4.0 release
    def test_intermodal_converter_with_services_osmgtfs2planit(self):
        OUTPUT_PATH = os.path.join(OSM_PATH, 'output', 'planit')

        # no correspondence to Java test as we explicitly test non-failure of Python code to instantiate converters
        planit = Planit()

        # intermodal converter
        intermodal_converter = planit.converter_factory.create(ConverterType.INTERMODAL)

        # osm reader
        osm_reader = intermodal_converter.create_reader(IntermodalReaderType.OSM, AUSTRALIA)
        osm_reader.settings.set_input_file(SYDNEY_OSM_PBF_FILE_PATH)

        # GTFS reader
        gtfs_reader = intermodal_converter.create_reader(IntermodalReaderType.GTFS, AUSTRALIA, osm_reader)
        gtfs_reader.settings.set_input_file(SYDNEY_GTFS_FILE_PATH)
        gtfs_reader.settings.services_settings.day_of_week = DayOfWeek.THURSDAY
        gtfs_reader.settings.services_settings.add_time_period_filter(
            datetime.time(hour=6, minute=0, second=0),
            datetime.time(hour=9, minute=59, second=59)
        )

        # planit writer
        planit_writer = intermodal_converter.create_writer(IntermodalWriterType.PLANIT)
        planit_writer.settings.set_output_directory(OUTPUT_PATH)
        planit_writer.settings.set_country(AUSTRALIA)

        # perform conversion
        intermodal_converter.convert(gtfs_reader, planit_writer)
        gc.collect()

    def test_network_converter_planit2planit(self):
        OUTPUT_PATH = os.path.join(PLANIT_PATH, 'output', 'planit')

        # no correspondence to Java test as we explicitly test non-failure of Python code to instantiate converters
        plan_it = Planit()

        # network converter
        network_converter = plan_it.converter_factory.create(ConverterType.NETWORK)

        # planit reader        
        planit_reader = network_converter.create_reader(NetworkReaderType.PLANIT)
        planit_reader.settings.set_input_directory(PLANIT_INPUT_PATH)

        # planit writer
        planit_writer = network_converter.create_writer(NetworkWriterType.PLANIT)
        planit_writer.settings.set_output_directory(OUTPUT_PATH)
        planit_writer.settings.set_country(AUSTRALIA)

        # perform conversion
        network_converter.convert(planit_reader, planit_writer)
        # result should be the same file, although we do not test this here automatically yet
        gc.collect()

    def test_intermodal_converter_planit2planit(self):
        OUTPUT_PATH = os.path.join(PLANIT_PATH, 'output', 'planit')

        # no correspondence to Java test as we explicitly test non-failure of Python code to instantiate converters
        plan_it = Planit()

        # network converter
        intermodal_converter = plan_it.converter_factory.create(ConverterType.INTERMODAL)

        # planit reader        
        planit_reader = intermodal_converter.create_reader(IntermodalReaderType.PLANIT)
        planit_reader.settings.set_input_directory(PLANIT_INPUT_PATH)

        # planit writer
        planit_writer = intermodal_converter.create_writer(IntermodalWriterType.PLANIT)
        # test if setting country and output path via separate settings works
        planit_writer.settings.network_settings.set_output_directory(OUTPUT_PATH)
        planit_writer.settings.zoning_settings.set_output_directory(OUTPUT_PATH)
        planit_writer.settings.zoning_settings.set_country(AUSTRALIA)
        # test if setting country and output path via intermodal settings directly works
        planit_writer.settings.set_output_directory(OUTPUT_PATH)
        planit_writer.settings.set_country(AUSTRALIA)

        # perform conversion
        intermodal_converter.convert(planit_reader, planit_writer)
        gc.collect()

    if __name__ == '__main__':
        unittest.main()

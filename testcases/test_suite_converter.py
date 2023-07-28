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
GTFS_INPUT_PATH = os.path.join(GTFS_PATH, 'input')
SYDNEY_GTFS_FILE_PATH = os.path.join(GTFS_INPUT_PATH, "greatersydneygtfsstaticnoshapes.zip")

OSM_GTFS_PATH = os.path.join('converter', 'osm_gtfs')

GEOIO_PATH = os.path.join('converter', 'geoio')

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
        osm_reader.settings.highway_settings.add_allowed_osm_highway_modes("primary", ["bus", "foot"])
        osm_reader.settings.highway_settings.deactivate_all_osm_road_modes_except(["bus"])
        osm_reader.settings.highway_settings.deactivate_all_osm_highway_types_except(["primary"])
        osm_reader.settings.highway_settings.deactivate_osm_road_modes(["bus"])
        osm_reader.settings.highway_settings.activate_osm_road_mode("bus")
        osm_reader.settings.highway_settings.deactivate_osm_road_mode("bus")
        osm_reader.settings.highway_settings.deactivate_osm_highway_type("primary")
        osm_reader.settings.highway_settings.set_default_when_osm_highway_type_unsupported("primary")
        osm_reader.settings.highway_settings.overwrite_capacity_max_density_defaults("primary", 2000, 150)

        # added v0.4.0
        osm_modes = osm_reader.settings.highway_settings.collect_allowed_osm_highway_modes("primary")
        assert osm_reader.settings.highway_settings.get_default_speed_limit_by_osm_highway_type("primary") == 60.0
        assert osm_reader.settings.highway_settings.is_speed_limit_defaults_based_on_urban_area() is True
        assert osm_reader.settings.highway_settings.is_osm_highway_type_deactivated("primary") is True
        assert osm_reader.settings.highway_settings.is_osm_highway_type_activated("primary") is False

        osm_reader.settings.highway_settings.activate_osm_highway_type("primary")
        cap, max_density = \
            osm_reader.settings.highway_settings.get_overwritten_capacity_max_density_by_osm_highway_type("primary")
        assert round(cap, 0) == 2000
        assert round(max_density, 0) == 150
        osm_reader.settings.highway_settings.set_speed_limit_defaults_based_on_urban_area(True)
        osm_reader.settings.highway_settings.remove_all_road_modes()
        assert osm_reader.settings.is_highway_parser_active() is True

        planit_pedestrian_mode = osm_reader.settings.highway_settings.get_mapped_planit_road_mode("foot")
        assert planit_pedestrian_mode is None
        osm_reader.settings.highway_settings.activate_osm_road_mode("foot")
        planit_pedestrian_mode = osm_reader.settings.highway_settings.get_mapped_planit_road_mode("foot")
        assert planit_pedestrian_mode is PredefinedModeType.PEDESTRIAN
        assert "foot" in \
               osm_reader.settings.highway_settings.get_mapped_osm_road_modes(planit_pedestrian_mode)

        # railway settings
        osm_reader.settings.railway_settings.activate_all_osm_railway_types()
        osm_reader.settings.railway_settings.activate_osm_railway_types(["rail", "funicular"])
        osm_reader.settings.railway_settings.deactivate_all_osm_railway_types()
        osm_reader.settings.railway_settings.deactivate_all_osm_railway_types_except(["rail", "monorail"])
        osm_reader.settings.railway_settings.deactivate_all_osm_rail_modes_except(["train", "tram"])
        osm_reader.settings.railway_settings.deactivate_osm_railway_type("rail")
        osm_reader.settings.railway_settings.deactivate_osm_rail_modes(["train", "subway"])
        osm_reader.settings.railway_settings.overwrite_capacity_max_density_defaults("rail", 100000, 100)

        # added v0.4.0
        assert osm_reader.settings.is_railway_parser_active() is True
        assert osm_reader.settings.railway_settings.is_osm_railway_type_deactivated("rail") is True
        assert osm_reader.settings.railway_settings.is_osm_railway_type_activated("rail") is False
        osm_reader.settings.railway_settings.activate_osm_railway_type("rail")
        assert True is osm_reader.settings.railway_settings.\
            is_default_capacity_or_max_density_overwritten_by_osm_railway_type("rail")
        cap, max_density = \
            osm_reader.settings.railway_settings.get_overwritten_capacity_max_density_by_osm_railway_type("rail")
        assert round(cap, 0) == 100000
        assert round(max_density, 0) == 100
        osm_reader.settings.railway_settings.get_default_speed_limit_by_osm_railway_type("rail")
        osm_reader.settings.railway_settings.deactivate_all_osm_rail_modes()
        osm_reader.settings.railway_settings.activate_osm_rail_mode("train")
        osm_reader.settings.railway_settings.deactivate_osm_rail_mode("train")

        planit_train_mode = osm_reader.settings.railway_settings.get_mapped_planit_rail_mode("train")
        assert planit_train_mode is None
        osm_reader.settings.railway_settings.activate_osm_rail_mode("train")
        planit_train_mode = osm_reader.settings.railway_settings.get_mapped_planit_rail_mode("train")
        assert planit_train_mode is PredefinedModeType.TRAIN
        assert "train" in osm_reader.settings.railway_settings.get_mapped_osm_rail_modes(planit_train_mode)

        #waterway settings (new in v0.4.0)
        assert osm_reader.settings.is_waterway_parser_active() is False
        osm_reader.settings.activate_waterway_parser(True)
        osm_reader.settings.waterway_settings.activate_all_osm_waterway_types()
        assert osm_reader.settings.waterway_settings.is_osm_waterway_type_deactivated("primary") is False
        osm_reader.settings.waterway_settings.activate_osm_waterway_types(["primary", "secondary"])
        osm_reader.settings.waterway_settings.deactivate_all_osm_water_modes_except(["ferry"])
        osm_reader.settings.waterway_settings.deactivate_all_osm_waterway_types_except(["primary"])
        osm_reader.settings.waterway_settings.deactivate_all_osm_water_modes()
        osm_reader.settings.waterway_settings.deactivate_osm_water_modes(["ferry"])
        osm_reader.settings.waterway_settings.activate_osm_water_mode("ferry")
        osm_reader.settings.waterway_settings.deactivate_osm_water_mode("ferry")
        osm_reader.settings.waterway_settings.deactivate_osm_waterway_type("primary")
        osm_reader.settings.waterway_settings.overwrite_capacity_max_density_defaults("primary", 2000, 150)
        assert osm_reader.settings.waterway_settings.is_osm_waterway_type_deactivated("primary") is True
        assert osm_reader.settings.waterway_settings.is_osm_waterway_type_activated("primary") is False
        osm_reader.settings.waterway_settings.activate_osm_waterway_type("primary")
        assert True is osm_reader.settings.waterway_settings.\
            is_default_capacity_or_max_density_overwritten_by_osm_waterway_route_type("primary")
        cap, max_density = \
            osm_reader.settings.waterway_settings.get_overwritten_capacity_max_density_by_osm_waterway_route_type("primary")
        assert round(cap, 0) == 2000
        assert round(max_density, 0) == 150
        osm_reader.settings.waterway_settings.get_default_speed_limit_by_osm_waterway_type("primary")

        # lane configuration
        osm_reader.settings.lane_configuration.set_default_directional_lanes_by_highway_type("primary", 4)
        osm_reader.settings.lane_configuration.set_default_directional_railway_tracks(2)

        # ensure planit connection is reset
        gc.collect()

    def test_converter_osm_reader_all_properties(self):
        # no correspondence to Java test as we explicitly test non-failure of Python code to test all properties
        # are accessible on the OSM reader based on the documentation
        planit = Planit()

        # OSM reader
        osm_reader = planit.converter_factory.create(ConverterType.INTERMODAL).create_reader(
            IntermodalReaderType.OSM, AUSTRALIA)

        pt_settings = osm_reader.settings.pt_settings
        pt_settings.exclude_osm_nodes_by_id([1234, 5678])
        pt_settings.exclude_osm_ways_by_id([1234, 5678])
        pt_settings.overwrite_waiting_area_of_stop_location(1234, OsmEntityType.WAY, 56789)
        assert pt_settings.is_overwrite_waiting_area_of_stop_location(1234) is True
        pt_settings.overwrite_waiting_area_nominated_osm_way_for_stop_location(
            1234, OsmEntityType.WAY, 56789) # changed in v0.4.0
        assert pt_settings.has_waiting_area_nominated_osm_way_for_stop_location(
            1234, OsmEntityType.WAY) is True
        pt_settings.set_remove_dangling_transfer_zone_groups(False)
        assert pt_settings.is_remove_dangling_transfer_zone_groups() is False
        pt_settings.set_station_to_waiting_area_search_radius_meters(50)
        assert round(pt_settings.get_station_to_waiting_area_search_radius_meters(), 0) == 50
        pt_settings.set_stop_to_waiting_area_search_radius_meters(50)
        assert round(pt_settings.get_stop_to_waiting_area_search_radius_meters(), 0) == 50
        pt_settings.set_station_to_parallel_tracks_search_radius_meters(50)
        assert round(pt_settings.get_station_to_parallel_tracks_search_radius_meters(), 0) == 50

        #v0.4.0
        pt_settings.exclude_osm_node_by_id(1234)
        pt_settings.exclude_osm_way_by_id(1234)
        assert pt_settings.is_excluded_osm_node(1234) is True
        assert pt_settings.is_excluded_osm_way(1234) is True
        pt_settings.set_remove_dangling_transfer_zone_groups(True)
        assert pt_settings.is_remove_dangling_transfer_zone_groups() is True
        pt_settings.suppress_osm_relation_stop_area_logging([1234, 5678, 91011])
        assert pt_settings.is_suppress_osm_relation_stop_area_logging(1234) is True
        pt_settings.set_connect_dangling_ferry_stop_to_nearby_ferry_route(True)
        assert pt_settings.is_connect_dangling_ferry_stop_to_nearby_ferry_route() is True
        pt_settings.set_ferry_stop_to_ferry_route_search_radius_meters(40)
        assert round(pt_settings.get_ferry_stop_to_ferry_route_search_radius_meters(),0) == 40
        pt_settings.overwrite_waiting_area_mode_Access(1234, OsmEntityType.WAY, ["tram"])
        assert "tram" in pt_settings.get_overwritten_waiting_area_mode_Access(1234, OsmEntityType.WAY)

        # ensure planit connection is reset
        gc.collect()

    def test_converter_gtfs_reader_all_properties(self):
        # no correspondence to Java test as we explicitly test non-failure of Python code to instantiate converters
        planit = Planit()

        # intermodal converter
        intermodal_converter = planit.converter_factory.create(ConverterType.INTERMODAL)

        # OSM reader (to feed to GTFS reader) - new in v0.4.0
        osm_reader = intermodal_converter.create_reader(IntermodalReaderType.OSM, AUSTRALIA)
        osm_reader.settings.set_input_file(SYDNEY_OSM_PBF_FILE_PATH)

        #############
        # GTFS reader - new in v0.4.0
        gtfs_reader = intermodal_converter.create_reader(IntermodalReaderType.GTFS, AUSTRALIA, osm_reader)
        gtfs_reader.settings.set_input_file(SYDNEY_GTFS_FILE_PATH)

        # (transfer) zoning settings - new in v0.4.0
        zoning_settings = gtfs_reader.settings.zoning_settings
        #todo: continue here, add all properties to test

        # (transfer) zoning settings - new in v0.4.0
        service_settings = gtfs_reader.settings.service_settings
        #todo: continue here, add all properties to test

        gtfs_reader.settings.service_settings.day_of_week = DayOfWeek.THURSDAY
        assert gtfs_reader.settings.service_settings.day_of_week == DayOfWeek.THURSDAY

        gtfs_reader.settings.service_settings.add_time_period_filter(
            datetime.time(hour=6, minute=0, second=0),
            datetime.time(hour=9, minute=59, second=59)
        )

        gc.collect()

    def test_converter_matsim_writer_all_properties(self):
        OUTPUT_PATH = os.path.join(OSM_PATH, 'output', 'matsim')

        # no correspondence to Java test as we explicitly test non-failure of Python code to test all properties
        # are accessible on the OSM reader based on the documentation
        planit = Planit()

        # matsim writer
        matsim_writer = planit.converter_factory.create(
            ConverterType.INTERMODAL).create_writer(IntermodalWriterType.MATSIM)

        # v0.4.0
        matsim_writer.set_id_mapper_type(IdMapperType.XML)
        assert matsim_writer.get_id_mapper_type() is IdMapperType.XML

        # general
        matsim_writer.settings.set_output_directory(OUTPUT_PATH)
        matsim_writer.settings.set_country(AUSTRALIA)
        matsim_writer.settings.set_file_name("my_network")

        #network specific
        network_settings = matsim_writer.settings.network_settings
        network_settings.set_generate_detailed_link_geometry_file(True)
        assert network_settings.is_generate_detailed_link_geometry_file() is True

        # v0.4.0
        network_settings.set_restrict_link_speed_by_supported_modes(True)
        assert network_settings.is_restrict_link_speed_by_supported_modes() is True

        # zoning specific (only when not writing with services)
        zoning_settings = matsim_writer.settings.zoning_settings
        zoning_settings.set_generate_matrix_based_pt_router_files(True)
        assert zoning_settings.is_generate_matrix_based_pt_router_files() is True

        # pt services specific (only when writing with services) - new to v0.4.0
        pt_services_settings = matsim_writer.settings.pt_services_settings
        pt_services_settings.set_await_departures(True)
        assert pt_services_settings.is_await_departures() is True

        # ensure planit connection is reset
        gc.collect()

    def test_converter_planit_writer_reader_all_properties(self):
        OUTPUT_PATH = os.path.join(PLANIT_PATH, 'output', 'planit')

        # no correspondence to Java test as we explicitly test non-failure of Python code to test all properties
        # are accessible on the OSM reader based on the documentation
        planit = Planit()

        # intermodal converter
        intermodal_converter = planit.converter_factory.create(ConverterType.INTERMODAL)

        ###############
        # PLANit reader       
        planit_reader = intermodal_converter.create_reader(IntermodalReaderType.PLANIT)
        planit_reader.settings.set_input_directory(PLANIT_PATH)

        # network settings
        planit_reader.settings.network_settings.set_input_directory(OSM_PATH)
        planit_reader.settings.network_settings.set_xml_file_extension(".not_xml")

        # zoning settings
        planit_reader.settings.zoning_settings.set_input_directory(OSM_PATH)
        planit_reader.settings.zoning_settings.set_xml_file_extension(".not_xml")

        # service network settings
        planit_reader.settings.service_network_settings.set_xml_file_extension(".not_xml")

        # routed services settings
        planit_reader.settings.routed_services_settings.set_xml_file_extension(".not_xml")

        ###############
        # PLANit writer        
        planit_writer = intermodal_converter.create_writer(IntermodalWriterType.PLANIT)

        # global settings 
        planit_writer.settings.set_output_directory(OUTPUT_PATH)
        planit_writer.settings.set_country(AUSTRALIA)

        # network settings
        planit_writer.settings.network_settings.set_output_directory(OUTPUT_PATH)
        planit_writer.settings.network_settings.set_file_name("network.xml")

        # zoning settings
        planit_writer.settings.zoning_settings.set_output_directory(OUTPUT_PATH)
        planit_writer.settings.zoning_settings.set_file_name("zoning.xml")

        # service network settings
        planit_writer.settings.service_network_settings.set_file_name("service_network.xml")

        # routed services settings
        planit_writer.settings.routed_services_settings.set_file_name("routed_services.xml")

        # ensure planit connection is reset
        gc.collect()

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

        # perform conversion
        intermodal_converter.convert(osm_reader, matsim_writer)
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

        # PLANit writer
        planit_writer = intermodal_converter.create_writer(IntermodalWriterType.PLANIT)
        planit_writer.settings.set_output_directory(OUTPUT_PATH)
        planit_writer.settings.set_country(AUSTRALIA)

        # perform conversion
        intermodal_converter.convert(osm_reader, planit_writer)
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

        # GTFS reader
        gtfs_reader = intermodal_converter.create_reader(IntermodalReaderType.GTFS, AUSTRALIA, osm_reader)
        gtfs_reader.settings.set_input_file(SYDNEY_GTFS_FILE_PATH)

        gtfs_reader.settings.service_settings.day_of_week = DayOfWeek.THURSDAY
        assert gtfs_reader.settings.service_settings.day_of_week == DayOfWeek.THURSDAY

        gtfs_reader.settings.service_settings.add_time_period_filter(
            datetime.time(hour=6, minute=0, second=0),
            datetime.time(hour=9, minute=59, second=59)
        )

        # planit writer
        planit_writer = intermodal_converter.create_writer(IntermodalWriterType.PLANIT)
        planit_writer.settings.set_output_directory(OUTPUT_PATH)
        planit_writer.settings.set_country(AUSTRALIA)

        # perform conversion
        intermodal_converter.convert_with_services(gtfs_reader, planit_writer)
        gc.collect()

    # TODO: workig on support for GEOIO converter on python side by means of this test. NOT DONE
    def test_intermodal_converter_with_services_planit2geoio(self):
        OUTPUT_PATH = os.path.join(PLANIT_PATH, 'output', 'geoio')

        # no correspondence to Java test as we explicitly test non-failure of Python code to instantiate converters
        planit = Planit()

        # intermodal converter
        intermodal_converter = planit.converter_factory.create(ConverterType.INTERMODAL)

        # PLANit reader
        planit_reader = intermodal_converter.create_reader(IntermodalReaderType.PLANIT, AUSTRALIA)
        planit_reader.settings.set_input_directory(PLANIT_INPUT_PATH)

        # GeoIo (GIS geometry shape) writer
        geo_writer = intermodal_converter.create_writer(IntermodalWriterType.GEOIO)
        geo_writer.settings.set_output_directory(OUTPUT_PATH)
        geo_writer.settings.set_country(AUSTRALIA)

        geo_writer.settings.zoning_settings.persist_virtual_network = True
        geo_writer.set_id_mapper_type(IdMapperType.XML)

        # perform conversion
        intermodal_converter.convert_with_services(planit_reader, geo_writer)
        gc.collect()

    def test_network_converter_planit2planit(self):
        OUTPUT_PATH = os.path.join(PLANIT_PATH, 'output', 'planit')

        # no correspondence to Java test as we explicitly test non-failure of Python code to instantiate converters
        plan_it = Planit()

        # network converter
        network_converter = plan_it.converter_factory.create(ConverterType.NETWORK)

        # PLANit reader
        planit_reader = network_converter.create_reader(NetworkReaderType.PLANIT)
        planit_reader.settings.set_input_directory(PLANIT_INPUT_PATH)

        # PLANit writer
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

        # PLANit reader
        planit_reader = intermodal_converter.create_reader(IntermodalReaderType.PLANIT)
        planit_reader.settings.set_input_directory(PLANIT_INPUT_PATH)

        # PLANit writer
        planit_writer = intermodal_converter.create_writer(IntermodalWriterType.PLANIT)
        # test if setting country and output path via separate settings works
        planit_writer.settings.network_settings.set_output_directory(OUTPUT_PATH)
        planit_writer.settings.zoning_settings.set_output_directory(OUTPUT_PATH)
        planit_writer.settings.zoning_settings.set_country(AUSTRALIA)
        # test if setting country and output path via intermodal settings directly works
        planit_writer.settings.set_output_directory(OUTPUT_PATH)
        planit_writer.settings.set_country(AUSTRALIA)

        # perform conversions, test that running conversion twice does not cause problems
        intermodal_converter.convert(planit_reader, planit_writer)
        intermodal_converter.convert_with_services(planit_reader, planit_writer)
        gc.collect()

    if __name__ == '__main__':
        unittest.main()

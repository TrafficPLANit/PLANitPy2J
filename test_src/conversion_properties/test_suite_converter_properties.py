import os
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '../..', 'src'))

from planit.converter import DemandsConverter

ABSOLUTE_PATH = os.path.dirname(__file__)
ABSOLUTE_PATH_TEST_DATA = os.path.join(ABSOLUTE_PATH, '..', '..', 'testdata')
ABSOLUTE_PATH_TEST_DATA_CONVERTER = os.path.join(ABSOLUTE_PATH_TEST_DATA, 'converter')

import gc
import unittest
from planit import *

AUSTRALIA = "Australia"

OSM_PATH = os.path.join(ABSOLUTE_PATH_TEST_DATA_CONVERTER, 'osm')
OSM_INPUT_PATH = os.path.join(OSM_PATH, 'input')
SYDNEY_OSM_PBF_FILE_PATH = os.path.join(OSM_INPUT_PATH, "sydneycbd_2023.osm.pbf")

GTFS_PATH = os.path.join(ABSOLUTE_PATH_TEST_DATA_CONVERTER, 'gtfs')
GTFS_INPUT_PATH = os.path.join(GTFS_PATH, 'input')
SYDNEY_GTFS_FILE_PATH = os.path.join(GTFS_INPUT_PATH, "greatersydneygtfsstaticnoshapes.zip")

PLANIT_PATH = os.path.join(ABSOLUTE_PATH_TEST_DATA_CONVERTER, 'planit')
PLANIT_INPUT_PATH = os.path.join(PLANIT_PATH, 'input')


class TestSuiteConverterProperties(unittest.TestCase):
    """ We are testing here if planit_conversions are runnable. We do not actually test the validity of the results
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
        assert osm_reader.settings.is_remove_dangling_subnetworks() is True
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
        osm_reader.settings.highway_settings.overwrite_capacity_max_density_defaults("primary", 2000, 150)

        # added v0.4.0
        osm_modes = osm_reader.settings.highway_settings.collect_allowed_osm_highway_modes("primary")
        assert osm_reader.settings.highway_settings.get_default_speed_limit_by_osm_highway_type("primary") == 60.0
        assert osm_reader.settings.highway_settings.is_osm_highway_type_deactivated("primary") is True
        assert osm_reader.settings.highway_settings.is_osm_highway_type_activated("primary") is False
        assert osm_reader.settings.highway_settings.is_speed_limit_defaults_based_on_urban_area() is True

        osm_reader.settings.highway_settings.activate_osm_highway_type("primary")
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

        cap, max_density = \
            osm_reader.settings.highway_settings.get_overwritten_capacity_max_density_by_osm_highway_type(
                "primary")  # not yet documented
        assert round(cap, 0) == 2000
        assert round(max_density, 0) == 150

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
        assert True is osm_reader.settings.railway_settings. \
            is_default_capacity_or_max_density_overwritten_by_osm_railway_type("rail")  # not documented yet
        cap, max_density = \
            osm_reader.settings.railway_settings.get_overwritten_capacity_max_density_by_osm_railway_type(
                "rail")  # not documented yet
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

        # waterway settings (new in v0.4.0)
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
        osm_reader.settings.waterway_settings.get_default_speed_limit_by_osm_waterway_type("primary")

        assert True is osm_reader.settings.waterway_settings. \
            is_default_capacity_or_max_density_overwritten_by_osm_waterway_route_type(
            "primary")  # Not yet documented in Python docs
        cap, max_density = \
            osm_reader.settings.waterway_settings.get_overwritten_capacity_max_density_by_osm_waterway_route_type(
                "primary")  # Not yet documented in Python docs
        assert round(cap, 0) == 2000
        assert round(max_density, 0) == 150

        # lane configuration
        osm_reader.settings.lane_configuration.set_default_directional_lanes_by_highway_type("primary", 4)
        assert osm_reader.settings.lane_configuration.get_default_directional_lanes_by_highway_type("primary") is 4
        osm_reader.settings.lane_configuration.set_default_directional_railway_tracks(2)
        assert osm_reader.settings.lane_configuration.get_default_directional_railway_tracks() is 2
        assert osm_reader.settings.lane_configuration.get_default_directional_waterway_lanes() > 0

        # ensure PLANit connection is reset
        planit.force_stop_java()
        gc.collect()

    def test_converter_osm_reader_all_properties(self):
        # no correspondence to Java test as we explicitly test non-failure of Python code to test all properties
        # are accessible on the OSM reader based on the documentation
        planit = Planit()

        # OSM reader
        osm_reader: OsmIntermodalReaderWrapper = planit.converter_factory.create(
            ConverterType.INTERMODAL).create_reader(
            IntermodalReaderType.OSM, AUSTRALIA)

        pt_settings = osm_reader.settings.pt_settings
        pt_settings.exclude_osm_nodes_by_id([1234, 5678])
        pt_settings.exclude_osm_ways_by_id([1234, 5678])
        pt_settings.overwrite_waiting_area_of_stop_location(1234, OsmEntityType.WAY, 56789)
        assert pt_settings.is_overwrite_waiting_area_of_stop_location(1234) is True
        pt_settings.overwrite_waiting_area_nominated_osm_way_for_stop_location(
            1234, OsmEntityType.WAY, 56789)  # changed in v0.4.0
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

        # v0.4.0
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
        assert round(pt_settings.get_ferry_stop_to_ferry_route_search_radius_meters(), 0) == 40
        pt_settings.overwrite_waiting_area_mode_access(1234, OsmEntityType.WAY, ["tram"])
        assert "tram" in pt_settings.get_overwritten_waiting_area_mode_access(1234, OsmEntityType.WAY)

        # ensure planit connection is reset
        planit.force_stop_java()
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
        zoning_settings: GtfsZoningReaderSettingsWrapper = gtfs_reader.settings.zoning_settings
        zoning_settings.set_gtfs_stop_to_transfer_zone_search_radius_meters(40)
        assert round(zoning_settings.get_gtfs_stop_to_transfer_zone_search_radius_meters(), 0) == 40
        zoning_settings.set_gtfs_stop_to_link_search_radius_meters(20)
        assert round(zoning_settings.get_gtfs_stop_to_link_search_radius_meters(), 0) == 20
        zoning_settings.add_overwrite_gtfs_stop_transfer_zone_mapping(
            "gtfs_Stop_id", "planit_transfer_zone_id", IdMapperType.XML)
        assert zoning_settings.is_overwritten_gtfs_stop_transfer_zone_mapping("gtfs_Stop_id") is True
        zoning_settings.add_overwrite_gtfs_stop_transfer_zone_mapping(
            "gtfs_Stop_id", "planit_transfer_zone_id_other", IdMapperType.XML)
        mappings: List[Tuple[Union[int, str], IdMapperType]] = \
            zoning_settings.get_overwritten_gtfs_stop_transfer_zone_mapping("gtfs_Stop_id")
        assert len(mappings) == 2
        zoning_settings.set_overwrite_gtfs_stop_location(
            "a_gtfs_stop_id", 33.33, 148.148)  # lat/lon
        assert zoning_settings.is_overwritten_gtfs_stop_location("a_gtfs_stop_id") is True
        lat_lon: Tuple[float, float] = zoning_settings.get_overwritten_gtfs_stop_location("a_gtfs_stop_id")
        assert round(lat_lon[0], 2) == 33.33
        assert round(lat_lon[1], 3) == 148.148
        zoning_settings.set_log_mapped_gtfs_zones(True)
        assert zoning_settings.is_log_mapped_gtfs_zones() is True
        zoning_settings.set_log_created_gtfs_zones(True)
        assert zoning_settings.is_log_created_gtfs_zones() is True
        zoning_settings.activate_extended_logging_for_gtfs_zones(["gtfs_stop_id_1", "gtfs_stop_id_2"])
        assert zoning_settings.is_extended_logging_for_gtfs_zone_activated("gtfs_stop_id_1") is True
        assert zoning_settings.is_extended_logging_for_gtfs_zone_activated("gtfs_stop_id_2") is True
        zoning_settings.set_remove_unused_transfer_zones(True)
        assert zoning_settings.is_remove_unused_transfer_zones() is True
        zoning_settings.exclude_gtfs_stops_by_id(["gtfs_stop_id_3", "gtfs_stop_id_4"])
        zoning_settings.exclude_gtfs_stop_by_id("gtfs_stop_id_5")
        assert zoning_settings.is_excluded_gtfs_stop("gtfs_stop_id_5") is True
        assert zoning_settings.is_excluded_gtfs_stop("gtfs_stop_id_3") is True
        assert zoning_settings.is_excluded_gtfs_stop("gtfs_stop_id_4") is True
        assert zoning_settings.is_excluded_gtfs_stop("gtfs_stop_id_6") is False
        zoning_settings.overwrite_gtfs_stop_to_link_mapping(
            "gtfs_stop_id_3", "planit_link_external_osm_id", IdMapperType.EXTERNAL_ID)
        assert zoning_settings.has_overwritten_gtfs_stop_to_link_mapping("gtfs_stop_id_3") is True
        overwritten_mapping: Tuple[Union[int, str], IdMapperType] = \
            zoning_settings.get_overwritten_gtfs_stop_to_link_mapping("gtfs_stop_id_3")
        assert overwritten_mapping[0] == "planit_link_external_osm_id"
        assert overwritten_mapping[1] is IdMapperType.EXTERNAL_ID
        zoning_settings.add_log_gtfs_stop_to_link_mapping(["gtfs_stop_id_7", "gtfs_stop_id_8"])
        assert zoning_settings.is_log_gtfs_stop_to_link_mapping("gtfs_stop_id_1") is False
        assert zoning_settings.is_log_gtfs_stop_to_link_mapping("gtfs_stop_id_7") is True
        assert zoning_settings.is_log_gtfs_stop_to_link_mapping("gtfs_stop_id_8") is True
        zoning_settings.disallow_gtfs_stop_to_transfer_zone_joint_mapping(["gtfs_stop_id_9", "gtfs_stop_id_10"])
        assert zoning_settings.is_disallow_gtfs_stop_to_transfer_zone_joint_mapping("gtfs_stop_id_9") is True
        assert zoning_settings.is_disallow_gtfs_stop_to_transfer_zone_joint_mapping("gtfs_stop_id_10") is True
        assert zoning_settings.is_disallow_gtfs_stop_to_transfer_zone_joint_mapping("gtfs_stop_id_11") is False
        zoning_settings.force_create_new_transfer_zone_for_gtfs_stops(["gtfs_stop_id_11", "gtfs_stop_id_12"])
        assert zoning_settings.is_force_create_new_transfer_zone_for_gtfs_stop("gtfs_stop_id_11") is True
        assert zoning_settings.is_force_create_new_transfer_zone_for_gtfs_stop("gtfs_stop_id_12") is True
        assert zoning_settings.is_force_create_new_transfer_zone_for_gtfs_stop("gtfs_stop_id_13") is False

        # (transfer) zoning settings - new in v0.4.0
        services_settings = gtfs_reader.settings.services_settings
        services_settings.exclude_all_gtfs_routes_except_by_short_name(["431", "433"])
        assert services_settings.is_gtfs_route_included_by_short_name("431") is True
        assert services_settings.is_gtfs_route_included_by_short_name("433") is True
        assert services_settings.is_gtfs_route_included_by_short_name("469") is False
        services_settings.exclude_gtfs_routes_by_short_name(["433"])
        assert services_settings.is_gtfs_route_included_by_short_name("433") is False
        services_settings.activate_logging_for_gtfs_route_by_short_name("438x")
        assert services_settings.is_activated_logging_for_gtfs_route_by_short_name("438x") is True
        assert services_settings.is_activated_logging_for_gtfs_route_by_short_name("438") is False

        services_settings.add_time_period_filter(
            datetime.time(hour=6, minute=0, second=0),
            datetime.time(hour=9, minute=59, second=59)
        )
        time_period_filters: Set[Tuple[datetime.time, datetime.time]] = services_settings.get_time_period_filters()
        assert len(time_period_filters) == 1
        time_period_filter = time_period_filters.pop()
        assert time_period_filter[0].hour == 6
        assert time_period_filter[0].minute == 0
        assert time_period_filter[0].second == 0
        assert time_period_filter[1].hour == 9
        assert time_period_filter[1].minute == 59
        assert time_period_filter[1].second == 59

        services_settings.day_of_week = DayOfWeek.THURSDAY
        assert gtfs_reader.settings.services_settings.day_of_week == DayOfWeek.THURSDAY

        services_settings.set_group_identical_gtfs_trips(False)
        assert services_settings.is_group_identical_gtfs_trips() is False
        services_settings.set_include_partial_gtfs_trips_if_stops_in_time_period(False)
        assert services_settings.is_include_partial_gtfs_trips_if_stops_in_time_period() is False
        services_settings.add_log_gtfs_stop_routes(["gtfs_stop_x", "gtfs_stop_y"])
        assert services_settings.is_log_gtfs_stop_route("gtfs_stop_x") is True
        assert services_settings.is_log_gtfs_stop_route("gtfs_stop_y") is True
        assert services_settings.is_log_gtfs_stop_route("gtfs_stop_z") is False

        planit.force_stop_java()
        gc.collect()

    def test_converter_matsim_writer_all_properties(self):
        OUTPUT_PATH = os.path.join(OSM_PATH, 'output', 'matsim')

        # no correspondence to Java test as we explicitly test non-failure of Python code to test all properties
        # are accessible on the OSM reader based on the documentation
        planit = Planit()

        # matsim writer
        matsim_writer: MatsimIntermodalWriterWrapper = planit.converter_factory.create(
            ConverterType.INTERMODAL).create_writer(IntermodalWriterType.MATSIM)

        # v0.4.0
        matsim_writer.set_id_mapper_type(IdMapperType.XML)
        assert matsim_writer.get_id_mapper_type() is IdMapperType.XML

        # general
        matsim_writer.settings.set_output_directory(OUTPUT_PATH)
        matsim_writer.settings.set_country(AUSTRALIA)
        matsim_writer.settings.set_file_name("my_network")

        # network specific
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
        planit.force_stop_java()
        gc.collect()

    def test_converter_geoio_writer_all_properties(self):
        OUTPUT_PATH = os.path.join(OSM_PATH, 'output', 'geoio')

        # no correspondence to Java test as we explicitly test non-failure of Python code to test all properties
        # are accessible on the OSM reader based on the documentation
        planit = Planit()

        # geo writer
        geoio_writer: GeometryIntermodalWriterWrapper = planit.converter_factory.create(
            ConverterType.INTERMODAL).create_writer(IntermodalWriterType.SHAPE)
        geoio_writer.settings.set_output_directory(OUTPUT_PATH)
        geoio_writer.settings.set_country(AUSTRALIA)

        ########
        # Network settings
        network_settings = geoio_writer.settings.network_settings
        network_settings.set_persist_links(False)
        assert network_settings.is_persist_links() is False
        network_settings.set_persist_nodes(False)
        assert network_settings.is_persist_nodes() is False
        # todo: add support for persisting link segments on/off
        network_settings.set_links_file_name("links_file_name")
        assert network_settings.get_links_file_name() == "links_file_name"
        network_settings.set_nodes_file_name("nodes_file_name")
        assert network_settings.get_nodes_file_name() == "nodes_file_name"

        ########
        # Zoning settings
        zoning_settings = geoio_writer.settings.zoning_settings

        zoning_settings.set_persist_virtual_network(True)
        assert zoning_settings.is_persist_virtual_network() is True

        zoning_settings.set_persist_od_zones(False)
        assert zoning_settings.is_persist_od_zones() is False
        zoning_settings.set_persist_transfer_zones(False)
        assert zoning_settings.is_persist_transfer_zones() is False
        zoning_settings.set_od_zones_file_name("od_file_name")
        assert zoning_settings.get_od_zones_file_name() == "od_file_name"
        zoning_settings.set_transfer_zones_file_name("transfer_file_name")
        assert zoning_settings.get_transfer_zones_file_name() == "transfer_file_name"

        zoning_settings.set_persist_od_connectoids(False)
        assert zoning_settings.is_persist_od_connectoids() is False
        zoning_settings.set_persist_transfer_connectoids(False)
        assert zoning_settings.is_persist_transfer_connectoids() is False
        zoning_settings.set_od_connectoids_file_name("odc_file_name")
        assert zoning_settings.get_od_connectoids_file_name() == "odc_file_name"
        zoning_settings.set_transfer_connectoids_file_name("transferc_file_name")
        assert zoning_settings.get_transfer_connectoids_file_name() == "transferc_file_name"

        zoning_settings.set_connectoid_edges_file_name("conn_edges_file_name")
        assert zoning_settings.get_connectoid_edges_file_name() == "conn_edges_file_name"
        zoning_settings.set_connectoid_segments_file_name("connectoid_seg_file_name")
        assert zoning_settings.get_connectoid_segments_file_name() == "connectoid_seg_file_name"

        ########
        # Service network settings
        service_network_settings = geoio_writer.settings.service_network_settings
        service_network_settings.set_persist_service_legs(False)
        assert service_network_settings.is_persist_service_legs() is False
        service_network_settings.set_persist_service_nodes(False)
        assert service_network_settings.is_persist_service_nodes() is False
        service_network_settings.set_persist_service_leg_segments(False)
        assert service_network_settings.is_persist_service_leg_segments() is False
        service_network_settings.set_service_legs_file_name("sl_file_name")
        assert service_network_settings.get_service_legs_file_name() == "sl_file_name"
        service_network_settings.set_service_leg_segments_file_name("sls_file_name")
        assert service_network_settings.get_service_leg_segments_file_name() == "sls_file_name"
        service_network_settings.set_service_nodes_file_name("sn_file_name")
        assert service_network_settings.get_service_nodes_file_name() == "sn_file_name"

        ########
        # Routed Services  settings
        routed_services_settings = geoio_writer.settings.routed_services_settings
        routed_services_settings.set_persist_services(False)
        assert routed_services_settings.is_persist_services() is False
        routed_services_settings.set_persist_trips_schedule(False)
        assert routed_services_settings.is_persist_trips_schedule() is False
        routed_services_settings.set_persist_trips_frequency(False)
        assert routed_services_settings.is_persist_trips_frequency() is False
        routed_services_settings.set_services_file_name("s_file_name")
        assert routed_services_settings.get_services_file_name() == "s_file_name"
        routed_services_settings.set_trips_schedule_file_name("ts_file_name")
        assert routed_services_settings.get_trips_schedule_file_name() == "ts_file_name"
        routed_services_settings.set_trips_frequency_file_name("tf_file_name")
        assert routed_services_settings.get_trips_frequency_file_name() == "tf_file_name"

        # ensure planit connection is reset
        planit.force_stop_java()
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
        planit_writer.settings.service_network_settings.set_output_directory(OUTPUT_PATH)
        planit_writer.settings.service_network_settings.set_file_name("service_network.xml")

        # routed services settings
        planit_writer.settings.routed_services_settings.set_output_directory(OUTPUT_PATH)
        planit_writer.settings.routed_services_settings.set_file_name("routed_services.xml")
        planit_writer.settings.routed_services_settings.set_log_services_without_trips(False)
        # not yet documented/supported
        # planit_writer.settings.routed_services_settings.set_trip_frequency_time_unit(...)

        # ensure planit connection is reset
        planit.force_stop_java()
        gc.collect()

    if __name__ == '__main__':
        unittest.main()

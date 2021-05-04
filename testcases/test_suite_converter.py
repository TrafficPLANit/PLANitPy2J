import os, sys   
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),'..','src'))

import gc
import unittest
import math
from test_utils import PlanItHelper
from planit import *

class TestSuiteConverter(unittest.TestCase):
    """ We are testing here if conversions are runnable. We do not actually test the validity of the results
        as this is being done on the Java side. Here, we just make sure the properties can be set as expected and
        the run does not yield any errors/exceptions
    """
    
    def test_network_converter_osm_reader_all_properties(self):
        OSM_PATH = os.path.join('converter', 'osm')
        INPUT_PATH = os.path.join(OSM_PATH, 'input')
        COUNTRY = "Australia"
        FULL_INPUT_FILE_NAME = os.path.join(INPUT_PATH, "sydneycbd.osm.pbf")
        
        # no correspondence to Java test as we explicitly test non-failure of Python code to test all properties
        # are accessible on the OSM reader based on the documentation
        plan_it = Planit()
        
        # network converter
        network_converter = plan_it.converter_factory.create(ConverterType.NETWORK)
        
        # osm reader        
        osm_reader = network_converter.create_reader(NetworkReaderType.OSM, COUNTRY)
        
        # global settings
        osm_reader.settings.activate_highway_parser(True)
        osm_reader.settings.activate_railway_parser(True)        
        osm_reader.settings.deactivate_all_osm_way_types_except(["primary"])
        osm_reader.settings.exclude_osm_ways_from_parsing([12345])
        osm_reader.settings.overwrite_mode_access_by_osm_way_id(123,["foot"])
        osm_reader.settings.set_always_keep_largest_subnetwork(True)
        osm_reader.settings.set_discard_dangling_networks_above(20)
        osm_reader.settings.set_discard_dangling_networks_below(10)
        osm_reader.settings.set_input_file(FULL_INPUT_FILE_NAME)
        osm_reader.settings.set_remove_dangling_subnetworks(True)
        
        # highway settings
        osm_reader.settings.highway_settings.activate_all_osm_highway_types()
        osm_reader.settings.highway_settings.activate_osm_highway_types(["primary"])
        osm_reader.settings.highway_settings.add_allowed_highway_modes("primary",["bus","foot"])
        osm_reader.settings.highway_settings.deactivate_all_road_modes_except(["bus"])
        osm_reader.settings.highway_settings.deactivate_all_osm_highway_types_except(["primary"])
        osm_reader.settings.highway_settings.deactivate_road_modes(["bus"])
        osm_reader.settings.highway_settings.deactivate_osm_highway_type("primary")
        osm_reader.settings.highway_settings.set_default_when_osm_highway_type_unsupported("primary")
        osm_reader.settings.highway_settings.overwrite_capacity_max_density_defaults("primary", 2000, 150)
        osm_reader.settings.highway_settings.remove_osm_road_mode_planit_mode_mapping(["motorcar"])
        osm_reader.settings.highway_settings.set_speed_limit_defaults_based_on_urban_area(True)
        
        # railway settings
        osm_reader.settings.railway_settings.activate_all_osm_railway_types()
        osm_reader.settings.railway_settings.activate_osm_railway_types(["rail","funicular"])
        osm_reader.settings.railway_settings.deactivate_all_osm_railway_types()
        osm_reader.settings.railway_settings.deactivate_all_osm_railway_types_except(["rail","monorail"])
        osm_reader.settings.railway_settings.deactivate_all_rail_modes_except(["train","tram"])
        osm_reader.settings.railway_settings.deactivate_osm_railway_type("rail")
        osm_reader.settings.railway_settings.deactivate_rail_modes(["train","subway"])
        osm_reader.settings.railway_settings.overwrite_capacity_max_density_defaults("rail",100000,100)
        osm_reader.settings.railway_settings.remove_osm_rail_mode_planit_mode_mapping(["train","subway"])
        
        # lane configuration
        osm_reader.settings.lane_configuration.set_default_directional_lanes_by_highway_type("primary",4)
        osm_reader.settings.lane_configuration.set_default_directional_railway_tracks(2)
    
    def test_network_converter_osm2matsim(self):
        OSM_PATH = os.path.join('converter', 'osm')
        INPUT_PATH = os.path.join(OSM_PATH, 'input')
        OUTPUT_PATH = os.path.join(OSM_PATH, 'output','matsim')
        COUNTRY = "Australia"
        FULL_INPUT_FILE_NAME = os.path.join(INPUT_PATH, "sydneycbd.osm.pbf")
        
        # no correspondence to Java test as we explicitly test non-failure of Python code to instantiate converters
        plan_it = Planit()
        
        # network converter
        network_converter = plan_it.converter_factory.create(ConverterType.NETWORK)
        
        # osm reader        
        osm_reader = network_converter.create_reader(NetworkReaderType.OSM, COUNTRY)
        osm_reader.settings.set_input_file(FULL_INPUT_FILE_NAME)
        
        #matsim writer
        matsim_writer = network_converter.create_writer(NetworkWriterType.MATSIM)
        matsim_writer.settings.set_output_directory(OUTPUT_PATH)
        matsim_writer.settings.set_country(COUNTRY)
        
        # perform conversion
        network_converter.convert(osm_reader,matsim_writer)
        gc.collect() 
        
    def test_network_converter_osm2planit(self):
        OSM_PATH = os.path.join('converter', 'osm')
        INPUT_PATH = os.path.join(OSM_PATH, 'input')
        OUTPUT_PATH = os.path.join(OSM_PATH, 'output','planit')
        COUNTRY = "Australia"
        FULL_INPUT_FILE_NAME = os.path.join(INPUT_PATH, "sydneycbd.osm.pbf")
        
        # no correspondence to Java test as we explicitly test non-failure of Python code to instantiate converters
        plan_it = Planit()
        
        # network converter
        network_converter = plan_it.converter_factory.create(ConverterType.NETWORK)
        
        # osm reader        
        osm_reader = network_converter.create_reader(NetworkReaderType.OSM, COUNTRY)
        osm_reader.settings.set_input_file(FULL_INPUT_FILE_NAME)
        
        #planit writer
        planit_writer = network_converter.create_writer(NetworkWriterType.PLANIT)
        planit_writer.settings.set_output_directory(OUTPUT_PATH)
        planit_writer.settings.set_country(COUNTRY)
        
        # perform conversion
        network_converter.convert(osm_reader,planit_writer)
        gc.collect()   
      
    def test_intermodal_converter_osm2matsim(self):
        OSM_PATH = os.path.join('converter', 'osm')
        INPUT_PATH = os.path.join(OSM_PATH, 'input')
        OUTPUT_PATH = os.path.join(OSM_PATH, 'output','matsim')
        COUNTRY = "Australia"
        FULL_INPUT_FILE_NAME = os.path.join(INPUT_PATH, "sydneycbd.osm.pbf")
        
        # no correspondence to Java test as we explicitly test non-failure of Python code to instantiate converters
        plan_it = Planit()
        
        # network converter
        intermodal_converter = plan_it.converter_factory.create(ConverterType.INTERMODAL)
        
        # osm reader        
        osm_reader = intermodal_converter.create_reader(IntermodalReaderType.OSM, COUNTRY)
        osm_reader.settings.set_input_file(FULL_INPUT_FILE_NAME)
        
        #matsim writer
        matsim_writer = intermodal_converter.create_writer(IntermodalWriterType.MATSIM)
        # test if setting country and output path via separate settings works
        matsim_writer.settings.network_settings.set_output_directory(OUTPUT_PATH)
        matsim_writer.settings.network_settings.set_country(COUNTRY)
        matsim_writer.settings.zoning_settings.set_output_directory(OUTPUT_PATH)
        matsim_writer.settings.zoning_settings.set_country(COUNTRY)
        # test if setting country and output path via intermodal settings directly works
        matsim_writer.settings.set_output_directory(OUTPUT_PATH)
        matsim_writer.settings.set_country(COUNTRY) 
        
        # perform conversion
        intermodal_converter.convert(osm_reader,matsim_writer)
        gc.collect() 
    
        
    def test_intermodal_converter_osm2planit(self):
        OSM_PATH = os.path.join('converter', 'osm')
        INPUT_PATH = os.path.join(OSM_PATH, 'input')
        OUTPUT_PATH = os.path.join(OSM_PATH, 'output','planit')
        COUNTRY = "Australia"
        FULL_INPUT_FILE_NAME = os.path.join(INPUT_PATH, "sydneycbd.osm.pbf")
        
        # no correspondence to Java test as we explicitly test non-failure of Python code to instantiate converters
        plan_it = Planit()
        
        # network converter
        intermodal_converter = plan_it.converter_factory.create(ConverterType.INTERMODAL)
        
        # osm reader        
        osm_reader = intermodal_converter.create_reader(IntermodalReaderType.OSM, COUNTRY)
        osm_reader.settings.set_input_file(FULL_INPUT_FILE_NAME)
        
        #planit writer
        planit_writer = intermodal_converter.create_writer(IntermodalWriterType.PLANIT)
        # test if setting country and output path via separate settings works
        planit_writer.settings.network_settings.set_output_directory(OUTPUT_PATH)
        planit_writer.settings.zoning_settings.set_output_directory(OUTPUT_PATH)
        planit_writer.settings.zoning_settings.set_country(COUNTRY)
        # test if setting country and output path via intermodal settings directly works
        planit_writer.settings.set_output_directory(OUTPUT_PATH)
        planit_writer.settings.set_country(COUNTRY) 
        
        # perform conversion
        intermodal_converter.convert(osm_reader,planit_writer)
        gc.collect()  
        
    def test_network_converter_planit2planit(self):
        PLANIT_PATH = os.path.join('converter', 'planit')
        INPUT_PATH = os.path.join(PLANIT_PATH, 'input')
        OUTPUT_PATH = os.path.join(PLANIT_PATH, 'output','planit')
        COUNTRY = "Australia"
        
        # no correspondence to Java test as we explicitly test non-failure of Python code to instantiate converters
        plan_it = Planit()
        
        # network converter
        network_converter = plan_it.converter_factory.create(ConverterType.NETWORK)
        
        # planit reader        
        planit_reader = network_converter.create_reader(NetworkReaderType.PLANIT)
        planit_reader.settings.set_input_directory(INPUT_PATH)
        
        #planit writer
        planit_writer = network_converter.create_writer(NetworkWriterType.PLANIT)
        planit_writer.settings.set_output_directory(OUTPUT_PATH)
        planit_writer.settings.set_country(COUNTRY)
        
        # perform conversion
        network_converter.convert(planit_reader,planit_writer)
        # result should be the same file, although we do not test this here automatically yet
        gc.collect()  
        
    def test_intermodal_converter_planit2planit(self):
        PLANIT_PATH = os.path.join('converter', 'planit')
        INPUT_PATH = os.path.join(PLANIT_PATH, 'input')
        OUTPUT_PATH = os.path.join(PLANIT_PATH, 'output','planit')
        COUNTRY = "Australia"
        
        # no correspondence to Java test as we explicitly test non-failure of Python code to instantiate converters
        plan_it = Planit()
        
        # network converter
        intermodal_converter = plan_it.converter_factory.create(ConverterType.INTERMODAL)
        
        # planit reader        
        planit_reader = intermodal_converter.create_reader(IntermodalReaderType.PLANIT)
        planit_reader.settings.set_input_directory(INPUT_PATH)
        
        #planit writer
        planit_writer = intermodal_converter.create_writer(IntermodalWriterType.PLANIT)
        # test if setting country and output path via separate settings works
        planit_writer.settings.network_settings.set_output_directory(OUTPUT_PATH)
        planit_writer.settings.zoning_settings.set_output_directory(OUTPUT_PATH)
        planit_writer.settings.zoning_settings.set_country(COUNTRY)
        # test if setting country and output path via intermodal settings directly works
        planit_writer.settings.set_output_directory(OUTPUT_PATH)
        planit_writer.settings.set_country(COUNTRY) 
        
        # perform conversion
        intermodal_converter.convert(planit_reader,planit_writer)
        gc.collect()
                 
    if __name__ == '__main__':
        unittest.main()
    
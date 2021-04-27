import os, sys   
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),'..','src'))

import gc
import unittest
import math
from test_utils import PlanItHelper
from planit import *

class TestSuiteConverter(unittest.TestCase):
    
    def test_network_converter_osm2matsim(self):
        INPUT_PATH = os.path.join('converter', 'osm')
        OUTPUT_PATH = os.path.join(INPUT_PATH, 'matsim')
        COUNTRY = "Australia"
        FULL_INPUT_FILE_NAME = os.path.join(INPUT_PATH, "sydneycbd.osm.pbf")
        
        # no correspondence to Java test as we explicitly test non-failure of Python code to instantiate converters
        plan_it = Planit()
        
        # network converter
        converter_factory = plan_it.converterFactory
        network_converter = converter_factory.create(ConverterType.NETWORK)
        
        # osm reader        
        osm_reader = network_converter.create_reader(NetworkReaderType.OSM, COUNTRY)
        osm_reader.settings.set_input_file(FULL_INPUT_FILE_NAME)
        
        #matsim writer
        osm_writer = network_converter.create_writer(NetworkWriterType.MATSIM)
        osm_writer.settings.set_output_directory(OUTPUT_PATH)
        osm_writer.settings.set_country(COUNTRY)
        
        # perform conversion
        network_converter.convert(osm_reader,osm_writer)
        gc.collect()   
        
    def test_intermodal_converter_osm2matsim(self):
        INPUT_PATH = os.path.join('converter', 'osm')
        OUTPUT_PATH = os.path.join(INPUT_PATH, 'matsim')
        COUNTRY = "Australia"
        FULL_INPUT_FILE_NAME = os.path.join(INPUT_PATH, "sydneycbd.osm.pbf")
        
        # no correspondence to Java test as we explicitly test non-failure of Python code to instantiate converters
        plan_it = Planit()
        
        # network converter
        converter_factory = plan_it.converterFactory
        intermodal_converter = converter_factory.create(ConverterType.INTERMODAL)
        
        # osm reader        
        osm_reader = intermodal_converter.create_reader(IntermodalReaderType.OSM, COUNTRY)
        osm_reader.network_settings.set_input_file(FULL_INPUT_FILE_NAME)
        
        #matsim writer
        osm_writer = intermodal_converter.create_writer(IntermodalWriterType.MATSIM)
        osm_writer.network_settings.set_output_directory(OUTPUT_PATH)
        osm_writer.network_settings.set_country(COUNTRY)
        
        # perform conversion
        intermodal_converter.convert(osm_reader,osm_writer)
        gc.collect()  
              
if __name__ == '__main__':
    unittest.main()
    
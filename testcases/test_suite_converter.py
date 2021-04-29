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
    
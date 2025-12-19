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

GEOIO_PATH = os.path.join(ABSOLUTE_PATH_TEST_DATA_CONVERTER, 'geoio')

PLANIT_PATH = os.path.join(ABSOLUTE_PATH_TEST_DATA_CONVERTER, 'planit')
PLANIT_INPUT_PATH = os.path.join(PLANIT_PATH, 'input')


class TestSuiteConverterPlanit(unittest.TestCase):
    """ We are testing here if planit_conversions are runnable. We do not actually test the validity of the results
        as this is being done on the Java side. Here, we just make sure the properties can be set as expected and
        the run does not yield any errors/exceptions
    """

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
        geo_writer = intermodal_converter.create_writer(IntermodalWriterType.SHAPE)
        geo_writer.settings.set_output_directory(OUTPUT_PATH)
        geo_writer.settings.set_country(AUSTRALIA)
        geo_writer.settings.network_settings.set_persist_nodes(True)
        geo_writer.settings.network_settings.set_persist_links(True)

        geo_writer.settings.zoning_settings.persist_virtual_network = True
        geo_writer.set_id_mapper_type(IdMapperType.XML)

        # perform conversion
        intermodal_converter.convert_with_services(planit_reader, geo_writer)

        planit.force_stop_java()
        gc.collect()

    def test_network_converter_planit2planit(self):
        OUTPUT_PATH = os.path.join(PLANIT_PATH, 'output', 'planit')

        # no correspondence to Java test as we explicitly test non-failure of Python code to instantiate converters
        planit = Planit()

        # network converter
        network_converter = planit.converter_factory.create(ConverterType.NETWORK)

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

        planit.force_stop_java()
        gc.collect()

    def test_zoning_converter_planit2planit(self):
        OUTPUT_PATH = os.path.join(PLANIT_PATH, 'output', 'planit')

        # no correspondence to Java test as we explicitly test non-failure of Python code to instantiate converters
        planit = Planit()

        planit_net_reader: PlanitNetworkReaderWrapper = \
            planit.converter_factory.create(ConverterType.NETWORK).create_reader(NetworkReaderType.PLANIT)
        planit_net_reader.settings.set_input_directory(PLANIT_INPUT_PATH)

        # zoning converter
        converter: ZoningConverter = planit.converter_factory.create(ConverterType.ZONING)

        # PLANit reader
        planit_zon_reader: PlanitZoningReaderWrapper = (
            converter.create_reader(ZoningReaderType.PLANIT, planit_net_reader))
        planit_zon_reader.settings.set_input_directory(PLANIT_INPUT_PATH)

        # PLANit writer
        planit_writer: PlanitZoningWriterWrapper = converter.create_writer(ZoningWriterType.PLANIT)
        planit_writer.settings.set_output_directory(OUTPUT_PATH)
        planit_writer.settings.set_country(AUSTRALIA)

        # perform conversion
        converter.convert(planit_zon_reader, planit_writer)
        # result should be the same file, although we do not test this here automatically yet

        planit.force_stop_java()
        gc.collect()

    def test_intermodal_converter_planit2planit(self):
        OUTPUT_PATH = os.path.join(PLANIT_PATH, 'output', 'planit')

        # no correspondence to Java test as we explicitly test non-failure of Python code to instantiate converters
        planit = Planit()

        # network converter
        intermodal_converter = planit.converter_factory.create(ConverterType.INTERMODAL)

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

        # perform planit_conversions, test that running conversion twice does not cause problems
        intermodal_converter.convert(planit_reader, planit_writer)
        intermodal_converter.convert_with_services(planit_reader, planit_writer)

        planit.force_stop_java()
        gc.collect()

    if __name__ == '__main__':
        unittest.main()

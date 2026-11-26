import os
import sys
import time
from pathlib import Path
from typing import List

from py4j.java_gateway import JavaObject

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

SETTINGS_PATH = os.path.join(ABSOLUTE_PATH, '..', 'conversion_properties', 'settings')
PLANIT_READER_SETTINGS_FILE_PATH = os.path.join(SETTINGS_PATH, "planit_reader_input.yaml")
PLANIT_INTERMODAL_READER_SETTINGS_FILE_PATH = os.path.join(SETTINGS_PATH, "planit_intermodal_reader.yaml")
PLANIT_WRITER_SETTINGS_FILE_PATH = os.path.join(SETTINGS_PATH, "planit_writer_output.yaml")
PLANIT_INTERMODAL_WRITER_SETTINGS_FILE_PATH = os.path.join(SETTINGS_PATH, "planit_intermodal_writer.yaml")
MATSIM_INTERMODAL_WRITER_SETTINGS_FILE_PATH = os.path.join(SETTINGS_PATH, "matsim_intermodal_writer.yaml")


def written_since(java_writer_settings: List[JavaObject], start_time: float) -> bool:
    """ whether the file each PLANit writer's settings name, in their output directory, was written since the given time
    :param java_writer_settings: of PLANit writers of one file each, giving the output directory and the file name
    :param start_time: in seconds since the epoch
    :return true when each was written since
    """
    return all(os.path.getmtime(os.path.join(settings.getOutputDirectory(), settings.getFileName())) >= start_time
               for settings in java_writer_settings)


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

    def test_intermodal_converter_with_services_planit2geoio_from_settings_file(self) -> None:
        OUTPUT_PATH = os.path.join(PLANIT_PATH, 'output', 'geoio')

        planit = Planit()

        # intermodal converter
        intermodal_converter = planit.converter_factory.create(ConverterType.INTERMODAL)

        # PLANit reader, made from a settings file naming the file of each of its nested settings
        planit_reader = intermodal_converter.create_yaml_based_reader(
            IntermodalReaderType.PLANIT, PLANIT_INTERMODAL_READER_SETTINGS_FILE_PATH)

        # GeoIo (GIS geometry shape) writer
        geo_writer = intermodal_converter.create_writer(IntermodalWriterType.SHAPE)
        geo_writer.settings.set_output_directory(OUTPUT_PATH)
        geo_writer.settings.set_country(AUSTRALIA)

        # perform conversion
        intermodal_converter.convert_with_services(planit_reader, geo_writer)

        planit.force_stop_java()
        gc.collect()

    def test_intermodal_converter_with_services_planit2matsim_from_settings_file(self) -> None:
        start_time = time.time()
        planit = Planit()

        intermodal_converter = planit.converter_factory.create(ConverterType.INTERMODAL)

        # PLANit reader and MATSim writer, each made from a settings file naming the file of each of its nested settings
        planit_reader = intermodal_converter.create_yaml_based_reader(
            IntermodalReaderType.PLANIT, PLANIT_INTERMODAL_READER_SETTINGS_FILE_PATH)
        matsim_writer = intermodal_converter.create_yaml_based_writer(
            IntermodalWriterType.MATSIM, MATSIM_INTERMODAL_WRITER_SETTINGS_FILE_PATH)

        # perform conversion
        intermodal_converter.convert_with_services(planit_reader, matsim_writer)

        # the network and the transit schedule are written to the files the settings name, not gzipped as they ask
        java_settings = matsim_writer.java.getSettings()
        for part_settings in [java_settings.getNetworkSettings(), java_settings.getPtServicesSettings()]:
            written_file = os.path.join(part_settings.getOutputDirectory(), part_settings.getFileName() + ".xml")
            assert os.path.getmtime(written_file) >= start_time, written_file

        planit.force_stop_java()
        gc.collect()

    def test_zoning_converter_planit2planit_from_settings_files(self) -> None:
        start_time = time.time()
        planit = Planit()

        planit_net_reader = planit.converter_factory.create(ConverterType.NETWORK).create_yaml_based_reader(
            NetworkReaderType.PLANIT, PLANIT_READER_SETTINGS_FILE_PATH)

        # zoning converter
        converter: ZoningConverter = planit.converter_factory.create(ConverterType.ZONING)
        planit_zon_reader = converter.create_yaml_based_reader(
            ZoningReaderType.PLANIT, PLANIT_READER_SETTINGS_FILE_PATH, planit_net_reader)

        # PLANit writer made before anything is read; the converter gives it the network the reader read
        planit_writer = converter.create_yaml_based_writer(ZoningWriterType.PLANIT, PLANIT_WRITER_SETTINGS_FILE_PATH)

        # perform conversion
        converter.convert(planit_zon_reader, planit_writer)
        assert written_since([planit_writer.java.getSettings()], start_time)

        planit.force_stop_java()
        gc.collect()

    def test_intermodal_converter_planit2planit_from_settings_files(self) -> None:
        start_time = time.time()
        planit = Planit()

        intermodal_converter = planit.converter_factory.create(ConverterType.INTERMODAL)

        # PLANit reader and writer, each made from a settings file naming the file of each of its nested settings
        planit_reader = intermodal_converter.create_yaml_based_reader(
            IntermodalReaderType.PLANIT, PLANIT_INTERMODAL_READER_SETTINGS_FILE_PATH)
        planit_writer = intermodal_converter.create_yaml_based_writer(
            IntermodalWriterType.PLANIT, PLANIT_INTERMODAL_WRITER_SETTINGS_FILE_PATH)

        # perform conversion
        intermodal_converter.convert_with_services(planit_reader, planit_writer)
        java_settings = planit_writer.java.getSettings()
        assert written_since([java_settings.getNetworkSettings(), java_settings.getZoningSettings(),
                              java_settings.getServiceNetworkSettings(), java_settings.getRoutedServicesSettings()],
                             start_time)

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

    def test_intermodal_converter_planit2planit(self) -> None:
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

        # perform planit_conversions, test that the same writer converts twice without problems; a reader reads once,
        # filling the network it was made with, so the second conversion takes a new one
        intermodal_converter.convert(planit_reader, planit_writer)
        services_reader = intermodal_converter.create_reader(IntermodalReaderType.PLANIT)
        services_reader.settings.set_input_directory(PLANIT_INPUT_PATH)
        intermodal_converter.convert_with_services(services_reader, planit_writer)

        planit.force_stop_java()
        gc.collect()

    if __name__ == '__main__':
        unittest.main()

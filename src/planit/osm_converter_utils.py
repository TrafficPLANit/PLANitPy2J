from planit.gateway import GatewayUtils


class OsmConverterUtils(object):
    """Utilities for Python-to-Java OSM converter compatibility."""

    @staticmethod
    def create_osm_boundary_from_bounding_box(x1, x2, y1, y2):
        """Create the Java OsmBoundary used by PLANitOSM v0.5.0 bounding-area settings."""
        return GatewayUtils.get_package_jvm().org.goplanit.osm.converter.OsmBoundary.of(x1, x2, y1, y2)

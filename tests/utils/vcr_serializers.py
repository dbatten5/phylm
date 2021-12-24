"""Module to hold custom serializers."""
import zlib
from typing import Any
from typing import Dict

import yaml

# Use the libYAML versions if possible
try:
    from yaml import CDumper as Dumper
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Dumper
    from yaml import Loader


class ResponseBodyCompressor:
    """A custom serializer class to compress/decompress response bodies."""

    @classmethod
    def deserialize(cls, cassette_string: str) -> Dict[Any, Any]:
        """Deserialize the cassette"""
        raw_yaml = yaml.load(cassette_string, Loader=Loader)  # noqa: S506
        for interaction in raw_yaml["interactions"]:
            body = interaction["response"]["body"]["string"]
            interaction["response"]["body"]["string"] = zlib.decompress(body).decode()
        return dict(raw_yaml)

    @classmethod
    def serialize(cls, cassette_dict: Dict[Any, Any]) -> Any:
        """Serialize the cassette"""
        for interaction in cassette_dict["interactions"]:
            body = interaction["response"]["body"]["string"]
            interaction["response"]["body"]["string"] = zlib.compress(body.encode())
        return yaml.dump(cassette_dict, Dumper=Dumper)

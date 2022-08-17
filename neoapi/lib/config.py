from dataclasses import dataclass, field, fields
from typing import List
from yaml import FullLoader
from yaml import load as yaml_load
from typing import Dict, Any


@dataclass
class Config:
    nodes: List[str] = field(default_factory=list)
    default_node: str = field(default_factory=str)

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'Config':
        param_names = [param.name for param in fields(Config)]
        return Config(**{param: param_value for param, param_value in config_dict.items() if param in param_names})

    @classmethod
    def load_from_yaml(cls, file_path: str) -> 'Config':
        with open(file_path) as yaml_file:
            loaded_yaml = yaml_load(yaml_file, Loader=FullLoader)

        return cls.from_dict(config_dict=loaded_yaml)

import json
import os
from dataclasses import dataclass, fields
from pathlib import Path
from typing import List
from .deps import CheckEnviron


class Environ(CheckEnviron):
    class DEFAULTS:
        ENTITYKB_ROOT = os.path.expanduser("~/.entitykb")
        ENTITYKB_RPC_HOST = "localhost"
        ENTITYKB_RPC_PORT = 3477
        ENTITYKB_RPC_TIMEOUT = 2
        ENTITYKB_RPC_RETRIES = 5
        ENTITYKB_MV_SPLIT = "|"

    def commit(self):
        # lock in any environ variables that are not set
        for i in vars(self.DEFAULTS):
            if not i.startswith("_"):
                self.__getitem__(i)

    @property
    def root(self) -> str:
        return self["ENTITYKB_ROOT"]

    @root.setter
    def root(self, value: str):
        self["ENTITYKB_ROOT"] = value

    @property
    def rpc_host(self) -> str:
        return self["ENTITYKB_RPC_HOST"]

    @rpc_host.setter
    def rpc_host(self, value: str):
        self["ENTITYKB_RPC_HOST"] = value

    @property
    def rpc_port(self) -> int:
        return int(self["ENTITYKB_RPC_PORT"])

    @rpc_port.setter
    def rpc_port(self, value: int):
        self["ENTITYKB_RPC_PORT"] = str(value)

    @property
    def rpc_timeout(self) -> int:
        return int(self["ENTITYKB_RPC_TIMEOUT"])

    @rpc_timeout.setter
    def rpc_timeout(self, value: int):
        self["ENTITYKB_RPC_TIMEOUT"] = str(value)

    @property
    def rpc_retries(self) -> int:
        return int(self["ENTITYKB_RPC_RETRIES"])

    @rpc_retries.setter
    def rpc_retries(self, value: int):
        self["ENTITYKB_RPC_RETRIES"] = str(value)

    @property
    def mv_split(self) -> str:
        return self["ENTITYKB_MV_SPLIT"]

    @mv_split.setter
    def mv_split(self, value: str):
        self["ENTITYKB_MV_SPLIT"] = value


environ = Environ()


@dataclass
class Config:
    file_path: str = None
    extractor: str = "entitykb.DefaultExtractor"
    filterers: List[str] = ()
    normalizer: str = "entitykb.LatinLowercaseNormalizer"
    resolvers: List[str] = ("entitykb.TermResolver",)
    tokenizer: str = "entitykb.WhitespaceTokenizer"
    terms: str = "entitykb.TermsIndex"
    graph: str = "entitykb.InMemoryGraph"
    modules: List[str] = ()

    def __str__(self):
        return f"<Config: {self.file_path}>"

    @property
    def root(self):
        return os.path.dirname(self.file_path)

    @classmethod
    def create(cls, root: str) -> "Config":
        config_file_path = cls.get_file_path(root=root)

        data = {}
        if os.path.isfile(config_file_path):
            with open(config_file_path, "r") as fp:
                data = json.load(fp)

        config = cls.construct(file_path=config_file_path, data=data)

        if not os.path.isfile(config_file_path):
            os.makedirs(os.path.dirname(config_file_path), exist_ok=True)
            with open(config_file_path, "w") as fp:
                json.dump(config.dict(), fp, indent=4)
                fp.write("\n")

        return config

    @classmethod
    def construct(cls, *, file_path: str, data: dict) -> "Config":
        field_names = {class_field.name for class_field in fields(cls)}
        data = {k: v for k, v in data.items() if k in field_names}
        config = Config(file_path=file_path, **data)
        return config

    def dict(self) -> dict:
        kw = {
            "extractor": self.extractor,
            "filterers": self.filterers,
            "normalizer": self.normalizer,
            "resolvers": self.resolvers,
            "terms": self.terms,
            "graph": self.graph,
        }

        return dict((k, v) for k, v in kw.items())

    @classmethod
    def get_file_path(cls, root=None, file_name="config.json"):
        root = cls.get_root(root)
        file_path = os.path.join(root, file_name)
        return file_path

    @classmethod
    def get_root(cls, root=None) -> str:
        if isinstance(root, Path):
            root = str(root.resolve())

        root = root or environ.root

        return root

    def info(self) -> dict:
        info = self.dict()
        info["root"] = self.root
        info["resolvers"] = self.resolvers
        info["filterers"] = self.filterers
        return info

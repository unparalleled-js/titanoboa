from typing import Any, List
from vyper.codegen.types.types import BaseType, is_integer_type, ByteArrayType, StringType, DArrayType, SArrayType, MappingType, is_base_type
from dataclasses import dataclass

@dataclass
class VyperObject:
    value: Any
    typ: BaseType

    @classmethod
    def empty(cls, typ):
        if is_integer_type(typ):
            return cls(0, typ)
        if isinstance(typ, ByteArrayType):
            return cls(b"", typ)
        if isinstance(typ, StringType):
            return cls("", typ)
        if isinstance(typ, DArrayType):
            return cls([], typ)
        if isinstance(typ, SArrayType):
            return cls([cls.empty(typ.subtype)] * typ.count, typ)
        if isinstance(typ, MappingType):
            return cls(VyperHashMap(typ.keytype, typ.valuetype), typ)
        if is_base_type(typ, "address"):
            return cls("0x" + "00"*20, typ)

        raise Exception(f"unreachable {typ}")

class VyperHashMap(dict):
    def __init__(self, key_type, value_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key_type = key_type
        self.value_type = value_type

    def __getitem__(self, k):
        if k not in self:
            return VyperObject.empty(self.value_type)
        return self[k]

@dataclass
class LogItem:
    topics: List[VyperObject]
    data: List[VyperObject]

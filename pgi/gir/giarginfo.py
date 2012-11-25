# Copyright 2012 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

from pgi.glib import Enum, gboolean, gint
from gitypeinfo import GITypeInfoPtr
from gibaseinfo import GIBaseInfo, GIBaseInfoPtr, GIInfoType
from pgi.ctypesutil import find_library, wrap_class

_gir = find_library("girepository-1.0")


def gi_is_arg_info(base_info, _type=GIInfoType.ARG):
    return base_info.get_type().value == _type


class GITransfer(Enum):
    NOTHING, CONTAINER, EVERYTHING = range(3)


class GIDirection(Enum):
    IN, OUT, INOUT = range(3)


class GIScopeType(Enum):
    INVALID, CALL, ASYNC, NOTIFIED = range(4)


class GIArgInfo(GIBaseInfo):
    pass


class GIArgInfoPtr(GIBaseInfoPtr):
    _type_ = GIArgInfo

    def _get_repr(self):
        values = super(GIArgInfoPtr, self)._get_repr()
        values["direction"] = repr(self.get_direction())
        values["is_caller_allocates"] = repr(self.is_caller_allocates())
        values["is_return_value"] = repr(self.is_return_value())
        values["is_optional"] = repr(self.is_optional())
        values["may_be_null"] = repr(self.may_be_null())
        values["ownership_transfer"] = repr(self.get_ownership_transfer())
        values["scope"] = repr(self.get_scope())
        values["closure"] = repr(self.get_closure())
        values["destroy"] = repr(self.get_destroy())
        type_ = self.get_type()
        values["type"] = repr(type_)
        type_.unref()

        return values

_methods = [
    ("get_direction", GIDirection, [GIArgInfoPtr]),
    ("is_caller_allocates", gboolean, [GIArgInfoPtr]),
    ("is_return_value", gboolean, [GIArgInfoPtr]),
    ("is_optional", gboolean, [GIArgInfoPtr]),
    ("may_be_null", gboolean, [GIArgInfoPtr]),
    ("get_ownership_transfer", GITransfer, [GIArgInfoPtr]),
    ("get_scope", GIScopeType, [GIArgInfoPtr]),
    ("get_closure", gint, [GIArgInfoPtr]),
    ("get_destroy", gint, [GIArgInfoPtr]),
    ("get_type", GITypeInfoPtr, [GIArgInfoPtr]),
    ("load_type", None, [GIArgInfoPtr, GITypeInfoPtr]),
]

wrap_class(_gir, GIArgInfo, GIArgInfoPtr, "g_arg_info_", _methods)

__all__ = ["GITransfer", "GIDirection", "GIScopeType", "GIArgInfo",
           "GIArgInfoPtr", "gi_is_arg_info"]

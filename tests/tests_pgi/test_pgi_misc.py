# Copyright 2013 Christoph Reiter
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import re
import unittest

from tests import skipUnlessCairo

import pgi

from pgi.foreign import get_foreign
from pgi.codegen import ctypes_backend
try:
    from pgi.codegen import cffi_backend
    cffi_backend = cffi_backend
except ImportError:
    cffi_backend = None
from pgi.util import escape_identifier, unescape_identifier
from pgi.util import escape_parameter, unescape_parameter
from pgi.gtype import PGType
from pgi.clib.gobject import GType


class PGIMisc(unittest.TestCase):
    def test_escape_property(self):
        self.assertEqual(escape_parameter("class"), "class_")
        self.assertEqual(escape_parameter("cla-ss"), "cla_ss")
        self.assertEqual(escape_parameter("2BUTTON_PRESS"), "_2BUTTON_PRESS")

    def test_unescape_property(self):
        self.assertEqual(unescape_parameter("foo_"), "foo")
        self.assertEqual(unescape_parameter("fo_oo"), "fo-oo")

    def test_escape_identifier(self):
        self.assertEqual(escape_identifier("class"), "class_")
        self.assertEqual(escape_identifier("2BUTTON_PRESS"), "_2BUTTON_PRESS")

    def test_unescape_identifier(self):
        self.assertEqual(unescape_identifier("foo_"), "foo")

    def test_gtype(self):
        self.assertEqual(PGType(0), PGType(GType(0)))

    @unittest.skipUnless(cffi_backend, "cffi missing")
    def test_backends(self):
        # to keep things simple the cffi backend should be a subset
        # of the ctypes one. So check all attributes
        cffi = [a for a in dir(cffi_backend.CFFIBackend) if a[:1] != "_"]
        ct = [a for a in dir(ctypes_backend.CTypesBackend) if a[:1] != "_"]
        self.assertFalse(set(cffi) - set(ct))

    def test_signal_property_object(self):
        from pgi.repository import Gtk
        sigs = Gtk.Window.signals
        sig = sigs.set_focus
        self.assertEqual(sig.name, "set-focus")
        self.assertEqual(sig.param_types, [Gtk.Widget.__gtype__])
        self.assertEqual(sig.instance_type, Gtk.Window.__gtype__)
        self.assertEqual(sig.flags, 2)
        self.assertEqual(sig.return_type, PGType.from_name("void"))

    def test_signal_dummy_callback(self):
        from pgi.repository import Gtk
        sigs = Gtk.Window.signals
        sig = sigs.set_focus
        self.assertRaises(TypeError, sig)
        self.assertRaises(NotImplementedError, sig, None)

    def test_signal_property_interface(self):
        from pgi.repository import Gtk
        sigs = Gtk.TreeModel.signals
        sig = sigs.row_changed
        self.assertEqual(sig.name, "row-changed")
        # TreePath gtypes fail here.. no idea
        self.assertEqual(len(sig.param_types), 2)
        self.assertEqual(sig.instance_type, Gtk.TreeModel.__gtype__)
        self.assertEqual(sig.flags, 2)
        self.assertEqual(sig.return_type, PGType.from_name("void"))

    def test_check_foreign(self):
        self.assertRaises(ValueError, pgi.check_foreign, "foo", "bar")

    @skipUnlessCairo
    def test_get_foreing(self):
        foreign = get_foreign("cairo", "Context")
        self.assertTrue(foreign)

    def test_check_version(self):
        # make sure the exception mentions both versions in case of an error
        self.assertRaisesRegexp(ValueError, re.escape("99.99.99"),
                                pgi.check_version, "99.99.99")

        self.assertRaisesRegexp(ValueError, re.escape(pgi.__version__),
                                pgi.check_version, "99.99.99")

    def test_callback(self):
        from gi.repository import GLib, GObject

        self.assertTrue(hasattr(GLib, "SourceFunc"))
        func = GLib.SourceFunc
        self.assertEqual(func.__name__, "SourceFunc")
        self.assertEqual(func.__module__, "GLib")

        self.assertTrue(hasattr(GObject, "Callback"))
        func = GObject.Callback
        self.assertEqual(func.__name__, "Callback")
        self.assertEqual(func.__module__, "GObject")

    def test_callback_call(self):
        from gi.repository import GLib

        self.assertRaises(RuntimeError, GLib.DestroyNotify, None)
        self.assertRaises(TypeError, GLib.DestroyNotify)

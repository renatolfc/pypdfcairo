#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Renato L. F. Cunha <renato-code@cunha.io>
#
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See the COPYING
# file for more details.
#

"""
.. module:: rsvgcffi
    :platform: Unix, Windows
    :synopsis: Utility module for pypdfcairo.

.. moduleauthor:: Renato L. F. Cunha <renato-code@cunha.io>

"""

from cffi import FFI
from ctypes import util

LIBRSVG = None

ffi = FFI()

ffi.cdef("""
    typedef void    RsvgHandle;
    typedef void    cairo_t;

    typedef int     gint;
    typedef gint    gboolean;
    typedef char    gchar;

    typedef struct {
        uint32_t    domain;
        int         code;
        char        *message;
    } GError;

    typedef struct {
        int         width, height;
        double      em, ex;
    } RsvgDimensionData;

    RsvgHandle *rsvg_handle_new_from_file(const gchar *, GError **);
    void rsvg_handle_get_dimensions(RsvgHandle *, RsvgDimensionData *);
    gboolean rsvg_handle_render_cairo(RsvgHandle *, cairo_t *);
    void g_type_init();
""")

def _load_rsvg(rsvg_lib_path=None, gobject_lib_path=None):
    """Loads the wrapped libraries.

    :param rsvg_lib_path: The path to the rsvg library.
    :param gobject_lib_path: The path to the gobject library.
    """
    if rsvg_lib_path is None:
        rsvg_lib_path = util.find_library('rsvg-2')
    if gobject_lib_path is None:
        gobject_lib_path = util.find_library('gobject-2.0')
    l = ffi.dlopen(rsvg_lib_path)
    g = ffi.dlopen(gobject_lib_path)
    g.g_type_init()

    return l

if not LIBRSVG:
    LIBRSVG = _load_rsvg()

class RsvgException(Exception):
    "Base generic exception for the rsvg module"
    pass

class Handle(object):
    def __init__(self, file):
        lib = LIBRSVG
        errorp = ffi.new("GError **");
        self.handle = lib.rsvg_handle_new_from_file(file, errorp)
        if self.handle is None:
            error = ffi.string(errorp[0][0].message)
            raise RsvgException(error)
        self.props = ffi.new("RsvgDimensionData *")
        lib.rsvg_handle_get_dimensions(self.handle, self.props)


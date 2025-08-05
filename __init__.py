'''
Lost Selection - Selection utilities and operators for Blender

Copyright (C) 2025 Lost Selection
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.
'''

bl_info = {
    'name': "Lost Selection",
    'description': "Set of usefull extra selection operators",
    'author': "ezelar.com",
    'version': (0, 1, 0),
    'blender': (4, 2, 0),
    'location': 'View3D > Context Menu',
    'wiki_url': 'https://github.com/niewinny/lost_selection',
    'category': '3D View'}

from . import registry, ops


def register():
    registry.register()


def unregister():
    registry.unregister()
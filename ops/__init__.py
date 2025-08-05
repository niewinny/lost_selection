# Operators module initialization
import bpy

from . import similar_display_type, similar_rotation


class Theme(bpy.types.PropertyGroup):
    """Theme settings for all operators"""
    pass


types_classes = (
    Theme,
)

# Collect classes from imported modules
classes = (
    *similar_display_type.classes,
    *similar_rotation.classes,
)
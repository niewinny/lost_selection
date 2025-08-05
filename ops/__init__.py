# Operators module initialization
import bpy


class Theme(bpy.types.PropertyGroup):
    """Theme settings for all operators"""
    pass


types_classes = (
    Theme,
)

# Collect classes from imported modules
# Currently empty - operators will be added here
classes = (
)
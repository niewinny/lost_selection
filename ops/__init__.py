# Operators module initialization

from . import (
    similar_display_type,
    similar_material,
    similar_color,
    similar_rotation,
    similar_modifiers,
    connected_crease,
    connected_sharp,
    connected_bevel,
    connected_seam,
    connected_length,
)


# Collect classes from imported modules
classes = (
    *similar_display_type.classes,
    *similar_material.classes,
    *similar_color.classes,
    *similar_rotation.classes,
    *similar_modifiers.classes,
    *connected_crease.classes,
    *connected_sharp.classes,
    *connected_bevel.classes,
    *connected_seam.classes,
    *connected_length.classes,
)
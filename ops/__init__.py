# Operators module initialization

from . import (
    connected_bevel,
    connected_crease,
    connected_length,
    connected_seam,
    connected_sharp,
    similar_color,
    similar_display_type,
    similar_material,
    similar_modifiers,
    similar_rotation,
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

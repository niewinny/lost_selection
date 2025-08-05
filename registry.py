from bpy.utils import register_class, unregister_class
import bpy

# Explicit imports - All modules that contain registrable classes
from . import ops


# Collect all classes in registration order
classes = (
    *ops.classes,
)


def register():
    """Register all addon components"""
    
    # Register all classes
    for cls in classes:
        register_class(cls)
    


def unregister():
    """Unregister all addon components"""
    
    # Unregister classes in reverse order
    for cls in reversed(classes):
        unregister_class(cls)
    
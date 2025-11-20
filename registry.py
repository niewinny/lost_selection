from bpy.utils import register_class, unregister_class

# Explicit imports - All modules that contain registrable classes
from . import keymap, ops, ui

# Collect all classes in registration order
classes = (
    *ops.classes,
    *ui.classes,
)


def register():
    """Register all addon components"""

    # Register all classes
    for cls in classes:
        register_class(cls)

    # Register UI menus
    ui.register()

    # Register keymaps
    keymap.register()


def unregister():
    """Unregister all addon components"""

    # Unregister keymaps
    keymap.unregister()

    # Unregister UI menus
    ui.unregister()

    # Unregister classes in reverse order
    for cls in reversed(classes):
        unregister_class(cls)

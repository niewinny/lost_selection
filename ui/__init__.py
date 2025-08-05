import bpy
from bpy.types import Menu


class VIEW3D_MT_select_similar(Menu):
    """Select Similar menu"""
    bl_label = "Select Similar"
    bl_idname = "VIEW3D_MT_select_similar"
    
    def draw(self, context):
        layout = self.layout
        layout.operator("object.select_similar_display_type", text="Display Type")
        layout.operator("object.select_similar_rotation", text="Rotation")
        # Use operator_context to ensure invoke is called
        layout.operator_context = 'INVOKE_DEFAULT'
        layout.operator("object.select_similar_modifiers", text="Modifiers")


def draw_select_similar_menu(self, context):
    """Add Select Similar submenu to the Select menu"""
    layout = self.layout
    layout.menu("VIEW3D_MT_select_similar")


classes = (
    VIEW3D_MT_select_similar,
)


def register():
    """Register UI menus"""
    # Add Select Similar menu to the main Select Object menu
    bpy.types.VIEW3D_MT_select_object.append(draw_select_similar_menu)


def unregister():
    """Unregister UI menus"""
    # Remove menu from Select Object menu
    bpy.types.VIEW3D_MT_select_object.remove(draw_select_similar_menu)
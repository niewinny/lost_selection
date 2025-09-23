import bpy
from bpy.types import Menu


class VIEW3D_MT_select_similar(Menu):
    """Select Similar menu"""
    bl_label = "Select Similar"
    bl_idname = "VIEW3D_MT_select_similar"
    
    def draw(self, context):
        layout = self.layout
        layout.operator("object.select_similar_display_type", text="Display Type")
        layout.operator("object.select_similar_material", text="Material")
        layout.operator("object.select_similar_color", text="Color")
        layout.operator("object.select_similar_rotation", text="Rotation")
        # Use operator_context to ensure invoke is called
        layout.operator_context = 'INVOKE_DEFAULT'
        layout.operator("object.select_similar_modifiers", text="Modifiers")


class VIEW3D_MT_select_connected(Menu):
    """Select Connected menu for Edit Mode"""
    bl_label = "Select Connected"
    bl_idname = "VIEW3D_MT_select_connected"
    
    def draw(self, context):
        layout = self.layout
        layout.operator("mesh.select_connected_crease", text="Crease")
        layout.operator("mesh.select_connected_sharp", text="Sharp")
        layout.operator("mesh.select_connected_bevel", text="Bevel Weight")
        layout.operator("mesh.select_connected_seam", text="Seam")
        
        # Only show Length operator in edge mode
        if context.tool_settings.mesh_select_mode[1]:
            layout.operator("mesh.select_connected_length", text="Length")


def draw_select_similar_menu(self, context):
    """Add Select Similar submenu to the Select menu"""
    layout = self.layout
    layout.menu("VIEW3D_MT_select_similar")


def draw_select_connected_menu(self, context):
    """Add Select Connected submenu to the Edit Mode Select menu"""
    layout = self.layout
    layout.separator()
    layout.menu("VIEW3D_MT_select_connected")


classes = (
    VIEW3D_MT_select_similar,
    VIEW3D_MT_select_connected,
)


def register():
    """Register UI menus"""
    # Add Select Similar menu to the main Select Object menu
    bpy.types.VIEW3D_MT_select_object.append(draw_select_similar_menu)
    
    # Add Select Connected menu to Edit Mesh Select menu
    bpy.types.VIEW3D_MT_select_edit_mesh.append(draw_select_connected_menu)


def unregister():
    """Unregister UI menus"""
    # Remove menu from Select Object menu
    bpy.types.VIEW3D_MT_select_object.remove(draw_select_similar_menu)
    
    # Remove menu from Edit Mesh Select menu
    bpy.types.VIEW3D_MT_select_edit_mesh.remove(draw_select_connected_menu)
import bpy
from bpy.types import Operator
from bpy.props import BoolProperty, CollectionProperty, StringProperty


class ModifierTypeItem(bpy.types.PropertyGroup):
    """Property group for storing modifier types"""
    name: StringProperty(
        name="Modifier Type",
        description="Type of modifier to match"
    )
    enabled: BoolProperty(
        name="Enabled",
        description="Include this modifier type in selection",
        default=True
    )


class OBJECT_OT_select_similar_modifiers(Operator):
    """Select objects with similar modifiers as active object"""
    bl_idname = "object.select_similar_modifiers"
    bl_label = "Modifiers"
    bl_options = {'REGISTER', 'UNDO'}
    
    extend: BoolProperty(
        name="Extend",
        description="Extend selection instead of replacing",
        default=False
    )
    
    modifier_types: CollectionProperty(
        type=ModifierTypeItem,
        name="Modifier Types",
        description="List of modifier types to match"
    )
    
    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and context.active_object is not None
    
    def invoke(self, context, event):
        active_obj = context.active_object
        
        if not active_obj:
            self.report({'WARNING'}, "No active object")
            return {'CANCELLED'}
        
        # Clear and populate modifier types from active object
        self.modifier_types.clear()
        
        # Get unique modifier types from active object
        modifier_types_set = set()
        for mod in active_obj.modifiers:
            modifier_types_set.add(mod.type)
        
        # Add each unique modifier type to the collection
        for mod_type in sorted(modifier_types_set):
            item = self.modifier_types.add()
            item.name = mod_type
            item.enabled = True
        
        if not self.modifier_types:
            self.report({'WARNING'}, "Active object has no modifiers")
            return {'CANCELLED'}
        
        # Show the dialog
        return context.window_manager.invoke_props_dialog(self, width=300)
    
    def draw(self, context):
        layout = self.layout
        
        layout.label(text="Select objects with these modifiers:")
        
        # Draw list of modifier types with checkboxes
        for item in self.modifier_types:
            row = layout.row()
            row.prop(item, "enabled", text="")
            # Format modifier name: ARRAY -> Array, SUBDIVISION_SURFACE -> Subdivision Surface
            formatted_name = item.name.replace('_', ' ').title()
            row.label(text=formatted_name)
        
        layout.separator()
        layout.prop(self, "extend")
    
    def execute(self, context):
        active_obj = context.active_object
        
        if not active_obj:
            self.report({'WARNING'}, "No active object")
            return {'CANCELLED'}
        
        # Get enabled modifier types
        selected_types = {item.name for item in self.modifier_types if item.enabled}
        
        if not selected_types:
            self.report({'WARNING'}, "No modifier types selected")
            return {'CANCELLED'}
        
        # Select objects with matching modifiers
        for obj in context.visible_objects:
            # Get object's modifier types
            obj_modifier_types = {mod.type for mod in obj.modifiers}
            
            # Check if object has all selected modifier types
            if selected_types.issubset(obj_modifier_types):
                obj.select_set(True)
            elif not self.extend:
                obj.select_set(False)
        
        return {'FINISHED'}


classes = (
    ModifierTypeItem,
    OBJECT_OT_select_similar_modifiers,
)
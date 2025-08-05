import bpy
from bpy.types import Operator
from bpy.props import BoolProperty


class OBJECT_OT_select_similar_display_type(Operator):
    """Select objects with same display type as active object"""
    bl_idname = "object.select_similar_display_type"
    bl_label = "Display Type"
    bl_options = {'REGISTER', 'UNDO'}
    
    extend: BoolProperty(
        name="Extend",
        description="Extend selection instead of replacing",
        default=False
    )
    
    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and context.active_object is not None
    
    def execute(self, context):
        active_obj = context.active_object
        
        if not active_obj:
            self.report({'WARNING'}, "No active object")
            return {'CANCELLED'}
        
        active_display_type = active_obj.display_type

        for obj in context.visible_objects:
            if obj.display_type == active_display_type:
                obj.select_set(True)
            elif not self.extend:
                obj.select_set(False)
        

        return {'FINISHED'}


classes = (
    OBJECT_OT_select_similar_display_type,
)
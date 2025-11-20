import bpy
from bpy.props import BoolProperty
from bpy.types import Operator


class OBJECT_OT_select_similar_rotation(Operator):
    """Select objects with exactly the same rotation as active object"""
    bl_idname = "object.select_similar_rotation"
    bl_label = "Rotation"
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

        # Get active object's rotation in euler
        active_rotation = active_obj.rotation_euler

        for obj in context.visible_objects:
            # Check if rotation is exactly the same (within floating point precision)
            if (abs(obj.rotation_euler.x - active_rotation.x) < 0.0001 and
                abs(obj.rotation_euler.y - active_rotation.y) < 0.0001 and
                abs(obj.rotation_euler.z - active_rotation.z) < 0.0001):
                obj.select_set(True)
            elif not self.extend:
                obj.select_set(False)

        return {'FINISHED'}


classes = (
    OBJECT_OT_select_similar_rotation,
)

import bpy
from bpy.props import BoolProperty
from bpy.types import Operator


class OBJECT_OT_select_similar_material(Operator):
    """Select objects with similar materials as active object"""
    bl_idname = "object.select_similar_material"
    bl_label = "Material"
    bl_options = {'REGISTER', 'UNDO'}

    extend: BoolProperty(
        name="Extend",
        description="Extend selection instead of replacing",
        default=False
    )

    match_all: BoolProperty(
        name="Match All",
        description="Match all materials (instead of any material)",
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

        # Get active object's materials
        active_materials = set()
        if active_obj.data and hasattr(active_obj.data, 'materials'):
            for mat in active_obj.data.materials:
                if mat:
                    active_materials.add(mat)

        if not active_materials:
            self.report({'WARNING'}, "Active object has no materials")
            return {'CANCELLED'}

        for obj in context.visible_objects:
            # Skip objects without material slots
            if not obj.data or not hasattr(obj.data, 'materials'):
                if not self.extend:
                    obj.select_set(False)
                continue

            # Get object's materials
            obj_materials = set()
            for mat in obj.data.materials:
                if mat:
                    obj_materials.add(mat)

            # Check material match
            if self.match_all:
                # Object must have exactly the same materials
                matches = obj_materials == active_materials
            else:
                # Object must have at least one material in common
                matches = bool(obj_materials & active_materials)

            if matches:
                obj.select_set(True)
            elif not self.extend:
                obj.select_set(False)

        return {'FINISHED'}


classes = (
    OBJECT_OT_select_similar_material,
)

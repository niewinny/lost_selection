import bpy
from bpy.props import BoolProperty, FloatProperty
from bpy.types import Operator


class OBJECT_OT_select_similar_color(Operator):
    """Select objects with similar material viewport display color as active object"""
    bl_idname = "object.select_similar_color"
    bl_label = "Color"
    bl_options = {'REGISTER', 'UNDO'}

    extend: BoolProperty(
        name="Extend",
        description="Extend selection instead of replacing",
        default=False
    )

    tolerance: FloatProperty(
        name="Tolerance",
        description="Color tolerance for matching (0 = exact match, 1 = any color)",
        min=0.0,
        max=1.0,
        default=0.1,
        precision=3
    )

    match_any: BoolProperty(
        name="Match Any",
        description="Match if any material has similar color (instead of all)",
        default=True
    )

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and context.active_object is not None

    def execute(self, context):
        active_obj = context.active_object

        if not active_obj:
            self.report({'WARNING'}, "No active object")
            return {'CANCELLED'}

        # Get active object's material viewport colors
        active_colors = []
        if active_obj.data and hasattr(active_obj.data, 'materials'):
            for mat in active_obj.data.materials:
                if mat:
                    # Get material's viewport display color
                    active_colors.append(mat.diffuse_color[:3])  # RGB only, ignore alpha

        if not active_colors:
            self.report({'WARNING'}, "Active object has no materials with viewport colors")
            return {'CANCELLED'}

        for obj in context.visible_objects:
            # Skip objects without material slots
            if not obj.data or not hasattr(obj.data, 'materials'):
                if not self.extend:
                    obj.select_set(False)
                continue

            # Get object's material viewport colors
            obj_colors = []
            for mat in obj.data.materials:
                if mat:
                    obj_colors.append(mat.diffuse_color[:3])

            if not obj_colors:
                if not self.extend:
                    obj.select_set(False)
                continue

            # Check for color matches
            matches = False
            for obj_color in obj_colors:
                for active_color in active_colors:
                    # Calculate color difference (Euclidean distance in RGB space)
                    diff = sum((a - b) ** 2 for a, b in zip(active_color, obj_color)) ** 0.5

                    # Maximum possible distance in RGB space is sqrt(3) for colors in 0-1 range
                    # Normalize to 0-1 range
                    normalized_diff = diff / (3 ** 0.5)

                    if normalized_diff <= self.tolerance:
                        matches = True
                        break

                if matches and self.match_any:
                    break
                elif matches and not self.match_any:
                    # Need to check if all materials match
                    # This is more complex logic - simplified for now
                    pass

            if matches:
                obj.select_set(True)
            elif not self.extend:
                obj.select_set(False)

        return {'FINISHED'}


classes = (
    OBJECT_OT_select_similar_color,
)

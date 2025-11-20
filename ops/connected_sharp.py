import bmesh
import bpy
from bpy.props import EnumProperty
from bpy.types import Operator

from .connected_utils import get_initial_vertices_and_edges


class MESH_OT_select_connected_sharp(Operator):
    """Select connected edges/faces with sharp marking"""
    bl_idname = "mesh.select_connected_sharp"
    bl_label = "Select Connected by Sharp"
    bl_options = {'REGISTER', 'UNDO'}

    comparison: EnumProperty(
        name="Comparison",
        description="How to compare sharp values",
        items=[
            ('EQUAL', "Equal", "Select edges with same sharp state"),
            ('TRUE', "Sharp", "Select only sharp edges"),
            ('FALSE', "Not Sharp", "Select only non-sharp edges"),
        ],
        default='EQUAL'
    )

    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'

    def execute(self, context):
        obj = context.active_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)

        # Check if we're in face mode
        face_mode = context.tool_settings.mesh_select_mode[2]

        if face_mode:
            # Face selection mode
            selected_faces = [f for f in bm.faces if f.select]
            if not selected_faces:
                self.report({'WARNING'}, "No faces selected")
                return {'CANCELLED'}

            # Get reference sharp value from first selected edge
            reference_sharp = None
            for face in selected_faces:
                for edge in face.edges:
                    if edge.select or face.select:  # Check if edge is part of selected face
                        reference_sharp = not edge.smooth
                        break
                if reference_sharp is not None:
                    break

            if reference_sharp is None:
                # Default to non-sharp if no reference found
                reference_sharp = False

            # Process each face
            faces_to_process = selected_faces.copy()
            selected_face_set = set(selected_faces)

            while faces_to_process:
                current_face = faces_to_process.pop(0)

                # Check connected faces through edges
                for edge in current_face.edges:
                    for face in edge.link_faces:
                        if face not in selected_face_set:
                            # Check if all edges of this face meet criteria
                            all_edges_match = True
                            for face_edge in face.edges:
                                edge_sharp = not face_edge.smooth

                                meets_criteria = False
                                if self.comparison == 'EQUAL':
                                    meets_criteria = edge_sharp == reference_sharp
                                elif self.comparison == 'TRUE':
                                    meets_criteria = edge_sharp  # Sharp edges have smooth=False
                                elif self.comparison == 'FALSE':
                                    meets_criteria = not edge_sharp  # Non-sharp edges have smooth=True

                                if not meets_criteria:
                                    all_edges_match = False
                                    break

                            if all_edges_match:
                                face.select = True
                                selected_face_set.add(face)
                                faces_to_process.append(face)
        else:
            # Edge/Vertex selection mode
            initial_verts, initial_edges = get_initial_vertices_and_edges(context, bm)
            if not initial_verts:
                self.report({'WARNING'}, "Nothing selected")
                return {'CANCELLED'}

            # Process expansion from each selected vertex
            all_selected_edges = set()

            for start_vert in initial_verts:
                # Get edges connected to this vertex
                edges_to_process = list(start_vert.link_edges)
                local_selected = set()

                # Get reference sharp value from first selected edge
                reference_sharp = None
                for edge in start_vert.link_edges:
                    if edge.select:
                        reference_sharp = not edge.smooth
                        break

                if reference_sharp is None:
                    continue

                while edges_to_process:
                    current_edge = edges_to_process.pop(0)

                    if current_edge in local_selected:
                        continue

                    edge_sharp = not current_edge.smooth

                    # Check if edge meets criteria
                    meets_criteria = False
                    if self.comparison == 'EQUAL':
                        meets_criteria = edge_sharp == reference_sharp
                    elif self.comparison == 'TRUE':
                        meets_criteria = edge_sharp  # Sharp edges have smooth=False
                    elif self.comparison == 'FALSE':
                        meets_criteria = not edge_sharp  # Non-sharp edges have smooth=True

                    if meets_criteria:
                        current_edge.select = True
                        all_selected_edges.add(current_edge)
                        local_selected.add(current_edge)

                        # Add connected edges through vertices
                        for vert in current_edge.verts:
                            for edge in vert.link_edges:
                                if edge not in local_selected:
                                    edges_to_process.append(edge)

        bmesh.update_edit_mesh(me)
        return {'FINISHED'}


classes = (
    MESH_OT_select_connected_sharp,
)

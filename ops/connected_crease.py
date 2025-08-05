import bpy
import bmesh
from bpy.types import Operator
from bpy.props import EnumProperty
from .connected_utils import get_initial_vertices_and_edges


class MESH_OT_select_connected_crease(Operator):
    """Select connected edges/faces with similar crease values"""
    bl_idname = "mesh.select_connected_crease"
    bl_label = "Select Connected by Crease"
    bl_options = {'REGISTER', 'UNDO'}
    
    comparison: EnumProperty(
        name="Comparison",
        description="How to compare crease values",
        items=[
            ('EQUAL', "Equal", "Select edges with equal crease value"),
            ('GREATER', "Greater", "Select edges with greater crease value"),
            ('LESS', "Less", "Select edges with less crease value"),
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
        
        # Get crease layer
        crease_layer = bm.edges.layers.crease.active
        if not crease_layer:
            self.report({'WARNING'}, "No crease values found")
            return {'CANCELLED'}
        
        # Check if we're in face mode
        face_mode = context.tool_settings.mesh_select_mode[2]
        
        if face_mode:
            # Face selection mode
            selected_faces = [f for f in bm.faces if f.select]
            if not selected_faces:
                self.report({'WARNING'}, "No faces selected")
                return {'CANCELLED'}
            
            # Get reference crease value from first face's edges
            if selected_faces:
                ref_edge = selected_faces[0].edges[0] if selected_faces[0].edges else None
                if ref_edge:
                    reference_crease = ref_edge[crease_layer]
                else:
                    return {'CANCELLED'}
            
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
                                edge_crease = face_edge[crease_layer]
                                
                                meets_criteria = False
                                if self.comparison == 'EQUAL':
                                    meets_criteria = abs(edge_crease - reference_crease) < 0.001
                                elif self.comparison == 'GREATER':
                                    meets_criteria = edge_crease > reference_crease
                                elif self.comparison == 'LESS':
                                    meets_criteria = edge_crease < reference_crease
                                
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
                
                # Get reference crease value from first edge
                if edges_to_process:
                    reference_crease = edges_to_process[0][crease_layer]
                else:
                    continue
                
                while edges_to_process:
                    current_edge = edges_to_process.pop(0)
                    
                    if current_edge in local_selected:
                        continue
                        
                    edge_crease = current_edge[crease_layer]
                    
                    # Check if edge meets criteria
                    meets_criteria = False
                    if self.comparison == 'EQUAL':
                        meets_criteria = abs(edge_crease - reference_crease) < 0.001
                    elif self.comparison == 'GREATER':
                        meets_criteria = edge_crease > reference_crease
                    elif self.comparison == 'LESS':
                        meets_criteria = edge_crease < reference_crease
                    
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
    MESH_OT_select_connected_crease,
)
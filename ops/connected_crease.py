import bpy
import bmesh
from bpy.types import Operator
from bpy.props import EnumProperty


class MESH_OT_select_connected_crease(Operator):
    """Select connected edges with similar crease values"""
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
        return context.mode == 'EDIT_MESH' and context.tool_settings.mesh_select_mode[1]
    
    def execute(self, context):
        obj = context.active_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        
        # Get crease layer
        crease_layer = bm.edges.layers.crease.active
        if not crease_layer:
            self.report({'WARNING'}, "No crease values found")
            return {'CANCELLED'}
        
        # Get initially selected edges and their crease values
        initial_edges = [e for e in bm.edges if e.select]
        if not initial_edges:
            self.report({'WARNING'}, "No edges selected")
            return {'CANCELLED'}
        
        # Process selection expansion
        edges_to_process = initial_edges.copy()
        selected_edges = set(initial_edges)
        
        while edges_to_process:
            current_edge = edges_to_process.pop(0)
            current_crease = current_edge[crease_layer]
            
            # Check connected edges through vertices
            for vert in current_edge.verts:
                for edge in vert.link_edges:
                    if edge not in selected_edges:
                        edge_crease = edge[crease_layer]
                        
                        # Check if edge meets criteria
                        meets_criteria = False
                        if self.comparison == 'EQUAL':
                            meets_criteria = abs(edge_crease - current_crease) < 0.001
                        elif self.comparison == 'GREATER':
                            meets_criteria = edge_crease > current_crease
                        elif self.comparison == 'LESS':
                            meets_criteria = edge_crease < current_crease
                        
                        if meets_criteria:
                            edge.select = True
                            selected_edges.add(edge)
                            edges_to_process.append(edge)
        
        bmesh.update_edit_mesh(me)
        return {'FINISHED'}


classes = (
    MESH_OT_select_connected_crease,
)
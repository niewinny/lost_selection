import bpy
import bmesh
from bpy.types import Operator
from bpy.props import EnumProperty


class MESH_OT_select_connected_seam(Operator):
    """Select connected edges with seam marking"""
    bl_idname = "mesh.select_connected_seam"
    bl_label = "Select Connected by Seam"
    bl_options = {'REGISTER', 'UNDO'}
    
    comparison: EnumProperty(
        name="Comparison",
        description="How to compare seam values",
        items=[
            ('EQUAL', "Equal", "Select edges with same seam state"),
            ('TRUE', "Seam", "Select only seam edges"),
            ('FALSE', "Not Seam", "Select only non-seam edges"),
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
        
        # Get initially selected edges
        initial_edges = [e for e in bm.edges if e.select]
        if not initial_edges:
            self.report({'WARNING'}, "No edges selected")
            return {'CANCELLED'}
        
        # Process selection expansion
        edges_to_process = initial_edges.copy()
        selected_edges = set(initial_edges)
        
        while edges_to_process:
            current_edge = edges_to_process.pop(0)
            current_seam = current_edge.seam
            
            # Check connected edges through vertices
            for vert in current_edge.verts:
                for edge in vert.link_edges:
                    if edge not in selected_edges:
                        edge_seam = edge.seam
                        
                        # Check if edge meets criteria
                        meets_criteria = False
                        if self.comparison == 'EQUAL':
                            meets_criteria = edge_seam == current_seam
                        elif self.comparison == 'TRUE':
                            meets_criteria = edge_seam
                        elif self.comparison == 'FALSE':
                            meets_criteria = not edge_seam
                        
                        if meets_criteria:
                            edge.select = True
                            selected_edges.add(edge)
                            edges_to_process.append(edge)
        
        bmesh.update_edit_mesh(me)
        return {'FINISHED'}


classes = (
    MESH_OT_select_connected_seam,
)
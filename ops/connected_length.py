import bpy
import bmesh
from bpy.types import Operator
from bpy.props import FloatProperty


class MESH_OT_select_connected_length(Operator):
    """Select connected edges based on length thresholds"""
    bl_idname = "mesh.select_connected_length"
    bl_label = "Select Connected by Length"
    bl_options = {'REGISTER', 'UNDO'}
    
    min_length: FloatProperty(
        name="Min Length",
        description="Minimum edge length to select (0 = use selected edge length)",
        default=0.0,
        min=0.0,
        unit='LENGTH'
    )
    
    max_length: FloatProperty(
        name="Max Length",
        description="Maximum edge length to select (0 = use selected edge length)",
        default=0.0,
        min=0.0,
        unit='LENGTH'
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
        
        # If both are 0, use the first selected edge's length
        if self.min_length == 0.0 and self.max_length == 0.0:
            edge_length = initial_edges[0].calc_length()
            # Use a small tolerance for floating point comparison
            tolerance = 0.0001
            min_val = edge_length - tolerance
            max_val = edge_length + tolerance
        else:
            min_val = self.min_length
            max_val = self.max_length
            
            # Validate min/max
            if min_val > max_val:
                self.report({'WARNING'}, "Min length cannot be greater than max length")
                return {'CANCELLED'}
        
        # Process selection expansion
        edges_to_process = initial_edges.copy()
        selected_edges = set(initial_edges)
        
        while edges_to_process:
            current_edge = edges_to_process.pop(0)
            
            # Check connected edges through vertices
            for vert in current_edge.verts:
                for edge in vert.link_edges:
                    if edge not in selected_edges:
                        edge_length = edge.calc_length()
                        
                        # Check if edge length is within range
                        if min_val <= edge_length <= max_val:
                            edge.select = True
                            selected_edges.add(edge)
                            edges_to_process.append(edge)
        
        bmesh.update_edit_mesh(me)
        return {'FINISHED'}


classes = (
    MESH_OT_select_connected_length,
)
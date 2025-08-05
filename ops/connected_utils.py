"""Utility functions for connected selection operators"""

def get_initial_vertices_and_edges(context, bm):
    """Get vertices to start from and edges to check based on selection mode"""
    initial_verts = []
    edges_to_check = []
    
    # Get vertices based on selection mode
    if context.tool_settings.mesh_select_mode[0]:  # Vertex mode
        initial_verts = [v for v in bm.verts if v.select]
        # Get all edges connected to these vertices
        for vert in initial_verts:
            edges_to_check.extend(vert.link_edges)
    
    elif context.tool_settings.mesh_select_mode[1]:  # Edge mode
        selected_edges = [e for e in bm.edges if e.select]
        # Get vertices from selected edges
        for edge in selected_edges:
            initial_verts.extend(edge.verts)
        edges_to_check = selected_edges.copy()
    
    elif context.tool_settings.mesh_select_mode[2]:  # Face mode
        selected_faces = [f for f in bm.faces if f.select]
        # Get vertices from selected faces
        for face in selected_faces:
            initial_verts.extend(face.verts)
            edges_to_check.extend(face.edges)
    
    # Remove duplicates
    initial_verts = list(set(initial_verts))
    edges_to_check = list(set(edges_to_check))
    
    return initial_verts, edges_to_check
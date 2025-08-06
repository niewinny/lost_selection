# Lost Selection - Advanced Selection Tools for Blender

**Lost Selection** is a powerful Blender addon that extends the default selection capabilities with advanced operators for both Object and Edit modes. It provides intelligent selection tools based on object properties, mesh attributes, and connectivity patterns.

## Features Overview

The addon provides two main categories of selection tools:

1. **Object Mode Selection** - Select objects based on shared properties
2. **Edit Mode Selection** - Select connected mesh elements based on attributes

## Installation

1. Download the Lost Selection addon
2. In Blender, go to Edit > Preferences > Add-ons
3. Click "Install" and select the downloaded file
4. Enable "Lost Selection" addon

## Object Mode Selection Tools

### Select Similar Menu
Access via: **Select > Select Similar** or **Shift+Alt+S**

#### 1. Display Type
Selects all objects that have the same display type as the active object.

**Options:**
- **Extend**: Add to existing selection instead of replacing it

**Use Cases:**
- Quickly select all objects shown as wireframe
- Find all objects with bounding box display
- Group objects by their viewport display settings

#### 2. Rotation
Selects objects with exactly the same rotation values as the active object.

**Options:**
- **Extend**: Add to existing selection instead of replacing it

**Use Cases:**
- Find all objects with default rotation (0,0,0)
- Select duplicated objects that maintain the same orientation
- Identify aligned objects in architectural models

#### 3. Modifiers
Selects objects that have the same modifiers as the active object.

**Options:**
- **Extend**: Add to existing selection
- **Modifier Types**: Choose which modifier types to match (interactive dialog)

**Use Cases:**
- Select all objects with Subdivision Surface modifier
- Find objects with specific modifier combinations
- Manage modifier stacks across multiple objects

## Edit Mode Selection Tools

### Select Connected Menu
Access via: **Select > Select Connected** (in Edit Mode)

These tools select connected mesh elements based on specific attributes, allowing for intelligent selection propagation through your mesh topology.

#### 1. Crease
Selects connected edges or faces based on crease values.

**Comparison Modes:**
- **Equal**: Select edges with the same crease value as the selected edge
- **Greater**: Select edges with higher crease values
- **Less**: Select edges with lower crease values

**Use Cases:**
- Select all edges with subdivision crease settings
- Manage crease weights for subdivision modeling
- Find and adjust hard edges in subdivision surfaces

#### 2. Sharp
Selects connected edges or faces based on sharp marking.

**Comparison Modes:**
- **Equal**: Select edges with the same sharp state
- **Sharp**: Select only edges marked as sharp
- **Not Sharp**: Select only edges not marked as sharp

**Use Cases:**
- Select all sharp edges for normal splitting
- Manage smooth shading boundaries
- Clean up sharp edge marking

#### 3. Bevel Weight
Selects connected edges or faces based on bevel weight values.

**Comparison Modes:**
- **Equal**: Select edges with equal bevel weight
- **Greater**: Select edges with greater bevel weight
- **Less**: Select edges with less bevel weight

**Use Cases:**
- Select edges for bevel modifier control
- Manage beveling across complex models
- Fine-tune bevel weights for hard surface modeling

#### 4. Seam
Selects connected edges or faces based on UV seam marking.

**Comparison Modes:**
- **Equal**: Select edges with the same seam state
- **Seam**: Select only edges marked as seams
- **Not Seam**: Select only edges not marked as seams

**Use Cases:**
- Select all UV seams for inspection
- Extend seam selection along edges
- Clean up UV unwrapping seams

#### 5. Length (Edge Mode Only)
Selects connected edges based on length thresholds.

**Parameters:**
- **Min Length**: Minimum edge length to select (0 = use selected edge length)
- **Max Length**: Maximum edge length to select (0 = use selected edge length)

**Use Cases:**
- Select edges within specific size ranges
- Find and fix very small or very large edges
- Maintain consistent edge lengths in retopology

## Selection Modes Behavior

### Edge Selection Mode
- All connected edge tools work by propagating selection through connected edges
- Selection stops at boundaries or when attribute conditions aren't met
- Initial selection is preserved and extended

### Face Selection Mode
- Face selection tools select faces whose edges meet the specified criteria
- Works with sharp, seam, bevel weight, and crease attributes
- Useful for selecting surface regions based on edge properties

### Vertex Selection Mode
- Vertex selection is derived from edge selection
- Vertices are selected if they belong to selected edges

## Keyboard Shortcuts

- **Shift+Alt+S** (Object Mode): Open Select Similar menu

## Tips and Best Practices

1. **Use Extend Option**: Enable the Extend option to add to your current selection rather than replacing it

2. **Combine with Other Tools**: These selection tools work great with Blender's native selection tools like Select Linked (L) and Select More/Less (Ctrl+/-)

3. **Selection Flow**: The connected selection tools follow mesh topology, making them perfect for selecting continuous regions with specific properties

4. **Performance**: These tools are optimized for performance and work efficiently even on high-poly meshes

5. **Undo Support**: All operations support undo (Ctrl+Z) for easy experimentation

## Use Case Examples

### Hard Surface Modeling
- Use Sharp and Crease selection to manage edge hardness
- Bevel Weight selection for controlling bevel modifier
- Select Similar Modifiers to manage multiple objects

### UV Unwrapping
- Use Seam selection to review and adjust UV seams
- Combine with face selection to select UV islands

### Architectural Visualization
- Select Similar Rotation to find aligned objects
- Display Type selection to manage viewport performance
- Select Similar Modifiers for batch modifier management

### Retopology
- Length selection to find and fix edge length issues
- Connected selection to maintain edge flow

## Technical Details

- **Blender Version**: 4.2.0 or higher
- **License**: GPL-2.0-or-later
- **Category**: 3D View, Modeling, Mesh, Selection
- **Location**: View3D > Select Menu

## Support

For issues, feature requests, or contributions, visit:
https://github.com/niewinny/lost_selection

## Credits

Developed by ezelar.com
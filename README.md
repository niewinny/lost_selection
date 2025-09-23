# Lost Selection

Advanced selection tools for Blender that extend the default selection capabilities with intelligent operators for Object and Edit modes.

### Display Type
Selects objects with the same display type as the active object.
- **Extend**: Add to existing selection instead of replacing
- **Same Type**: Only select objects of the same type

### Material
Selects objects with similar materials as the active object.
- **Extend**: Add to existing selection instead of replacing
- **Match All**: Match all materials (instead of any material)

### Color
Selects objects with similar material viewport display colors.
- **Extend**: Add to existing selection instead of replacing
- **Tolerance**: Color tolerance for matching (0 = exact, 1 = any color)
- **Match Any**: Match if any material has similar color

### Rotation
Selects objects with exactly the same rotation values as the active object.
- **Extend**: Add to existing selection instead of replacing

### Modifiers
Selects objects that have the same modifiers as the active object.
- **Extend**: Add to existing selection instead of replacing
- **Modifier Types**: Interactive list to choose which modifiers to match

### Crease
Selects connected edges/faces based on crease values.
- **Comparison**: Equal / Greater / Less

### Sharp
Selects connected edges/faces based on sharp marking.
- **Comparison**: Equal / Sharp / Not Sharp

### Bevel Weight
Selects connected edges/faces based on bevel weight values.
- **Comparison**: Equal / Greater / Less

### Seam
Selects connected edges/faces based on UV seam marking.
- **Comparison**: Equal / Seam / Not Seam

### Length
Selects connected edges based on length thresholds (edge mode only).
- **Min Length**: Minimum edge length (0 = use selected edge)
- **Max Length**: Maximum edge length (0 = use selected edge)
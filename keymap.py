import bpy

# Store addon keymaps
addon_keymaps = []


def register():
    """Register keymaps for the addon"""
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if kc:
        # Object Mode keymap for Select Similar menu
        km = kc.keymaps.new(name='Object Mode', space_type='EMPTY')
        kmi = km.keymap_items.new('wm.call_menu', 'S', 'PRESS', shift=True, alt=True)
        kmi.properties.name = 'VIEW3D_MT_select_similar'
        addon_keymaps.append((km, kmi))


def unregister():
    """Unregister keymaps"""
    # Remove all registered keymaps
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

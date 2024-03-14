bl_info = {
    "name": "Node Editor Pie",
    "author": "Chedeville Victor",
    "description": "Pie menu to swith between node editor",
    "blender": (4, 0, 0),
    "version": (0, 0, 1, 0),
    "location": "Node Editor",
    "warning": "",
    "category": "3D View",
}

import bpy

class SwitchNodeEditor(bpy.types.Operator):
    bl_idname = "node.switch_to_shader_editor"
    bl_label = "Switch to Shader Editor"

    def execute(self, context):
        bpy.context.area.ui_type = 'ShaderNodeTree'
        context.space_data.shader_type = 'OBJECT'
        return {'FINISHED'}

class SwitchWorldEditor(bpy.types.Operator):
    bl_idname = "node.switch_to_world_editor"
    bl_label = "Switch to World Editor"

    def execute(self, context):
        bpy.context.area.ui_type = 'ShaderNodeTree'
        context.space_data.shader_type = 'WORLD'
        return {'FINISHED'}
    
class SwitchCompositorEditor(bpy.types.Operator):
    bl_idname = "node.switch_to_compositor_editor"
    bl_label = "Switch to Compositor Editor"

    def execute(self, context):
        bpy.context.area.ui_type = 'CompositorNodeTree'
        return {'FINISHED'}

class SwitchGeometryEditor(bpy.types.Operator):
    bl_idname = "node.switch_to_geometry_editor"
    bl_label = "Switch to Geometry Editor"

    def execute(self, context):
        bpy.context.area.ui_type = 'GeometryNodeTree'
        return {'FINISHED'}

class VIEW3D_MT_NODE_PIE_Menu(bpy.types.Menu):
    bl_idname = "VIEW3D_MT_NODE_PIE_Menu"
    bl_label = "Node Editor Pie Menu"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        pie.operator("node.switch_to_shader_editor", text="Shader", icon="NODE_MATERIAL")
        pie.operator("node.switch_to_world_editor", text="World", icon="WORLD_DATA")
        pie.operator("node.switch_to_geometry_editor", text="Geometry", icon="GEOMETRY_NODES")
        pie.operator("node.switch_to_compositor_editor", text="Compositor", icon="NODE_COMPOSITING")


def draw_switch_buttons(self, context):
    layout = self.layout

    if context.area.ui_type == 'ShaderNodeTree' and context.space_data.shader_type == 'OBJECT':
        row = layout.row(align=True)
        row.operator("node.switch_to_geometry_editor", text="", icon="GEOMETRY_NODES")
        row.operator("node.switch_to_shader_editor", text="", icon="NODE_MATERIAL", emboss=True, depress=True)
        row.operator("node.switch_to_world_editor", text="", icon="WORLD_DATA")
        row.operator("node.switch_to_compositor_editor", text="", icon="NODE_COMPOSITING")
    
    if context.area.ui_type == 'ShaderNodeTree' and context.space_data.shader_type == 'WORLD':
        row = layout.row(align=True)
        row.operator("node.switch_to_geometry_editor", text="", icon="GEOMETRY_NODES")
        row.operator("node.switch_to_shader_editor", text="", icon="NODE_MATERIAL")
        row.operator("node.switch_to_world_editor", text="", icon="WORLD_DATA", emboss=True, depress=True)
        row.operator("node.switch_to_compositor_editor", text="", icon="NODE_COMPOSITING")
    
    if context.area.ui_type == 'GeometryNodeTree':
        row = layout.row(align=True)
        row.operator("node.switch_to_geometry_editor", text="", icon="GEOMETRY_NODES", emboss=True, depress=True)
        row.operator("node.switch_to_shader_editor", text="", icon="NODE_MATERIAL")
        row.operator("node.switch_to_world_editor", text="", icon="WORLD_DATA")
        row.operator("node.switch_to_compositor_editor", text="", icon="NODE_COMPOSITING")
    
    if context.area.ui_type == 'CompositorNodeTree':
        row = layout.row(align=True)
        row.operator("node.switch_to_geometry_editor", text="", icon="GEOMETRY_NODES")
        row.operator("node.switch_to_shader_editor", text="", icon="NODE_MATERIAL")
        row.operator("node.switch_to_world_editor", text="", icon="WORLD_DATA")
        row.operator("node.switch_to_compositor_editor", text="", icon="NODE_COMPOSITING", emboss=True, depress=True)
    
def register():
    bpy.utils.register_class(SwitchNodeEditor)
    bpy.utils.register_class(SwitchCompositorEditor)
    bpy.utils.register_class(SwitchWorldEditor)
    bpy.utils.register_class(SwitchGeometryEditor)
    bpy.utils.register_class(VIEW3D_MT_NODE_PIE_Menu)
    bpy.types.NODE_HT_header.append(draw_switch_buttons)
    
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Node Editor', space_type='NODE_EDITOR')
    kmi = km.keymap_items.new('wm.call_menu_pie', 'SEMI_COLON', 'PRESS', ctrl=True, alt=True)
    kmi.properties.name = "VIEW3D_MT_NODE_PIE_Menu"
    
    kmi = km.keymap_items.new('node.switch_to_geometry_editor', 'ONE', 'PRESS')
    kmi = km.keymap_items.new('node.switch_to_shader_editor', 'TWO', 'PRESS')
    kmi = km.keymap_items.new('node.switch_to_world_editor', 'THREE', 'PRESS')
    kmi = km.keymap_items.new('node.switch_to_compositor_editor', 'FOUR', 'PRESS')

def unregister():
    bpy.utils.unregister_class(SwitchNodeEditor)
    bpy.utils.unregister_class(SwitchCompositorEditor)
    bpy.utils.unregister_class(SwitchWorldEditor)
    bpy.utils.unregister_class(SwitchGeometryEditor)
    bpy.utils.unregister_class(VIEW3D_MT_NODE_PIE_Menu)
    bpy.types.NODE_HT_header.remove(draw_switch_buttons)

if __name__ == "__main__":
    register()




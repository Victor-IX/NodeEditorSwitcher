bl_info = {
    "name": "Node Editor Switcher",
    "author": "Chedeville Victor",
    "description": "Pie menu, shorcut and quick access buttons for switching between different node editors",
    "blender": (4, 0, 0),
    "version": (1, 0),
    "location": "Node Editor",
    "category": "Node Editor",
}

import bpy
import rna_keymap_ui
from bpy.props import BoolProperty


class SwitchNodeEditor(bpy.types.Operator):
    bl_idname = "node.switch_to_shader_editor"
    bl_label = "Switch to Shader Editor"

    def execute(self, context):
        bpy.context.area.ui_type = "ShaderNodeTree"
        context.space_data.shader_type = "OBJECT"
        return {"FINISHED"}


class SwitchWorldEditor(bpy.types.Operator):
    bl_idname = "node.switch_to_world_editor"
    bl_label = "Switch to World Editor"

    def execute(self, context):
        bpy.context.area.ui_type = "ShaderNodeTree"
        context.space_data.shader_type = "WORLD"
        return {"FINISHED"}


class SwitchCompositorEditor(bpy.types.Operator):
    bl_idname = "node.switch_to_compositor_editor"
    bl_label = "Switch to Compositor Editor"

    def execute(self, context):
        bpy.context.area.ui_type = "CompositorNodeTree"
        return {"FINISHED"}


class SwitchGeometryEditor(bpy.types.Operator):
    bl_idname = "node.switch_to_geometry_editor"
    bl_label = "Switch to Geometry Editor"

    def execute(self, context):
        bpy.context.area.ui_type = "GeometryNodeTree"
        return {"FINISHED"}


class NODE_MT_NODE_PIE_Menu(bpy.types.Menu):
    bl_idname = "NODE_MT_NODE_PIE_Menu"
    bl_label = "Node Editor Pie Menu"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()

        pie.operator(
            "node.switch_to_shader_editor", text="Shader", icon="NODE_MATERIAL"
        )
        pie.operator("node.switch_to_world_editor", text="World", icon="WORLD_DATA")
        pie.operator(
            "node.switch_to_geometry_editor", text="Geometry", icon="GEOMETRY_NODES"
        )
        pie.operator(
            "node.switch_to_compositor_editor",
            text="Compositor",
            icon="NODE_COMPOSITING",
        )


def draw_switch_buttons(self, context):
    layout = self.layout
    if context.preferences.addons[__name__].preferences.enable_button:
        if (
            context.area.ui_type == "ShaderNodeTree"
            and context.space_data.shader_type == "OBJECT"
        ):
            row = layout.row(align=True)
            row.operator(
                "node.switch_to_geometry_editor", text="", icon="GEOMETRY_NODES"
            )
            row.operator(
                "node.switch_to_shader_editor",
                text="",
                icon="NODE_MATERIAL",
                emboss=True,
                depress=True,
            )
            row.operator("node.switch_to_world_editor", text="", icon="WORLD_DATA")
            row.operator(
                "node.switch_to_compositor_editor", text="", icon="NODE_COMPOSITING"
            )

        if (
            context.area.ui_type == "ShaderNodeTree"
            and context.space_data.shader_type == "WORLD"
        ):
            row = layout.row(align=True)
            row.operator(
                "node.switch_to_geometry_editor", text="", icon="GEOMETRY_NODES"
            )
            row.operator("node.switch_to_shader_editor", text="", icon="NODE_MATERIAL")
            row.operator(
                "node.switch_to_world_editor",
                text="",
                icon="WORLD_DATA",
                emboss=True,
                depress=True,
            )
            row.operator(
                "node.switch_to_compositor_editor", text="", icon="NODE_COMPOSITING"
            )

        if context.area.ui_type == "GeometryNodeTree":
            row = layout.row(align=True)
            row.operator(
                "node.switch_to_geometry_editor",
                text="",
                icon="GEOMETRY_NODES",
                emboss=True,
                depress=True,
            )
            row.operator("node.switch_to_shader_editor", text="", icon="NODE_MATERIAL")
            row.operator("node.switch_to_world_editor", text="", icon="WORLD_DATA")
            row.operator(
                "node.switch_to_compositor_editor", text="", icon="NODE_COMPOSITING"
            )

        if context.area.ui_type == "CompositorNodeTree":
            row = layout.row(align=True)
            row.operator(
                "node.switch_to_geometry_editor", text="", icon="GEOMETRY_NODES"
            )
            row.operator("node.switch_to_shader_editor", text="", icon="NODE_MATERIAL")
            row.operator("node.switch_to_world_editor", text="", icon="WORLD_DATA")
            row.operator(
                "node.switch_to_compositor_editor",
                text="",
                icon="NODE_COMPOSITING",
                emboss=True,
                depress=True,
            )


class Preferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    enable_button: BoolProperty(
        name="Quick Access Button",
        description="Enable quick access buttons for switching between different node editors",
        default=True,
    )  # type: ignore

    def draw(self, context):
        layout = self.layout

        row = layout.row(align=True)
        row.prop(self, "enable_button")

        box = layout.box()
        box.label(text="Hotkey")
        wm = context.window_manager
        kc = wm.keyconfigs.user
        km = kc.keymaps["Node Editor"]

        kmi = km.keymap_items.get("wm.call_menu_pie")
        box.context_pointer_set("keymap", km)
        rna_keymap_ui.draw_kmi([], kc, km, kmi, box, 0)

        kmi = km.keymap_items.get("node.switch_to_geometry_editor")
        box.context_pointer_set("keymap", km)
        rna_keymap_ui.draw_kmi([], kc, km, kmi, box, 0)

        kmi = km.keymap_items.get("node.switch_to_shader_editor")
        box.context_pointer_set("keymap", km)
        rna_keymap_ui.draw_kmi([], kc, km, kmi, box, 0)

        kmi = km.keymap_items.get("node.switch_to_world_editor")
        box.context_pointer_set("keymap", km)
        rna_keymap_ui.draw_kmi([], kc, km, kmi, box, 0)

        kmi = km.keymap_items.get("node.switch_to_compositor_editor")
        box.context_pointer_set("keymap", km)
        rna_keymap_ui.draw_kmi([], kc, km, kmi, box, 0)


addon_keymaps = []


def registerKeymaps():
    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        km = wm.keyconfigs.addon.keymaps.get("Node Editor")
        if not km:
            km = wm.keyconfigs.addon.keymaps.new(
                name="Node Editor", space_type="NODE_EDITOR"
            )

        kmi = km.keymap_items.new("wm.call_menu_pie", "E", "PRESS")
        kmi.properties.name = "NODE_MT_NODE_PIE_Menu"
        addon_keymaps.append((km, kmi))

        kmi = km.keymap_items.new("node.switch_to_geometry_editor", "ONE", "PRESS")
        addon_keymaps.append((km, kmi))

        kmi = km.keymap_items.new("node.switch_to_shader_editor", "TWO", "PRESS")
        addon_keymaps.append((km, kmi))

        kmi = km.keymap_items.new("node.switch_to_world_editor", "THREE", "PRESS")
        addon_keymaps.append((km, kmi))

        kmi = km.keymap_items.new("node.switch_to_compositor_editor", "FOUR", "PRESS")
        addon_keymaps.append((km, kmi))


def unregisterKeymaps():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


classes = (
    SwitchNodeEditor,
    SwitchCompositorEditor,
    SwitchWorldEditor,
    SwitchGeometryEditor,
    NODE_MT_NODE_PIE_Menu,
    Preferences,
)


def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)
    bpy.types.NODE_HT_header.append(draw_switch_buttons)
    registerKeymaps()


def unregister():
    unregisterKeymaps()
    from bpy.utils import unregister_class

    for cls in reversed(classes):
        unregister_class(cls)

    bpy.types.NODE_HT_header.remove(draw_switch_buttons)

    registerKeymaps()


if __name__ == "__main__":
    register()

import bpy
import rna_keymap_ui
from bpy.props import EnumProperty


class SwitchNodeEditorBase(bpy.types.Operator):
    bl_idname = ""
    bl_label = ""

    ui_type: str
    shader_type: str = ""

    def execute(self, context):
        bpy.context.area.ui_type = self.ui_type
        if self.shader_type:
            context.space_data.shader_type = self.shader_type
        return {"FINISHED"}


class SwitchNodeEditor(SwitchNodeEditorBase):
    bl_idname = "node.switch_to_shader_editor"
    bl_label = "Switch to Shader Editor"
    ui_type = "ShaderNodeTree"
    shader_type = "OBJECT"


class SwitchWorldEditor(SwitchNodeEditorBase):
    bl_idname = "node.switch_to_world_editor"
    bl_label = "Switch to World Editor"
    ui_type = "ShaderNodeTree"
    shader_type = "WORLD"


class SwitchCompositorEditor(SwitchNodeEditorBase):
    bl_idname = "node.switch_to_compositor_editor"
    bl_label = "Switch to Compositor Editor"
    ui_type = "CompositorNodeTree"


class SwitchGeometryEditor(SwitchNodeEditorBase):
    bl_idname = "node.switch_to_geometry_editor"
    bl_label = "Switch to Geometry Editor"
    ui_type = "GeometryNodeTree"


class NODE_MT_NODE_PIE_Menu(bpy.types.Menu):
    bl_idname = "NODE_MT_NODE_PIE_Menu"
    bl_label = "Node Editor Pie Menu"

    def draw(self, context):
        layout = self.layout.menu_pie()
        layout.operator("node.switch_to_shader_editor", text="Shader", icon="NODE_MATERIAL")
        layout.operator("node.switch_to_world_editor", text="World", icon="WORLD_DATA")
        layout.operator("node.switch_to_geometry_editor", text="Geometry", icon="GEOMETRY_NODES")
        layout.operator("node.switch_to_compositor_editor", text="Compositor", icon="NODE_COMPOSITING")


def switch_button(row, operator, icon, active=False):
    return row.operator(operator, text="", icon=icon, depress=active)


def draw_switch_buttons(self, context):
    if context.preferences.addons[__package__].preferences.button_location != "OFF":
        layout = self.layout
        row = layout.row(align=True)
        area = context.area
        space_data = context.space_data

        buttons = [
            ("ShaderNodeTree", "OBJECT", "node.switch_to_shader_editor", "NODE_MATERIAL"),
            ("ShaderNodeTree", "WORLD", "node.switch_to_world_editor", "WORLD_DATA"),
            ("GeometryNodeTree", "", "node.switch_to_geometry_editor", "GEOMETRY_NODES"),
            ("CompositorNodeTree", "", "node.switch_to_compositor_editor", "NODE_COMPOSITING"),
        ]

        for ui_type, shader_type, operator, icon in buttons:
            active = area.ui_type == ui_type and (shader_type == "" or space_data.shader_type == shader_type)
            switch_button(row, operator, icon, active)


class Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    button_location: EnumProperty(
        name="Quick Access Button",
        description="Location of the quick access buttons for switching between different node editors located in the header of the node editor",
        items=[
            ("OFF", "Off", "Do not display the button in the header"),
            ("LEFT", "Left", "Place the button on the left side of the UI"),
            ("RIGHT", "Right", "Place the button on the right side of the UI"),
        ],
        default="OFF",
        update=lambda self, context: update_header_buttons(),
    )  # type: ignore

    def draw(self, context):
        layout = self.layout
        layout.row(align=True).prop(self, "button_location")

        box = layout.box()
        box.label(text="Hotkey")
        wm = context.window_manager
        kc = wm.keyconfigs.user
        km = kc.keymaps["Node Editor"]

        for keymap in [
            "wm.call_menu_pie",
            "node.switch_to_geometry_editor",
            "node.switch_to_shader_editor",
            "node.switch_to_world_editor",
            "node.switch_to_compositor_editor",
        ]:
            kmi = km.keymap_items.get(keymap)
            box.context_pointer_set("keymap", km)
            rna_keymap_ui.draw_kmi([], kc, km, kmi, box, 0)


addon_keymaps = []


def registerKeymaps():
    wm = bpy.context.window_manager
    if wm.keyconfigs.addon:
        km = wm.keyconfigs.addon.keymaps.get("Node Editor")
        if not km:
            km = wm.keyconfigs.addon.keymaps.new(name="Node Editor", space_type="NODE_EDITOR")

        for key, operator in [
            ("E", "wm.call_menu_pie"),
            ("ONE", "node.switch_to_geometry_editor"),
            ("TWO", "node.switch_to_shader_editor"),
            ("THREE", "node.switch_to_world_editor"),
            ("FOUR", "node.switch_to_compositor_editor"),
        ]:
            kmi = km.keymap_items.new(operator, key, "PRESS")
            if operator == "wm.call_menu_pie":
                kmi.properties.name = "NODE_MT_NODE_PIE_Menu"
            addon_keymaps.append((km, kmi))


classes = (
    SwitchNodeEditor,
    SwitchCompositorEditor,
    SwitchWorldEditor,
    SwitchGeometryEditor,
    NODE_MT_NODE_PIE_Menu,
    Preferences,
)


def unregisterKeymaps():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


def update_header_buttons():
    unregister_header_buttons()
    register_header_buttons()


def register_header_buttons():
    if bpy.context.preferences.addons[__package__].preferences.button_location == "LEFT":
        bpy.types.NODE_HT_header.prepend(draw_switch_buttons)
    else:
        bpy.types.NODE_HT_header.append(draw_switch_buttons)


def unregister_header_buttons():
    bpy.types.NODE_HT_header.remove(draw_switch_buttons)


def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)
    register_header_buttons()
    registerKeymaps()


def unregister():
    unregisterKeymaps()
    unregister_header_buttons()
    from bpy.utils import unregister_class

    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()
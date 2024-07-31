import bpy
import rna_keymap_ui
from bpy.props import EnumProperty, BoolProperty


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
        pref = context.preferences.addons[__package__].preferences
        if pref.pie_menu != "OFF":
            layout = self.layout.menu_pie()
            if pref.show_material:
                layout.operator("node.switch_to_shader_editor", text="Shader", icon="NODE_MATERIAL")
            if pref.show_world:    
                layout.operator("node.switch_to_world_editor", text="World", icon="WORLD_DATA")
            if pref.show_geometry_nodes:
                layout.operator("node.switch_to_geometry_editor", text="Geometry", icon="GEOMETRY_NODES")
            if pref.show_compositor:
                layout.operator("node.switch_to_compositor_editor", text="Compositor", icon="NODE_COMPOSITING")


def switch_button(row, operator, icon, active=False):
    return row.operator(operator, text="", icon=icon, depress=active)


def draw_switch_buttons(self, context):
    pref = context.preferences.addons[__package__].preferences
    if pref.button_location != "OFF":
        layout = self.layout
        row = layout.row(align=True)
        area = context.area
        space_data = context.space_data

        buttons = []

        if pref.show_material:
            buttons.append(("ShaderNodeTree", "OBJECT", "node.switch_to_shader_editor", "NODE_MATERIAL"))
        if pref.show_world:
            buttons.append(("ShaderNodeTree", "WORLD", "node.switch_to_world_editor", "WORLD_DATA"))
        if pref.show_geometry_nodes:
            buttons.append(("GeometryNodeTree", "", "node.switch_to_geometry_editor", "GEOMETRY_NODES"))
        if pref.show_compositor:
            buttons.append(("CompositorNodeTree", "", "node.switch_to_compositor_editor", "NODE_COMPOSITING"))

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

    show_material: BoolProperty(
        name="Material",
        description="Show the material nodes in the node editor",
        default=True,
    )  # type: ignore

    show_world: BoolProperty(
        name="World",
        description="Show the world nodes in the node editor",
        default=True,
    )  # type: ignore

    show_geometry_nodes: BoolProperty(
        name="Geometry Nodes",
        description="Show the geometry nodes in the node editor",
        default=True,
    )  # type: ignore
    
    show_compositor: BoolProperty(
        name="Compositor",
        description="Show the compositor nodes in the node editor",
        default=True,
    )  # type: ignore
    
    pie_menu: EnumProperty(
        name="Pie Menu",
        description="Choose the pie menu to use for switching between different node editors",
        items=[
            ("ON", "On", "Enable the pie menu for switching between different node editors"),
            ("OFF", "Off", "Disable the pie menu for switching between different node editors"),
        ],
        default="ON",
    )  # type: ignore

    def draw(self, context):
        pref = context.preferences.addons[__package__].preferences

        layout = self.layout
        layout.row(align=True).prop(self, "button_location")

        if pref.button_location != "OFF":
            box = layout.box()
            box.label(text="Show Editor")
            box.row(align=True).prop(self, "show_material")
            box.row(align=True).prop(self, "show_world")
            box.row(align=True).prop(self, "show_geometry_nodes")
            box.row(align=True).prop(self, "show_compositor")

        layout.row().prop(self, "pie_menu")
        
        if pref.pie_menu != "OFF":
            box = layout.box()
            box.label(text="Show Editor")
            box.row(align=True).prop(self, "show_material")
            box.row(align=True).prop(self, "show_world")
            box.row(align=True).prop(self, "show_geometry_nodes")
            box.row(align=True).prop(self, "show_compositor")
        
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

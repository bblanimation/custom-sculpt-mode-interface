# Copyright (C) 2019 Christopher Gearhart
# chris@bblanimation.com
# http://bblanimation.com/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# System imports
# NONE!

# Blender imports
import bpy
import bmesh

# Addon imports
from .custom_sculpt_mode import *
from ..functions import *
from ..addon_common.common import ui


class SCULPT_OT_region_painter(SCENE_OT_custom_sculpt_mode):
    """  """
    bl_idname = "sculpt.region_painter"
    bl_label = "Region Painter"
    bl_description = ""

    #############################################
    # overwriting functions from Wax Dropper submodule

    def start_post(self):
        self.obj = bpy.context.active_object
        self.painted_verts = list()

        scn = bpy.context.scene
        paint_settings = scn.tool_settings.unified_paint_settings
        paint_settings.use_locked_size = True
        paint_settings.unprojected_radius = 0.5
        brush = bpy.data.brushes['Mask']
        brush.strength = 2
        brush.stroke_method = 'SPACE'
        scn.tool_settings.sculpt.brush = brush
        scn.tool_settings.sculpt.use_symmetry_x = False
        scn.tool_settings.sculpt.use_symmetry_y = False
        scn.tool_settings.sculpt.use_symmetry_z = False
        bpy.ops.brush.curve_preset(shape='MAX')

    def ui_setup(self):
        # instructions
        self.instructions = {
            "do something": "Do something...",
            "do something else": "Do something else...",
        }

        # UI Box functionality
        def get_blobsize(): return self.sculpt_opts["size"]
        def get_blobsize_print(): return "%0.3f" % self.sculpt_opts["size"]
        def set_blobsize(v): self.sculpt_opts["size"] = min(max(0.001, float(v)),8.0)

        def get_action(): return self.sculpt_opts["action"]
        def set_action(v): self.sculpt_opts["action"] = v

        def mode_getter(): return self._state
        def mode_setter(m): self.fsm_change(m)

        # UPPER LEFT WINDOW, mode setters and commit/cancel buttons
        self.tools_panel = self.wm.create_window('Sculpt Tools', {'pos':7, 'movable':True, 'bgcolor':(0.50, 0.50, 0.50, 0.90)})
        precut_container = self.tools_panel.add(ui.UI_Container()) # TODO: make this rounded
        self.cancel_button = precut_container.add(ui.UI_Button('Delete', self.delete_painted, align=0))
        self.cancel_button = precut_container.add(ui.UI_Button('Separate', self.separate_painted, align=0))
        self.cancel_button = precut_container.add(ui.UI_Button('Duplicate', self.duplicate_painted, align=0))

        segmentation_container = self.tools_panel.add(ui.UI_Container())
        self.finish_frame = segmentation_container.add(ui.UI_Frame('Finish Tools'))
        self.commit_button = self.finish_frame.add(ui.UI_Button('Commit', self.done, align=0))
        self.cancel_button = self.finish_frame.add(ui.UI_Button('Cancel', lambda:self.done(cancel=True), align=0))

        #####################################
        ### Collapsible Help and Options   ##
        #####################################
        self.info_panel = self.wm.create_window('Sculpt Mode Help',
                                                {'pos':9,
                                                 'movable':True,
                                                 'bgcolor':(0.50, 0.50, 0.50, 0.90)})

        collapse_container = self.info_panel.add(ui.UI_Collapsible('Instructions     ', collapsed=False))
        self.inst_paragraphs = [collapse_container.add(ui.UI_Markdown('', min_size=(100,10), max_size=(250, 20))) for i in range(2)]
        self.set_ui_text()
        #for i in self.inst_paragraphs: i.visible = False
        # self.options_frame = self.info_panel.add(ui.UI_Frame('Tool Options'))
        # self.options_frame.add(ui.UI_Number("Size", get_blobsize, set_blobsize, fn_get_print_value=get_blobsize_print, fn_set_print_value=set_blobsize))
        # self.wax_action_options = self.options_frame.add(ui.UI_Options(get_action, set_action, label="Action: ", vertical=True))
        # self.wax_action_options.add_option("do something")
        # self.wax_action_options.add_option("do something else")
        # self.wax_action_options.add_option("none")

    def delete_painted(self):
        last_mode = bpy.context.mode
        bpy.ops.object.mode_set(mode='OBJECT')

        obj = bpy.context.active_object

        bme = bmesh.new()
        bme.from_mesh(obj.data)

        mask = bme.verts.layers.paint_mask.verify()

        delete = [v for v in bme.verts if v[mask] > 0]
        bmesh.ops.delete(bme, geom=delete, context=1)

        bme.to_mesh(obj.data)
        bme.free()
        obj.data.update()

        bpy.ops.object.mode_set(mode=last_mode)

    def separate_painted(self):
        last_mode = bpy.context.mode
        bpy.ops.object.mode_set(mode='EDIT')

        obj = bpy.context.active_object
        bpy.ops.mesh.select_all(action='DESELECT')

        bpy.ops.object.mode_set(mode='OBJECT')

        obj_dup = bpy.data.objects.new(obj.name + "_dup", obj.data.copy())

        # bme = bmesh.new()
        # bme.from_mesh(obj.data)
        #
        # mask = bme.verts.layers.paint_mask.verify()
        # delete = [v for v in bme.verts if v[mask] == 0]
        # bmesh.ops.delete(bme, geom=delete, context=1)
        #
        # bme.to_mesh(obj.data)
        # bme.free()
        # obj.data.update()
        #
        # bme = bmesh.new()
        # bme.from_mesh(obj.data)
        #
        # link_object(obj_dup)

        bme = bmesh.new()
        bme.from_mesh(obj.data)
        bme_dup = bme.copy()

        mask = bme.verts.layers.paint_mask.verify()
        delete = [v for v in bme.verts if v[mask] > 0]
        bmesh.ops.delete(bme, geom=delete, context=1)

        bme.to_mesh(obj.data)
        bme.free()
        obj.data.update()

        mask = bme_dup.verts.layers.paint_mask.verify()
        delete = [f for f in bme_dup.faces if all([v[mask] == 0 for v in f.verts])]
        bmesh.ops.delete(bme_dup, geom=delete, context=5)

        bme_dup.to_mesh(obj_dup.data)
        bme_dup.free()
        obj_dup.data.update()
        link_object(obj_dup)

        bpy.ops.object.mode_set(mode=last_mode)

    def duplicate_painted(self):
        last_mode = bpy.context.mode
        bpy.ops.object.mode_set(mode='OBJECT')

        obj = bpy.context.active_object
        obj_dup = bpy.data.objects.new(obj.name + "_dup", obj.data.copy())

        bme = bmesh.new()
        bme.from_mesh(obj.data)

        mask = bme.verts.layers.paint_mask.verify()

        delete = [v for v in bme.verts if v[mask] == 0]
        bmesh.ops.delete(bme, geom=delete, context=1)

        bme.to_mesh(obj_dup.data)
        bme.free()
        obj_dup.data.update()
        link_object(obj_dup)

        bpy.ops.object.mode_set(mode=last_mode)

    #############################################

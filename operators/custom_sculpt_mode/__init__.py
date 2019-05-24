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

# Addon imports
from .sculpt_ui_init import Sculpt_UI_Init
# from .sculpt_ui_draw import Sculpt_UI_Draw
from .sculpt_states import Sculpt_States
from ...functions import *
from ...addon_common.cookiecutter.cookiecutter import CookieCutter
from ...addon_common.common.decorators import PersistentOptions


@PersistentOptions()
class SculptOptions:
    defaults = {
        "action": "none",
        "size": 1,
        "position": 9,
    }


class SCENE_OT_custom_sculpt_mode(Sculpt_UI_Init, Sculpt_States, CookieCutter):
    """ Forces sculpt mode with custom interface """
    operator_id    = "scene.custom_sculpt_mode"
    bl_idname      = "scene.custom_sculpt_mode"
    bl_label       = "Sculpt Mode"
    bl_description = "Forces sculpt mode with custom interface"
    bl_space_type  = "VIEW_3D"
    bl_region_type = "UI" if b280() else "TOOLS"

    ################################################
    # CookieCutter Operator methods

    @classmethod
    def can_start(cls, context):
        """ Start only if editing a mesh """
        ob = context.active_object
        return (ob and ob.type == "MESH" and context.mode == "OBJECT")

    def start(self):
        """ Custom Sculpt Mode is starting """
        scn = bpy.context.scene

        bpy.ops.ed.undo_push()  # push current state to undo

        self.header_text_set("Sculpt Mode")
        self.cursor_modal_set("CROSSHAIR")
        self.manipulator_hide()
        try:
            bpy.ops.screen.back_to_previous()
        except:
            pass
        # bpy.ops.screen.screen_full_area()
        bpy.ops.view3d.toolshelf()  # hide tool shelf

        self.sculpt_opts = SculptOptions()

        self.starting_mode = bpy.context.mode
        bpy.ops.object.mode_set(mode='SCULPT')

        self.ui_setup()
        self.ui_setup_post()
        self.start_post()


    def end_commit(self):
        """ Commit changes to mesh! """
        bpy.ops.object.mode_set(mode='OBJECT')
        self.end_commit_post()

    def end_cancel(self):
        """ Cancel changes """
        bpy.ops.object.mode_set(mode=self.starting_mode)
        bpy.ops.ed.undo()   # undo everything

    def end(self):
        """ Restore everything, because we're done """
        self.manipulator_restore()
        self.header_text_restore()
        self.cursor_modal_restore()
        # bpy.ops.view3d.toolshelf()  # hide tool shelf
        # bpy.ops.screen.back_to_previous()

    def update(self):
        """ Check if we need to update any internal data structures """
        pass

    def should_pass_through(self, context, event):
        # TODO: BUG... this allows anything to pass through. Is the context being overwritten somewhere in cookiecutter?
        if context.area.type == "VIEW_3D":
            return True
        return False

    ###################################################
    # class methods

    def do_something(self):
        pass

    def do_something_else(self):
        pass

    #############################################
    # Subclassing functions

    def ui_setup_post(self):
        pass

    def start_post(self):
        pass

    def end_commit_post(self):
        pass

    #############################################

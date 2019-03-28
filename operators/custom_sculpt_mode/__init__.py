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
from ..functions import *
from ..addon_common.cookiecutter.cookiecutter import CookieCutter
from ..addon_common.common.decorators import PersistentOptions


@PersistentOptions()
class SculptOptions:
    defaults = {
        "action": "none",
        "size": 1,
        "position": 9,
    }


class SCENE_OT_custom_sculpt_mode(Sculpt_UI_Init, Sculpt_UI_Draw, Sculpt_States, CookieCutter):
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
        return (ob and ob.type == "MESH" and context.mode == "EDIT_MESH")

    def start(self):
        """ ExtruCut tool is starting """
        scn = bpy.context.scene

        bpy.ops.ed.undo_push()  # push current state to undo

        self.header_text_set("Sculpt Mode")
        self.cursor_modal_set("CROSSHAIR")
        self.manipulator_hide()

        self.sculpt_opts = SculptOptions()

        self.ui_setup()


    def end_commit(self):
        """ Commit changes to mesh! """
        pass

    def end_cancel(self):
        """ Cancel changes """
        bpy.ops.ed.undo()   # undo everything

    def end(self):
        """ Restore everything, because we're done """
        self.manipulator_restore()
        self.header_text_restore()
        self.cursor_modal_restore()

    def update(self):
        """ Check if we need to update any internal data structures """
        pass

    ###################################################
    # class methods

    def do_something(self):
        pass

    def do_something_else(self):
        pass

    #############################################

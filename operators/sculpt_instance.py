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

    def end_commit_pre(self):
        # bme = bmesh.new()
        # bme.from_mesh(self.obj.data)
        for v in self.painted_verts:
            pass  # remove(v)

    #############################################

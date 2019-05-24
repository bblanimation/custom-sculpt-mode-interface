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

        scn = bpy.context.scene
        paint_settings = scn.tool_settings.unified_paint_settings
        paint_settings.use_locked_size = True
        paint_settings.unprojected_radius = .5
        brush = bpy.data.brushes['Mask']
        brush.strength = 2
        brush.stroke_method = 'SPACE'
        scn.tool_settings.sculpt.brush = brush
        scn.tool_settings.sculpt.use_symmetry_x = False
        scn.tool_settings.sculpt.use_symmetry_y = False
        scn.tool_settings.sculpt.use_symmetry_z = False
        bpy.ops.brush.curve_preset(shape='MAX')

    def end_commit_post(self):

        obj = bpy.context.active_object

        bme = bmesh.new()
        bme.from_mesh(obj.data)

        mask = bme.verts.layers.paint_mask.verify()

        print('There are %i verts in the bmesh' % len(bme.verts))
        delete = []
        for v in bme.verts:
            if v[mask] > 0:
                delete.append(v)

        print('Deleting %i verts' % len(delete))
        bmesh.ops.delete(bme, geom=delete, context=1)

        bme.to_mesh(obj.data)
        bme.free()
        obj.data.update()

    #############################################

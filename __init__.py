# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

bl_info = {
    "name": "New Planetary System",
    "author": "",
    "version": (0, 1),
    "blender": (2, 79, 0),
    "location": "View3D > Add > Mesh > New Planetary System",
    "description": "Adds a new Planetary System",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
    }

import os
import json
import bpy
from mathutils import Vector
from bpy.types import Operator
from bpy.props import FloatVectorProperty
from bpy_extras.object_utils import AddObjectHelper, object_data_add

def readJsonFile(file_path):
  """docstring for readJsonFile"""
  with open(file_path, 'r') as content_file:
    return json.loads(content_file.read())

def add_planet(name, radius, distance):
  """docstring for add_planet"""
  bpy.ops.mesh.primitive_ico_sphere_add(
      subdivisions = 8,
      size = radius,
      location = (0.0, distance, 0.0),
      rotation = (0.0, 0.0, 0.0));
  ob = bpy.context.object
  ob.name = name
  ob.show_name = True
  me = ob.data
  me.name = name + '-' + 'Mesh'
  return ob

def add_object(self, context):
  BASE_DIR = os.path.dirname(os.path.realpath(__file__))
  JSON_FILE = 'planetaty-characteristics.json'
  file_path = os.path.join(BASE_DIR, JSON_FILE)
  planetaryData = readJsonFile(file_path)

  """ A.U. in km"""
  AU = float(149597870.7)
  FACTOR = float(100000000)
  for name, properties in planetaryData.items():
    """ (A.U.) """
    distance = ( float(properties['distance']) * AU) / FACTOR
    """ km """
    radius = ( float(properties['diameter']) / 2) / FACTOR
    add_planet(name, radius, distance)


class OBJECT_OT_add_object(Operator, AddObjectHelper):
  """Create a new Planetary System"""
  bl_idname = "mesh.add_object"
  bl_label = "Add Planetary System"
  bl_options = {'REGISTER', 'UNDO'}

  scale = FloatVectorProperty(
      name="scale",
      default=(1.0, 1.0, 1.0),
      subtype='TRANSLATION',
      description="scaling",
      )

  def execute(self, context):

    add_object(self, context)

    return {'FINISHED'}


# Registration

def add_object_button(self, context):
  self.layout.operator(
      OBJECT_OT_add_object.bl_idname,
      text="Add Planetary System",
      icon='PLUGIN')


  # This allows you to right click on a button and link to the manual
def add_object_manual_map():
  url_manual_prefix = "https://docs.blender.org/manual/en/dev/"
  url_manual_mapping = ( ("bpy.ops.mesh.add_object", "editors/3dview/object"),)
  return url_manual_prefix, url_manual_mapping


def register():
  bpy.utils.register_class(OBJECT_OT_add_object)
  bpy.utils.register_manual_map(add_object_manual_map)
  bpy.types.INFO_MT_mesh_add.append(add_object_button)


def unregister():
  bpy.utils.unregister_class(OBJECT_OT_add_object)
  bpy.utils.unregister_manual_map(add_object_manual_map)
  bpy.types.INFO_MT_mesh_add.remove(add_object_button)

if __name__ == "__main__":
    register()

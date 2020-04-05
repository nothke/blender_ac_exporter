bl_info = {
    "name": "AC Export",
    "category": "Object",
}

import bpy
import os
from bpy.props import IntProperty
from bpy.props import StringProperty

# OPERATOR

class ACExportOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.ac_export"
    bl_label = "AC Export"
    
    layer = IntProperty(default=0)
    filename = StringProperty(default='ac_export')

    #@classmethod
    #def poll(cls, context):
    #    return context.active_object is not None

    def execute(self, context):
        #main(context, self.layer, self.filename)

        layer = self.layer
        filename = self.filename

        basedir = os.path.dirname(bpy.data.filepath)

        if not basedir:
            raise Exception("Blend file is not saved")

        fpath = basedir + '/' + filename
            
        scene = bpy.context.scene

        bpy.context.scene.layers[layer] = True
        #bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.select_by_layer(match='SHARED', extend=False, layers=layer+1)

        if not bpy.context.selected_objects:
            raise Exception("No objects found in this layer")

        #unlink object data
        bpy.ops.object.make_single_user(object=True, obdata=True, material=False, texture=False, animation=False)

        selection = bpy.context.selected_objects

        #bpy.ops.object.convert(target='MESH') # not working! context is incorrect

        #TODO: make sure all objects have materials
        #for obj in selection:
            #print(obj)
        #    obj.select = True
        #    scene.objects.active = obj
        #    bpy.ops.object.convert(target='MESH')

            #mesh = obj.data
            
            #if mesh:
            #    print(len(mesh.vertices))

        #export
        bpy.ops.export_scene.fbx(
            filepath=fpath + ".fbx", 
            version='BIN7400',
            global_scale=0.01,
            apply_unit_scale=False,
            use_selection=True,
            object_types={'EMPTY', 'MESH', 'OTHER'})

        print('Finished AC export to ' + fpath + ' for layer: ' + str(layer))

        #reload 
        #bpy.ops.wm.revert_mainfile()


        return {'FINISHED'}

# UI PANEL

class ACExportPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "AC Exporter"
    bl_idname = "OBJECT_PT_hello"
    
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'AC Exporter'

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        row = layout.row()
        row.prop(scene, 'acexport_layer')

        row = layout.row()
        row.prop(scene, 'acexport_filename')

        row = layout.row()
        op = row.operator('object.ac_export', text='Export FBX')
        op.layer = scene.acexport_layer
        op.filename = scene.acexport_filename

        row = layout.row()
        row.label('Important:')

        row = layout.row()
        row.label('Save before pressing export')

        row = layout.row()
        row.label('Revert after export!')

def register():
    
    bpy.utils.register_class(ACExportOperator)
    print('operator registered')

    # register properties
    bpy.types.Scene.acexport_layer = bpy.props.IntProperty(
        name="Layer",
        description="Export all objects from this layer",
        default = 1)

    bpy.types.Scene.acexport_filename = bpy.props.StringProperty(
        name="Filename",
        description="Filename",
        default = 'ac_export')
    print('properties registered')

    bpy.utils.register_class(ACExportPanel)
    print('panel registered')

def unregister():
    bpy.utils.unregister_class(ACExportOperator)
    bpy.utils.unregister_class(ACExportPanel)
    del bpy.types.Scene.acexport_layer
    del bpy.types.Scene.acexport_filename

if __name__ == "__main__":
    register()

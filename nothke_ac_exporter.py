bl_info = {
    "name": "AC Export",
    "category": "Object",
    "blender": (2, 80, 0)
}

import bpy
import os
from bpy.props import IntProperty
from bpy.props import StringProperty

# OPERATOR

def recurLayerCollection(layerColl, collName):
    found = None
    if (layerColl.name == collName):
        return layerColl
    for layer in layerColl.children:
        found = recurLayerCollection(layer, collName)
        if found:
            return found

class NOTHKE_OT_ACExport(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.ac_export"
    bl_label = "AC Export"
    
    collectionName: StringProperty(default='EXPORT')
    filename: StringProperty(default='ac_export')

    def execute(self, context):
        #main(context, self.layer, self.filename)

        #layer = self.layer
        collectionName = self.collectionName
        filename = self.filename

        basedir = os.path.dirname(bpy.data.filepath)

        if not basedir:
            raise Exception("Blend file is not saved")

        fpath = basedir + '/' + filename
            
        scene = bpy.context.scene
        
        # Deselect all
        bpy.ops.object.select_all(action='DESELECT')

        # Find collection
        lc = bpy.context.view_layer.layer_collection
        layerColl = recurLayerCollection(lc, collectionName)
        
        if layerColl is None:
            raise Exception("Collection " + collectionName + " doesn't exist!")
            
        print('Found collection: ' + layerColl.name)
        bpy.context.view_layer.active_layer_collection = layerColl

        # select all in collection
        bpy.ops.object.select_same_collection(collection = collectionName)

        # check if objects exist
        if not bpy.context.selected_objects:
            raise Exception("" + collectionName + " collection is empty!")

        # unlink object data
        bpy.ops.object.make_single_user(type='SELECTED_OBJECTS', object=True, obdata=True, material=False, animation=False)
        print('Unlinked objects')

        selection = bpy.context.selected_objects

        #bpy.ops.object.convert(target='MESH') # not working! context is incorrect

        # make sure all objects..
        for ob in bpy.context.selected_editable_objects:
            # ..are meshes,
            if ob.type != "MESH":
                raise Exception("Object " + ob.name + " is not a valid mesh")

            # ..have at least 1 material slot,
            if not ob.material_slots:
                raise Exception("Object " + ob.name + " has no materials!")

            # ..have materials assigned to all slots,
            for slot in ob.material_slots:
                if slot.material is None:
                    raise Exception(ob.name + " has an empty slot without assigned material")

            # ..are not vertexless
            #if len(ob.data.vertices) > 0:
                #raise Exception("Object " + ob.name + " has no vertices")

            # ..don't have more than 65535 vertices
            if len(ob.data.vertices) > 65535:
                raise Exception("Object " + ob.name + " has more than 65535 vertices")

        #export
        bpy.ops.export_scene.fbx(
            filepath = fpath + ".fbx", 
            #version = 'BIN7400',
            use_active_collection = True,
            #use_selection = True,
            global_scale = 1,
            apply_unit_scale = False,
            apply_scale_options = 'FBX_SCALE_UNITS',
            object_types = {'EMPTY', 'MESH', 'OTHER'})

        print('Finished AC export to ' + fpath + ' for collection: ' + collectionName)

        # auto reload?

        return {'FINISHED'}

# UI PANEL

class NOTHKE_PT_ACExport(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "AC Exporter"
    bl_idname = "NOTHKE_PT_ACExport"
    
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI' #'TOOLS'
    bl_category = 'AC Exporter'

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        row = layout.row()
        row.prop(scene, 'acexport_collectionName')

        row = layout.row()
        row.prop(scene, 'acexport_filename')

        # export button, create operator
        row = layout.row()
        op = row.operator('object.ac_export', text='Export FBX')

        # set properties to operator values
        op.collectionName = scene.acexport_collectionName
        op.filename = scene.acexport_filename

        row = layout.row()
        row.label(text = 'Important:')

        row = layout.row()
        row.label(text = 'Save before pressing export')

        row = layout.row()
        row.label(text = 'Revert after export!')

def register():
    
    bpy.utils.register_class(NOTHKE_OT_ACExport)
    print('operator registered')

    # register properties
    bpy.types.Scene.acexport_layer = bpy.props.IntProperty(
        name="Layer",
        description="Export all objects from this layer",
        default = 1)
        
    bpy.types.Scene.acexport_collectionName = bpy.props.StringProperty(
        name="Collection",
        description="Export all objects from this collection",
        default='EXPORT')

    bpy.types.Scene.acexport_filename = bpy.props.StringProperty(
        name="Filename",
        description="Filename",
        default = 'ac_export')
    print('properties registered')

    bpy.utils.register_class(NOTHKE_PT_ACExport)
    print('panel registered')

def unregister():
    bpy.utils.unregister_class(NOTHKE_OT_ACExport)
    bpy.utils.unregister_class(NOTHKE_PT_ACExport)
    del bpy.types.Scene.acexport_layer
    del bpy.types.Scene.acexport_filename

if __name__ == "__main__":
    register()

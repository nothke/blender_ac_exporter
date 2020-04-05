## blender_ac_exporter
This script exports fbx for Assetto Corsa tracks in a single click. Created for fast iteration in mind, primarily to make sure all objects are properly setup, avoid opening export dialogue every time and since ksEditor is extremely slow and a terrible experience overall, where getting a single thing wrong can easily lose you 5+ minutes for no reason.

## What does it exactly do?
- Makes sure all objects are unlinked (because cloned objects (copied with alt + D) will have spurrious materials when exported to fbx)
- TODO: Makes sure at least one material slot is present on all objects (because objects with no slots will get autocreated FBX_MATERIALs)
- TODO: Makes sure meshes don't have more than 65k vertices (because AC works with 16bit indices)
- Sets correct fbx export units and settings

### How to install
1. Edit > Preferences.. > Add-Ons > Install.. and select nothke_ac_exporter.py, then activate it on the checkbox
2. A new tab will appear on the right of the viewport called "ACExporter"

### How to use
1. Save your blend file (and do it every time before export, because you'll have to revert after pressing "Export")
2. Open the ACExport tab: On the right side of the viewport > ACExporter
3. Type the name of the exporting collection. Make sure that only meshes are present. Curves, backgrounds, lights etc. will be invalid.
4. Type in the desired name of the fbx file
5. Hit "Export FBX". If there are were no warnings, now be in the same folder where .blend is.
6. Revert to your previous save (File > Revert) so that linked objects are preserved
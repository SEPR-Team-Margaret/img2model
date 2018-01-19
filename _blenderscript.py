code = """
import bpy
fp = "{0}"
print("Working on", fp)

for o in bpy.data.objects:
    o.select = True
bpy.ops.object.delete()

x = bpy.ops.import_curve.svg(filepath=fp)
for o in bpy.data.objects:
    o.select = True
    bpy.context.scene.objects.active = o
    bpy.ops.object.convert(target="MESH")
    o.select = False
    bpy.context.scene.objects.active = None

for o in bpy.data.objects:
    o.select = True
    bpy.context.scene.objects.active = o
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all()
    bpy.ops.mesh.dissolve_degenerate()
    bpy.ops.mesh.dissolve_limited()
    bpy.ops.mesh.dissolve_limited()
    bpy.ops.object.mode_set(mode="OBJECT")
    o.select = False
    bpy.context.scene.objects.active = None
for c in bpy.data.curves:
	c.extrude = {1}


fpo = "{2}"
bpy.ops.export_scene.autodesk_3ds(filepath=fpo)
"""

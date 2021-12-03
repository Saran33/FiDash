import bpy
import csv
import json

# Open the empty base scene.
bpy.ops.wm.open_mainfile(filepath="stereo_equirectangular_base.blend")

elem_size = 0.1  # Make the points fairly small.
alpha_level = 0.25  # for transparency (though, I'm not sure this works below...)
input_path = "datascience_twitter_users_3d_tsne_with_communities.csv"

# Make materials for coloring data points.
# http://wiki.blender.org/index.php/Dev:2.5/Py/Scripts/Cookbook/Code_snippets/Materials_and_textures
def make_material(name, diffuse, alpha):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = diffuse
    mat.alpha = alpha
    return mat

# Make different colored materials for each community.
with open(input_path) as csvfile:
    reader = csv.DictReader(csvfile)
    communities = {row['community'] for row in reader}

# Load a color scheme from http://colorbrewer2.org/.
all_colors = json.load(open("colorbrewer.json"))

# Make materials for the different groups of points.
colors = [[float(v) / 255 for v in x[4:-1].split(',')]
          for x in all_colors['Set3'][str(len(communities))]]
materials = {}
for community, rgb_tuple in zip(communities, colors):
    mat = make_material("mat_{}".format(community), rgb_tuple, alpha_level)
    materials[community] = mat

# Position and color the points.
with open(input_path) as csvfile:
    reader = csv.DictReader(csvfile)  # no pandas in blender (by default) :-(
    for row in reader:
        x, y, z = float(row['x']), float(row['y']), float(row['z'])
        bpy.ops.mesh.primitive_uv_sphere_add(location=(x, y, z))
        ob = bpy.context.object
        ob.data.materials.append(materials[row['community']])
        for face in ob.data.polygons:
            face.use_smooth = True
        bpy.ops.transform.resize(value=(elem_size, elem_size, elem_size))

bpy.data.scenes['Scene'].render.filepath = 'stereo_3d_tsne.png'
bpy.ops.render.render(write_still=True)

# Save the modified file.
bpy.ops.wm.save_as_mainfile(filepath="modified_stereo_equirectangular_base.blend")
import os

os.environ['OVITO_GUI_MODE'] = '1'  # Request a session with OpenGL support

import cv2
import math
import shutil
from PIL import Image
from ovito.io import import_file
from ovito.vis import Viewport

ovito_png_files = "./ovito_png_files"
metad_png_files = "./metad_png_files"

# Clear the directory
if os.path.exists(ovito_png_files):
    shutil.rmtree(ovito_png_files)
os.mkdir(ovito_png_files)
if os.path.exists(metad_png_files):
    shutil.rmtree(metad_png_files)
os.mkdir(metad_png_files)

# Import the XYZ file
pipeline = import_file('./XDATRAIN.xyz')
pipeline.add_to_scene()

vp = Viewport()
vp.type = Viewport.Type.Perspective
vp.camera_pos = (5, -40, 5)
vp.camera_dir = (0, 1, 0)
vp.fov = math.radians(60.0)

# Export image each 50 frames
for frame in range(0, 5000, 50):
    print('Rendering frame %d' % frame)
    vp.render_image(filename="./ovito_png_files/myimage_%05d.png" % frame, size=(480, 480), frame=frame)

# Combine two images into one
ovito_png_files = os.listdir("./ovito_png_files/")
metad_png_files = os.listdir("../../Metadynamics/vasp_codes/output_LLTO_U1_MetaD_2000K_H01_W01_BIN50")

for i in range(len(ovito_png_files)):
    print('Combining frame %d' % i)
    images = [
        Image.open("../../old_metadynamics/vasp_codes/output_LLTO_U1_MetaD_2000K_H01_W01_BIN50/" + metad_png_files[i]),
        Image.open("./ovito_png_files/" + ovito_png_files[i])]

    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]

    new_im.save('metad_png_files/metad_%05d.png' % i)

image_folder = 'metad_png_files'
video_name = 'video.avi'

images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, 0, 1, (width, height))

for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()

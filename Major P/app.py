# # # # # # from flask import Flask, request, render_template, send_file, redirect, url_for
# # # # # # from werkzeug.utils import secure_filename
# # # # # # import os
# # # # # # import zipfile
# # # # # # from io import BytesIO
# # # # # # from PIL import Image, ImageEnhance, ImageOps
# # # # # # import numpy as np

# # # # # # app = Flask(__name__)

# # # # # # UPLOAD_FOLDER = 'uploaded_images'
# # # # # # AUGMENTED_FOLDER = 'augmented_images'
# # # # # # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# # # # # # app.config['AUGMENTED_FOLDER'] = AUGMENTED_FOLDER

# # # # # # # Ensure directories exist
# # # # # # if not os.path.exists(UPLOAD_FOLDER):
# # # # # #     os.makedirs(UPLOAD_FOLDER)

# # # # # # if not os.path.exists(AUGMENTED_FOLDER):
# # # # # #     os.makedirs(AUGMENTED_FOLDER)

# # # # # # # Function to apply augmentations
# # # # # # def apply_augmentations(image, techniques):
# # # # # #     for technique in techniques:
# # # # # #         if technique == 'rotation':
# # # # # #             image = image.rotate(45)
# # # # # #         elif technique == 'scaling':
# # # # # #             image = image.resize((int(image.width * 1.5), int(image.height * 1.5)))
# # # # # #         elif technique == 'translation':
# # # # # #             image = ImageOps.offset(image, 50, 50)
# # # # # #         elif technique == 'shearing':
# # # # # #             matrix = (1, 0.5, 0, 0.5, 1, 0)
# # # # # #             image = image.transform(image.size, Image.AFFINE, matrix)
# # # # # #         elif technique == 'flipping':
# # # # # #             image = ImageOps.mirror(image)
# # # # # #         elif technique == 'cropping':
# # # # # #             image = image.crop((10, 10, image.width - 10, image.height - 10))
# # # # # #         elif technique == 'padding':
# # # # # #             image = ImageOps.expand(image, border=20, fill='black')
# # # # # #         elif technique == 'brightness':
# # # # # #             enhancer = ImageEnhance.Brightness(image)
# # # # # #             image = enhancer.enhance(1.5)
# # # # # #         elif technique == 'contrast':
# # # # # #             enhancer = ImageEnhance.Contrast(image)
# # # # # #             image = enhancer.enhance(1.5)
# # # # # #         elif technique == 'saturation':
# # # # # #             enhancer = ImageEnhance.Color(image)
# # # # # #             image = enhancer.enhance(1.5)
# # # # # #         elif technique == 'hue':
# # # # # #             image = image.convert('HSV')
# # # # # #             np_img = np.array(image)
# # # # # #             np_img[..., 0] = (np_img[..., 0] + 50) % 255
# # # # # #             image = Image.fromarray(np_img, 'HSV').convert('RGB')
# # # # # #         elif technique == 'grayscale':
# # # # # #             image = ImageOps.grayscale(image)
# # # # # #         elif technique == 'color_jittering':
# # # # # #             image = ImageEnhance.Color(image).enhance(np.random.uniform(0.8, 1.2))
# # # # # #     return image

# # # # # # @app.route('/')
# # # # # # def index():
# # # # # #     return render_template('index.html')

# # # # # # @app.route('/upload', methods=['POST'])
# # # # # # def upload():
# # # # # #     files = request.files.getlist('images')
# # # # # #     for file in files:
# # # # # #         filename = secure_filename(file.filename)
# # # # # #         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
# # # # # #     return redirect(url_for('select_augmentations'))

# # # # # # @app.route('/select_augmentations')
# # # # # # def select_augmentations():
# # # # # #     return render_template('select_augmentations.html')

# # # # # # @app.route('/apply_augmentations', methods=['POST'])
# # # # # # def apply_augmentations_route():
# # # # # #     techniques = request.form.getlist('augmentations')
# # # # # #     version = len(os.listdir(app.config['AUGMENTED_FOLDER'])) + 1
# # # # # #     version_folder = os.path.join(app.config['AUGMENTED_FOLDER'], f'version_{version}')
# # # # # #     os.makedirs(version_folder)

# # # # # #     for filename in os.listdir(app.config['UPLOAD_FOLDER']):
# # # # # #         image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
# # # # # #         image = Image.open(image_path)
# # # # # #         augmented_image = apply_augmentations(image, techniques)
# # # # # #         augmented_image.save(os.path.join(version_folder, filename))

# # # # # #     return redirect(url_for('download'))

# # # # # # @app.route('/download')
# # # # # # def download():
# # # # # #     versions = [folder.split('_')[-1] for folder in os.listdir(app.config['AUGMENTED_FOLDER']) if folder.startswith('version_')]
# # # # # #     versions.sort(key=int)
# # # # # #     return render_template('download.html', versions=versions)

# # # # # # @app.route('/download_zip/<int:version>')
# # # # # # def download_zip(version):
# # # # # #     version_folder = os.path.join(app.config['AUGMENTED_FOLDER'], f'version_{version}')
    
# # # # # #     memory_file = BytesIO()
# # # # # #     with zipfile.ZipFile(memory_file, 'w') as zf:
# # # # # #         for filename in os.listdir(version_folder):
# # # # # #             file_path = os.path.join(version_folder, filename)
# # # # # #             zf.write(file_path, arcname=filename)
    
# # # # # #     memory_file.seek(0)
    
# # # # # #     return send_file(memory_file, as_attachment=True, download_name=f'version_{version}.zip', mimetype='application/zip')

# # # # # # if __name__ == '__main__':
# # # # # #     app.run(debug=True)






# # # # # from flask import Flask, request, render_template, send_file, redirect, url_for, session
# # # # # from werkzeug.utils import secure_filename
# # # # # import os
# # # # # import zipfile
# # # # # from io import BytesIO
# # # # # from PIL import Image, ImageEnhance, ImageOps
# # # # # import numpy as np

# # # # # app = Flask(__name__)
# # # # # app.secret_key = 'secret_key'

# # # # # UPLOAD_FOLDER = 'uploaded_images'
# # # # # AUGMENTED_FOLDER = 'augmented_images'
# # # # # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# # # # # app.config['AUGMENTED_FOLDER'] = AUGMENTED_FOLDER

# # # # # if not os.path.exists(UPLOAD_FOLDER):
# # # # #     os.makedirs(UPLOAD_FOLDER)

# # # # # if not os.path.exists(AUGMENTED_FOLDER):
# # # # #     os.makedirs(AUGMENTED_FOLDER)

# # # # # def apply_augmentations(image, techniques, params):
# # # # #     for technique in techniques:
# # # # #         if technique == 'rotation':
# # # # #             angle = float(params.get('rotation_angle', 0))
# # # # #             image = image.rotate(angle)
# # # # #         elif technique == 'scaling':
# # # # #             factor = float(params.get('scaling_factor', 1))
# # # # #             image = image.resize((int(image.width * factor), int(image.height * factor)))
# # # # #         elif technique == 'brightness':
# # # # #             enhancer = ImageEnhance.Brightness(image)
# # # # #             image = enhancer.enhance(float(params.get('brightness_factor', 1)))
# # # # #         elif technique == 'contrast':
# # # # #             enhancer = ImageEnhance.Contrast(image)
# # # # #             image = enhancer.enhance(float(params.get('contrast_factor', 1)))
# # # # #         elif technique == 'flipping':
# # # # #             image = ImageOps.mirror(image)
# # # # #     return image

# # # # # @app.route('/')
# # # # # def index():
# # # # #     return render_template('index.html')

# # # # # @app.route('/upload', methods=['POST'])
# # # # # def upload():
# # # # #     files = request.files.getlist('images')
# # # # #     for file in files:
# # # # #         filename = secure_filename(file.filename)
# # # # #         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
# # # # #     session['uploaded_files'] = os.listdir(app.config['UPLOAD_FOLDER'])
# # # # #     return redirect(url_for('select_augmentations'))

# # # # # @app.route('/select_augmentations')
# # # # # def select_augmentations():
# # # # #     return render_template('select_augmentations.html')

# # # # # @app.route('/set_augmentation_count', methods=['POST'])
# # # # # def set_augmentation_count():
# # # # #     augmentations = request.form.to_dict()
# # # # #     max_images = len(session.get('uploaded_files', [])) * 5  # Allow up to 5x augmentation
# # # # #     return render_template('set_augmentation_count.html', augmentations=augmentations, max_images=max_images)

# # # # # @app.route('/apply_augmentations', methods=['POST'])
# # # # # def apply_augmentations_route():
# # # # #     techniques = request.form.getlist('augmentations')
# # # # #     params = request.form.to_dict()
# # # # #     augment_count = int(params.pop('augment_count', 1))

# # # # #     version = len(os.listdir(app.config['AUGMENTED_FOLDER'])) + 1
# # # # #     version_folder = os.path.join(app.config['AUGMENTED_FOLDER'], f'version_{version}')
# # # # #     os.makedirs(version_folder)

# # # # #     for filename in session.get('uploaded_files', []):
# # # # #         image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
# # # # #         image = Image.open(image_path)
# # # # #         for i in range(augment_count):
# # # # #             augmented_image = apply_augmentations(image, techniques, params)
# # # # #             augmented_image.save(os.path.join(version_folder, f"{filename.split('.')[0]}_aug_{i}.png"))

# # # # #     return redirect(url_for('download'))

# # # # # @app.route('/download')
# # # # # def download():
# # # # #     versions = [folder.split('_')[-1] for folder in os.listdir(app.config['AUGMENTED_FOLDER']) if folder.startswith('version_')]
# # # # #     versions.sort(key=int)
# # # # #     return render_template('download.html', versions=versions)

# # # # # @app.route('/download_zip/<int:version>')
# # # # # def download_zip(version):
# # # # #     version_folder = os.path.join(app.config['AUGMENTED_FOLDER'], f'version_{version}')
    
# # # # #     memory_file = BytesIO()
# # # # #     with zipfile.ZipFile(memory_file, 'w') as zf:
# # # # #         for filename in os.listdir(version_folder):
# # # # #             file_path = os.path.join(version_folder, filename)
# # # # #             zf.write(file_path, arcname=filename)
    
# # # # #     memory_file.seek(0)
    
# # # # #     return send_file(memory_file, as_attachment=True, download_name=f'version_{version}.zip', mimetype='application/zip')

# # # # # if __name__ == '__main__':
# # # # #     app.run(debug=True)





# # # # import json
# # # # import random
# # # # from flask import Flask, request, render_template, send_file, redirect, url_for, session
# # # # from werkzeug.utils import secure_filename
# # # # import os
# # # # import zipfile
# # # # from io import BytesIO
# # # # from PIL import Image, ImageEnhance, ImageOps

# # # # app = Flask(__name__)
# # # # app.secret_key = 'secret_key'

# # # # UPLOAD_FOLDER = 'uploaded_images'
# # # # AUGMENTED_FOLDER = 'augmented_images'
# # # # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# # # # app.config['AUGMENTED_FOLDER'] = AUGMENTED_FOLDER

# # # # if not os.path.exists(UPLOAD_FOLDER):
# # # #     os.makedirs(UPLOAD_FOLDER)

# # # # if not os.path.exists(AUGMENTED_FOLDER):
# # # #     os.makedirs(AUGMENTED_FOLDER)

# # # # def apply_augmentations(image, techniques, params):
# # # #     for technique in techniques:
# # # #         if technique == 'rotation':
# # # #             angle = float(params.get('rotation_angle', 0))
# # # #             image = image.rotate(angle)
# # # #         elif technique == 'scaling':
# # # #             factor = float(params.get('scaling_factor', 1))
# # # #             image = image.resize((int(image.width * factor), int(image.height * factor)))
# # # #         elif technique == 'brightness':
# # # #             enhancer = ImageEnhance.Brightness(image)
# # # #             image = enhancer.enhance(float(params.get('brightness_factor', 1)))
# # # #         elif technique == 'contrast':
# # # #             enhancer = ImageEnhance.Contrast(image)
# # # #             image = enhancer.enhance(float(params.get('contrast_factor', 1)))
# # # #         elif technique == 'flipping':
# # # #             image = ImageOps.mirror(image)
# # # #     return image

# # # # @app.route('/')
# # # # def index():
# # # #     return render_template('index.html')

# # # # @app.route('/upload', methods=['POST'])
# # # # def upload():
# # # #     files = request.files.getlist('images')
# # # #     for file in files:
# # # #         filename = secure_filename(file.filename)
# # # #         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
# # # #     session['uploaded_files'] = os.listdir(app.config['UPLOAD_FOLDER'])
# # # #     return redirect(url_for('select_augmentations'))

# # # # @app.route('/select_augmentations')
# # # # def select_augmentations():
# # # #     return render_template('select_augmentations.html')

# # # # @app.route('/set_augmentation_count', methods=['POST'])
# # # # def set_augmentation_count():
# # # #     augmentations = request.form.to_dict()
# # # #     uploaded_images = len(session.get('uploaded_files', []))  # Get total uploaded images
# # # #     return render_template('set_augmentation_count.html', augmentations=augmentations, uploaded_images=uploaded_images)

# # # # @app.route('/apply_augmentations', methods=['POST'])
# # # # def apply_augmentations_route():
# # # #     techniques = request.form.getlist('augmentations')
# # # #     params = request.form.to_dict()
# # # #     augment_count = int(params.pop('augment_count', 1))

# # # #     version = len(os.listdir(app.config['AUGMENTED_FOLDER'])) + 1
# # # #     version_folder = os.path.join(app.config['AUGMENTED_FOLDER'], f'version_{version}')
# # # #     os.makedirs(version_folder)

# # # #     uploaded_files = session.get('uploaded_files', [])
# # # #     selected_files = random.sample(uploaded_files, min(augment_count, len(uploaded_files)))

# # # #     augmented_images = []
# # # #     for filename in selected_files:
# # # #         image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
# # # #         image = Image.open(image_path)
# # # #         augmented_image = apply_augmentations(image, techniques, params)
# # # #         save_path = os.path.join(version_folder, f"{filename.split('.')[0]}_aug.png")
# # # #         augmented_image.save(save_path)
# # # #         augmented_images.append(save_path)

# # # #     metadata = {
# # # #         "version": version,
# # # #         "total_augmented_images": len(augmented_images),
# # # #         "selected_augmentations": techniques,
# # # #         "augmentation_params": params
# # # #     }

# # # #     with open(os.path.join(version_folder, "metadata.json"), "w") as f:
# # # #         json.dump(metadata, f, indent=4)

# # # #     return redirect(url_for('download'))

# # # # @app.route('/download')
# # # # def download():
# # # #     versions = {}
    
# # # #     # Iterate over version folders
# # # #     for folder in os.listdir(app.config['AUGMENTED_FOLDER']):
# # # #         if folder.startswith('version_'):
# # # #             version_number = int(folder.split('_')[-1])
# # # #             metadata_path = os.path.join(app.config['AUGMENTED_FOLDER'], folder, "metadata.json")

# # # #             # Read metadata
# # # #             if os.path.exists(metadata_path):
# # # #                 with open(metadata_path, 'r') as f:
# # # #                     metadata = json.load(f)
# # # #             else:
# # # #                 metadata = {"total_augmented_images": 0, "selected_augmentations": [], "augmentation_params": {}}

# # # #             versions[version_number] = metadata

# # # #     # Sort versions in ascending order
# # # #     sorted_versions = dict(sorted(versions.items()))

# # # #     return render_template('download.html', versions=sorted_versions)


# # # # @app.route('/download_zip/<int:version>')
# # # # def download_zip(version):
# # # #     version_folder = os.path.join(app.config['AUGMENTED_FOLDER'], f'version_{version}')
    
# # # #     memory_file = BytesIO()
# # # #     with zipfile.ZipFile(memory_file, 'w') as zf:
# # # #         for filename in os.listdir(version_folder):
# # # #             file_path = os.path.join(version_folder, filename)
# # # #             zf.write(file_path, arcname=filename)
    
# # # #     memory_file.seek(0)
    
# # # #     return send_file(memory_file, as_attachment=True, download_name=f'version_{version}.zip', mimetype='application/zip')

# # # # if __name__ == '__main__':
# # # #     app.run(debug=True)





# # # import os
# # # import json
# # # import random
# # # import zipfile
# # # from flask import Flask, request, render_template, send_file, redirect, url_for, session
# # # from werkzeug.utils import secure_filename
# # # from io import BytesIO
# # # from PIL import Image, ImageEnhance, ImageOps

# # # app = Flask(__name__)
# # # app.secret_key = 'secret_key'

# # # UPLOAD_FOLDER = 'uploaded_images'
# # # AUGMENTED_FOLDER = 'augmented_images'
# # # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# # # app.config['AUGMENTED_FOLDER'] = AUGMENTED_FOLDER

# # # if not os.path.exists(UPLOAD_FOLDER):
# # #     os.makedirs(UPLOAD_FOLDER)

# # # if not os.path.exists(AUGMENTED_FOLDER):
# # #     os.makedirs(AUGMENTED_FOLDER)

# # # def apply_augmentations(image, techniques, params):
# # #     if "rotation" in techniques:
# # #         image = image.rotate(float(params.get("rotation_angle", 0)))
# # #     if "scaling" in techniques:
# # #         scale = float(params.get("scaling_factor", 1))
# # #         image = image.resize((int(image.width * scale), int(image.height * scale)))
# # #     if "flipping" in techniques:
# # #         image = ImageOps.mirror(image)
# # #     if "brightness" in techniques:
# # #         enhancer = ImageEnhance.Brightness(image)
# # #         image = enhancer.enhance(float(params.get("brightness_factor", 1)))
# # #     if "contrast" in techniques:
# # #         enhancer = ImageEnhance.Contrast(image)
# # #         image = enhancer.enhance(float(params.get("contrast_factor", 1)))
# # #     if "grayscale" in techniques:
# # #         image = ImageOps.grayscale(image)
# # #     return image

# # # @app.route('/')
# # # def index():
# # #     return render_template('index.html')

# # # @app.route('/upload', methods=['POST'])
# # # def upload():
# # #     files = request.files.getlist('images')
# # #     for file in files:
# # #         filename = secure_filename(file.filename)
# # #         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
# # #     session['uploaded_files'] = os.listdir(app.config['UPLOAD_FOLDER'])
# # #     return redirect(url_for('select_augmentations'))

# # # @app.route('/select_augmentations')
# # # def select_augmentations():
# # #     return render_template('select_augmentations.html')

# # # @app.route('/set_augmentation_count', methods=['POST'])
# # # def set_augmentation_count():
# # #     augmentations = request.form.to_dict()
# # #     uploaded_images = len(session.get('uploaded_files', []))
# # #     return render_template('set_augmentation_count.html', augmentations=augmentations, uploaded_images=uploaded_images)

# # # @app.route('/apply_augmentations', methods=['POST'])
# # # def apply_augmentations_route():
# # #     techniques = request.form.getlist('augmentations')
# # #     params = request.form.to_dict()
# # #     augment_count = int(params.pop('augment_count', 1))

# # #     version = len(os.listdir(app.config['AUGMENTED_FOLDER'])) + 1
# # #     version_folder = os.path.join(app.config['AUGMENTED_FOLDER'], f'version_{version}')
# # #     os.makedirs(version_folder)

# # #     uploaded_files = session.get('uploaded_files', [])
# # #     selected_files = random.sample(uploaded_files, min(augment_count, len(uploaded_files)))

# # #     augmented_images = []
# # #     for filename in selected_files:
# # #         image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
# # #         image = Image.open(image_path)
# # #         augmented_image = apply_augmentations(image, techniques, params)
# # #         save_path = os.path.join(version_folder, f"{filename.split('.')[0]}_aug.png")
# # #         augmented_image.save(save_path)
# # #         augmented_images.append(save_path)

# # #     metadata = {
# # #         "version": version,
# # #         "total_augmented_images": len(augmented_images),
# # #         "selected_augmentations": techniques,
# # #         "augmentation_params": params
# # #     }

# # #     with open(os.path.join(version_folder, "metadata.json"), "w") as f:
# # #         json.dump(metadata, f, indent=4)

# # #     return redirect(url_for('download'))

# # # if __name__ == '__main__':
# # #     app.run(debug=True)



# # import os
# # import json
# # import random
# # import zipfile
# # from flask import Flask, request, render_template, send_file, redirect, url_for, session
# # from werkzeug.utils import secure_filename
# # from io import BytesIO
# # from PIL import Image, ImageEnhance, ImageOps

# # app = Flask(__name__)
# # app.secret_key = 'secret_key'

# # UPLOAD_FOLDER = 'uploaded_images'
# # AUGMENTED_FOLDER = 'augmented_images'
# # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# # app.config['AUGMENTED_FOLDER'] = AUGMENTED_FOLDER

# # if not os.path.exists(UPLOAD_FOLDER):
# #     os.makedirs(UPLOAD_FOLDER)

# # if not os.path.exists(AUGMENTED_FOLDER):
# #     os.makedirs(AUGMENTED_FOLDER)

# # def apply_augmentations(image, techniques, params):
# #     if "rotation" in techniques and "rotation_angle" in params:
# #         image = image.rotate(float(params["rotation_angle"]), expand=True)

# #     if "scaling" in techniques and "scaling_factor" in params:
# #         scale = float(params["scaling_factor"])
# #         image = image.resize((int(image.width * scale), int(image.height * scale)))

# #     if "translation" in techniques and "translation_x" in params and "translation_y" in params:
# #         x_offset = int(params["translation_x"])
# #         y_offset = int(params["translation_y"])
# #         image = ImageOps.expand(image, border=(x_offset, y_offset, 0, 0), fill="black")

# #     if "flipping" in techniques:
# #         image = ImageOps.mirror(image)

# #     if "brightness" in techniques and "brightness_factor" in params:
# #         enhancer = ImageEnhance.Brightness(image)
# #         image = enhancer.enhance(float(params["brightness_factor"]))

# #     if "contrast" in techniques and "contrast_factor" in params:
# #         enhancer = ImageEnhance.Contrast(image)
# #         image = enhancer.enhance(float(params["contrast_factor"]))

# #     if "grayscale" in techniques:
# #         image = ImageOps.grayscale(image)

# #     return image


# # @app.route('/')
# # def index():
# #     return render_template('index.html')

# # @app.route('/upload', methods=['POST'])
# # def upload():
# #     files = request.files.getlist('images')
# #     for file in files:
# #         filename = secure_filename(file.filename)
# #         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
# #     session['uploaded_files'] = os.listdir(app.config['UPLOAD_FOLDER'])
# #     return redirect(url_for('select_augmentations'))

# # @app.route('/select_augmentations')
# # def select_augmentations():
# #     return render_template('select_augmentations.html')

# # @app.route('/set_augmentation_count', methods=['POST'])
# # def set_augmentation_count():
# #     augmentations = request.form.to_dict()
# #     uploaded_images = len(session.get('uploaded_files', []))
# #     return render_template('set_augmentation_count.html', augmentations=augmentations, uploaded_images=uploaded_images)

# # def apply_augmentations(image, techniques, params):
# #     """Applies selected augmentation techniques to an image."""
    
# #     if "rotation" in techniques and "rotation_angle" in params:
# #         angle = float(params["rotation_angle"])
# #         image = image.rotate(angle, expand=True)  # Ensures rotated image fits properly
    
# #     if "scaling" in techniques and "scaling_factor" in params:
# #         scale = float(params["scaling_factor"])
# #         new_size = (int(image.width * scale), int(image.height * scale))
# #         image = image.resize(new_size, Image.ANTIALIAS)

# #     if "translation" in techniques and "translation_x" in params and "translation_y" in params:
# #         x_offset = int(params["translation_x"])
# #         y_offset = int(params["translation_y"])
# #         new_image = Image.new("RGB", (image.width + abs(x_offset), image.height + abs(y_offset)), "black")
# #         new_image.paste(image, (max(0, x_offset), max(0, y_offset)))
# #         image = new_image

# #     if "flipping" in techniques:
# #         image = ImageOps.mirror(image)

# #     if "brightness" in techniques and "brightness_factor" in params:
# #         enhancer = ImageEnhance.Brightness(image)
# #         image = enhancer.enhance(float(params["brightness_factor"]))

# #     if "contrast" in techniques and "contrast_factor" in params:
# #         enhancer = ImageEnhance.Contrast(image)
# #         image = enhancer.enhance(float(params["contrast_factor"]))

# #     if "grayscale" in techniques:
# #         image = ImageOps.grayscale(image)

# #     return image


# # @app.route('/download')
# # def download():
# #     versions = {}

# #     # Iterate over version folders
# #     for folder in os.listdir(app.config['AUGMENTED_FOLDER']):
# #         if folder.startswith('version_'):
# #             version_number = int(folder.split('_')[-1])
# #             metadata_path = os.path.join(app.config['AUGMENTED_FOLDER'], folder, "metadata.json")

# #             # Read metadata
# #             if os.path.exists(metadata_path):
# #                 with open(metadata_path, 'r') as f:
# #                     metadata = json.load(f)
# #             else:
# #                 metadata = {"total_augmented_images": 0, "selected_augmentations": [], "augmentation_params": {}}

# #             versions[version_number] = metadata

# #     # Sort versions in ascending order
# #     sorted_versions = dict(sorted(versions.items()))

# #     return render_template('download.html', versions=sorted_versions)

# # @app.route('/download_zip/<version>')
# # def download_zip(version):
# #     version_folder = os.path.join(app.config['AUGMENTED_FOLDER'], version)
# #     zip_filename = f"{version}.zip"

# #     # Create an in-memory ZIP file
# #     memory_file = BytesIO()
# #     with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
# #         for root, _, files in os.walk(version_folder):
# #             for file in files:
# #                 if file.endswith('.png') or file.endswith('.jpg'):
# #                     file_path = os.path.join(root, file)
# #                     zipf.write(file_path, os.path.relpath(file_path, version_folder))

# #     memory_file.seek(0)

# #     return send_file(memory_file, download_name=zip_filename, as_attachment=True)

# # if __name__ == '__main__':
# #     app.run(debug=True)



# import os
# import json
# import zipfile
# from flask import Flask, request, render_template, send_file, redirect, url_for, session
# from werkzeug.utils import secure_filename
# from io import BytesIO
# from PIL import Image, ImageEnhance, ImageOps

# app = Flask(__name__)
# app.secret_key = 'your_secret_key_here'  # Replace with a secure, random key for production

# UPLOAD_FOLDER = 'uploaded_images'
# AUGMENTED_FOLDER = 'augmented_images'
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['AUGMENTED_FOLDER'] = AUGMENTED_FOLDER

# # Ensure the upload and augmented directories exist
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(AUGMENTED_FOLDER, exist_ok=True)

# def allowed_file(filename):
#     """Check if the file has an allowed extension."""
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def apply_augmentations(image, techniques, params):
#     """Applies selected augmentation techniques to an image."""

#     # Geometric Transformations
#     if "rotation" in techniques and "rotation_angle" in params:
#         angle = float(params["rotation_angle"])
#         image = image.rotate(angle, expand=True)

#     if "scaling" in techniques and "scaling_factor" in params:
#         scale = float(params["scaling_factor"])
#         new_size = (int(image.width * scale), int(image.height * scale))
#         image = image.resize(new_size, Image.LANCZOS)

#     if "translation" in techniques and "translation_x" in params and "translation_y" in params:
#         x_offset = int(params["translation_x"])
#         y_offset = int(params["translation_y"])
#         new_width = image.width + abs(x_offset)
#         new_height = image.height + abs(y_offset)
#         new_image = Image.new("RGB", (new_width, new_height), "black")
#         new_image.paste(image, (max(0, x_offset), max(0, y_offset)))
#         image = new_image

#     if "flipping" in techniques:
#         image = ImageOps.mirror(image)

#     # Color Transformations
#     if "brightness" in techniques and "brightness_factor" in params:
#         enhancer = ImageEnhance.Brightness(image)
#         image = enhancer.enhance(float(params["brightness_factor"]))

#     if "contrast" in techniques and "contrast_factor" in params:
#         enhancer = ImageEnhance.Contrast(image)
#         image = enhancer.enhance(float(params["contrast_factor"]))

#     if "grayscale" in techniques:
#         image = ImageOps.grayscale(image)

#     return image

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/upload', methods=['POST'])
# def upload():
#     files = request.files.getlist('images')
#     for file in files:
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(filepath)
#     session['uploaded_files'] = os.listdir(app.config['UPLOAD_FOLDER'])
#     return redirect(url_for('select_augmentations'))

# @app.route('/select_augmentations', methods=['GET', 'POST'])
# def select_augmentations():
#     if request.method == 'POST':
#         augmentations = request.form.to_dict()
#         session['augmentations'] = augmentations
#         uploaded_images = len(session.get('uploaded_files', []))
#         return render_template('set_augmentation_count.html', augmentations=augmentations, uploaded_images=uploaded_images)
#     return render_template('select_augmentations.html')

# @app.route('/set_augmentation_count', methods=['POST'])
# def set_augmentation_count():
#     augment_count = int(request.form.get('augment_count', 1))
#     session['augment_count'] = augment_count
#     return redirect(url_for('apply_augmentations_route'))

# @app.route('/apply_augmentations', methods=['GET', 'POST'])
# def apply_augmentations_route():
#     uploaded_files = session.get('uploaded_files', [])
#     augmentations = session.get('augmentations', {})
#     augment_count = session.get('augment_count', 1)
#     params = augmentations.copy()

#     # Prepare techniques list
#     techniques = [key for key, value in augmentations.items() if value == 'yes']

#     # Prepare versioning
#     existing_versions = [int(d.split('_')[-1]) for d in os.listdir(app.config['AUGMENTED_FOLDER']) if d.startswith('version_')]
#     version_number = max(existing_versions + [0]) + 1
#     version_folder = os.path.join(app.config['AUGMENTED_FOLDER'], f"version_{version_number}")
#     os.makedirs(version_folder, exist_ok=True)

#     total_augmented_images = 0

#     # Apply augmentations
#     for i in range(augment_count):
#         for filename in uploaded_files:
#             filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             image = Image.open(filepath)

#             augmented_image = apply_augmentations(image, techniques, params)
#             file_root, file_ext = os.path.splitext(filename)
#             augmented_filename = f"{file_root}_aug_{i}{file_ext}"
#             augmented_filepath = os.path.join(version_folder, augmented_filename)
#             augmented_image.save(augmented_filepath)
#             total_augmented_images += 1

#     # Save metadata
#     metadata = {
#         "total_augmented_images": total_augmented_images,
#         "selected_augmentations": techniques,
#         "augmentation_params": params
#     }
#     with open(os.path.join(version_folder, "metadata.json"), 'w') as f:
#         json.dump(metadata, f, indent=4)

#     # Clear uploaded images after processing
#     session.pop('uploaded_files', None)
#     session.pop('augmentations', None)
#     session.pop('augment_count', None)

#     # Optionally, clear the uploaded_images folder after processing
#     for file in os.listdir(app.config['UPLOAD_FOLDER']):
#         os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))

#     return redirect(url_for('download'))

# @app.route('/download')
# def download():
#     versions = {}

#     # Iterate over version folders
#     for folder in os.listdir(app.config['AUGMENTED_FOLDER']):
#         if folder.startswith('version_'):
#             version_number = int(folder.split('_')[-1])
#             metadata_path = os.path.join(app.config['AUGMENTED_FOLDER'], folder, "metadata.json")

#             # Read metadata
#             if os.path.exists(metadata_path):
#                 with open(metadata_path, 'r') as f:
#                     metadata = json.load(f)
#             else:
#                 metadata = {"total_augmented_images": 0, "selected_augmentations": [], "augmentation_params": {}}

#             versions[version_number] = metadata

#     # Sort versions in descending order (most recent first)
#     sorted_versions = dict(sorted(versions.items(), reverse=True))

#     return render_template('download.html', versions=sorted_versions)

# @app.route('/download_zip/<version>')
# def download_zip(version):
#     version_folder = os.path.join(app.config['AUGMENTED_FOLDER'], version)
#     zip_filename = f"{version}.zip"

#     # Create an in-memory ZIP file
#     memory_file = BytesIO()
#     with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
#         for root, _, files in os.walk(version_folder):
#             for file in files:
#                 if file.endswith(('.png', '.jpg', '.jpeg', '.gif')):
#                     file_path = os.path.join(root, file)
#                     zipf.write(file_path, os.path.relpath(file_path, version_folder))

#     memory_file.seek(0)

#     return send_file(memory_file, download_name=zip_filename, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)




import os
import json
import zipfile
from flask import Flask, request, render_template, send_file, redirect, url_for, session
from werkzeug.utils import secure_filename
from io import BytesIO
from PIL import Image, ImageEnhance, ImageOps

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure, random key for production

UPLOAD_FOLDER = 'uploaded_images'
AUGMENTED_FOLDER = 'augmented_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['AUGMENTED_FOLDER'] = AUGMENTED_FOLDER

# Ensure the upload and augmented directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AUGMENTED_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def apply_augmentations(image, techniques, params):
    """Applies selected augmentation techniques to an image."""

    # Geometric Transformations
    if "rotation" in techniques and "rotation_angle" in params:
        angle = float(params["rotation_angle"])
        image = image.rotate(angle, expand=True)

    if "scaling" in techniques and "scaling_factor" in params:
        scale = float(params["scaling_factor"])
        new_size = (int(image.width * scale), int(image.height * scale))
        image = image.resize(new_size, Image.LANCZOS)

    if "translation" in techniques and "translation_x" in params and "translation_y" in params:
        x_offset = int(params["translation_x"])
        y_offset = int(params["translation_y"])
        new_width = image.width + abs(x_offset)
        new_height = image.height + abs(y_offset)
        new_image = Image.new("RGB", (new_width, new_height), "black")
        new_image.paste(image, (max(0, x_offset), max(0, y_offset)))
        image = new_image

    if "flipping_horizontal" in techniques:
        image = ImageOps.mirror(image)  # Horizontal flip

    if "flipping_vertical" in techniques:
        image = ImageOps.flip(image)  # Vertical flip

    # Color Transformations
    if "brightness" in techniques and "brightness_factor" in params:
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(float(params["brightness_factor"]))

    if "contrast" in techniques and "contrast_factor" in params:
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(float(params["contrast_factor"]))

    if "grayscale" in techniques:
        image = ImageOps.grayscale(image)

    return image


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist('images')
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
    session['uploaded_files'] = os.listdir(app.config['UPLOAD_FOLDER'])
    return redirect(url_for('select_augmentations'))

@app.route('/select_augmentations', methods=['GET', 'POST'])
def select_augmentations():
    if request.method == 'POST':
        augmentations = request.form.to_dict()
        session['augmentations'] = augmentations
        uploaded_images = len(session.get('uploaded_files', []))
        return render_template('set_augmentation_count.html', augmentations=augmentations, uploaded_images=uploaded_images)
    return render_template('select_augmentations.html')

@app.route('/set_augmentation_count', methods=['POST'])
def set_augmentation_count():
    augment_count = int(request.form.get('augment_count', 1))
    session['augment_count'] = augment_count
    return redirect(url_for('apply_augmentations_route'))

@app.route('/apply_augmentations', methods=['GET', 'POST'])
def apply_augmentations_route():
    uploaded_files = session.get('uploaded_files', [])
    augmentations = session.get('augmentations', {})
    augment_count = session.get('augment_count', 1)
    params = augmentations.copy()

    # Prepare techniques list
    techniques = [key for key, value in augmentations.items() if value == 'yes']

    # Prepare versioning
    existing_versions = [int(d.split('_')[-1]) for d in os.listdir(app.config['AUGMENTED_FOLDER']) if d.startswith('version_')]
    version_number = max(existing_versions + [0]) + 1
    version_folder = os.path.join(app.config['AUGMENTED_FOLDER'], f"version_{version_number}")
    os.makedirs(version_folder, exist_ok=True)

    total_augmented_images = 0

    # Apply augmentations
    for i in range(augment_count):
        for filename in uploaded_files:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image = Image.open(filepath)

            augmented_image = apply_augmentations(image, techniques, params)
            file_root, file_ext = os.path.splitext(filename)
            augmented_filename = f"{file_root}_aug_{i}{file_ext}"
            augmented_filepath = os.path.join(version_folder, augmented_filename)
            augmented_image.save(augmented_filepath)
            total_augmented_images += 1

    # Save metadata
    metadata = {
        "total_augmented_images": total_augmented_images,
        "selected_augmentations": techniques,
        "augmentation_params": params
    }
    with open(os.path.join(version_folder, "metadata.json"), 'w') as f:
        json.dump(metadata, f, indent=4)

    # Clear uploaded images after processing
    session.pop('uploaded_files', None)
    session.pop('augmentations', None)
    session.pop('augment_count', None)

    # Optionally, clear the uploaded_images folder after processing
    for file in os.listdir(app.config['UPLOAD_FOLDER']):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))

    return redirect(url_for('download'))

@app.route('/download')
def download():
    versions = {}

    # Iterate over version folders
    for folder in os.listdir(app.config['AUGMENTED_FOLDER']):
        if folder.startswith('version_'):
            version_number = int(folder.split('_')[-1])
            metadata_path = os.path.join(app.config['AUGMENTED_FOLDER'], folder, "metadata.json")

            # Read metadata
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
            else:
                metadata = {"total_augmented_images": 0, "selected_augmentations": [], "augmentation_params": {}}

            versions[version_number] = metadata

    # Sort versions in descending order (most recent first)
    sorted_versions = dict(sorted(versions.items(), reverse=True))

    return render_template('download.html', versions=sorted_versions)

@app.route('/download_zip/<version>')
def download_zip(version):
    version_folder = os.path.join(app.config['AUGMENTED_FOLDER'], version)
    zip_filename = f"{version}.zip"

    # Create an in-memory ZIP file
    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(version_folder):
            for file in files:
                if file.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, version_folder))

    memory_file.seek(0)

    return send_file(memory_file, download_name=zip_filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

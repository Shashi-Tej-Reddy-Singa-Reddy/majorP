# # # # # # # # # # from flask import Flask, request, render_template, send_file, redirect, url_for
# # # # # # # # # # from werkzeug.utils import secure_filename
# # # # # # # # # # import os
# # # # # # # # # # import zipfile
# # # # # # # # # # from io import BytesIO
# # # # # # # # # # from PIL import Image, ImageEnhance, ImageOps
# # # # # # # # # # import numpy as np

# # # # # # # # # # app = Flask(__name__)

# # # # # # # # # # UPLOAD_FOLDER = 'uploaded_images'
# # # # # # # # # # AUGMENTED_FOLDER = 'augmented_images'
# # # # # # # # # # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# # # # # # # # # # app.config['AUGMENTED_FOLDER'] = AUGMENTED_FOLDER

# # # # # # # # # # # Ensure directories exist
# # # # # # # # # # if not os.path.exists(UPLOAD_FOLDER):
# # # # # # # # # #     os.makedirs(UPLOAD_FOLDER)

# # # # # # # # # # if not os.path.exists(AUGMENTED_FOLDER):
# # # # # # # # # #     os.makedirs(AUGMENTED_FOLDER)

# # # # # # # # # # # Function to apply augmentations
# # # # # # # # # # def apply_augmentations(image, techniques):
# # # # # # # # # #     for technique in techniques:
# # # # # # # # # #         if technique == 'rotation':
# # # # # # # # # #             image = image.rotate(45)
# # # # # # # # # #         elif technique == 'scaling':
# # # # # # # # # #             image = image.resize((int(image.width * 1.5), int(image.height * 1.5)))
# # # # # # # # # #         elif technique == 'translation':
# # # # # # # # # #             image = ImageOps.offset(image, 50, 50)
# # # # # # # # # #         elif technique == 'shearing':
# # # # # # # # # #             matrix = (1, 0.5, 0, 0.5, 1, 0)
# # # # # # # # # #             image = image.transform(image.size, Image.AFFINE, matrix)
# # # # # # # # # #         elif technique == 'flipping':
# # # # # # # # # #             image = ImageOps.mirror(image)
# # # # # # # # # #         elif technique == 'cropping':
# # # # # # # # # #             image = image.crop((10, 10, image.width - 10, image.height - 10))
# # # # # # # # # #         elif technique == 'padding':
# # # # # # # # # #             image = ImageOps.expand(image, border=20, fill='black')
# # # # # # # # # #         elif technique == 'brightness':
# # # # # # # # # #             enhancer = ImageEnhance.Brightness(image)
# # # # # # # # # #             image = enhancer.enhance(1.5)
# # # # # # # # # #         elif technique == 'contrast':
# # # # # # # # # #             enhancer = ImageEnhance.Contrast(image)
# # # # # # # # # #             image = enhancer.enhance(1.5)
# # # # # # # # # #         elif technique == 'saturation':
# # # # # # # # # #             enhancer = ImageEnhance.Color(image)
# # # # # # # # # #             image = enhancer.enhance(1.5)
# # # # # # # # # #         elif technique == 'hue':
# # # # # # # # # #             image = image.convert('HSV')
# # # # # # # # # #             np_img = np.array(image)
# # # # # # # # # #             np_img[..., 0] = (np_img[..., 0] + 50) % 255
# # # # # # # # # #             image = Image.fromarray(np_img, 'HSV').convert('RGB')
# # # # # # # # # #         elif technique == 'grayscale':
# # # # # # # # # #             image = ImageOps.grayscale(image)
# # # # # # # # # #         elif technique == 'color_jittering':
# # # # # # # # # #             image = ImageEnhance.Color(image).enhance(np.random.uniform(0.8, 1.2))
# # # # # # # # # #     return image

# # # # # # # # # # @app.route('/')
# # # # # # # # # # def index():
# # # # # # # # # #     return render_template('index.html')

# # # # # # # # # # @app.route('/upload', methods=['POST'])
# # # # # # # # # # def upload():
# # # # # # # # # #     files = request.files.getlist('images')
# # # # # # # # # #     for file in files:
# # # # # # # # # #         filename = secure_filename(file.filename)
# # # # # # # # # #         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
# # # # # # # # # #     return redirect(url_for('select_augmentations'))

# # # # # # # # # # @app.route('/select_augmentations')
# # # # # # # # # # def select_augmentations():
# # # # # # # # # #     return render_template('select_augmentations.html')

# # # # # # # # # # @app.route('/apply_augmentations', methods=['POST'])
# # # # # # # # # # def apply_augmentations_route():
# # # # # # # # # #     techniques = request.form.getlist('augmentations')
# # # # # # # # # #     version = len(os.listdir(app.config['AUGMENTED_FOLDER'])) + 1
# # # # # # # # # #     version_folder = os.path.join(app.config['AUGMENTED_FOLDER'], f'version_{version}')
# # # # # # # # # #     os.makedirs(version_folder)

# # # # # # # # # #     for filename in os.listdir(app.config['UPLOAD_FOLDER']):
# # # # # # # # # #         image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
# # # # # # # # # #         image = Image.open(image_path)
# # # # # # # # # #         augmented_image = apply_augmentations(image, techniques)
# # # # # # # # # #         augmented_image.save(os.path.join(version_folder, filename))

# # # # # # # # # #     return redirect(url_for('download'))

# # # # # # # # # # @app.route('/download')
# # # # # # # # # # def download():
# # # # # # # # # #     versions = [folder.split('_')[-1] for folder in os.listdir(app.config['AUGMENTED_FOLDER']) if folder.startswith('version_')]
# # # # # # # # # #     versions.sort(key=int)
# # # # # # # # # #     return render_template('download.html', versions=versions)

# # # # # # # # # # @app.route('/download_zip/<int:version>')
# # # # # # # # # # def download_zip(version):
# # # # # # # # # #     version_folder = os.path.join(app.config['AUGMENTED_FOLDER'], f'version_{version}')
    
# # # # # # # # # #     memory_file = BytesIO()
# # # # # # # # # #     with zipfile.ZipFile(memory_file, 'w') as zf:
# # # # # # # # # #         for filename in os.listdir(version_folder):
# # # # # # # # # #             file_path = os.path.join(version_folder, filename)
# # # # # # # # # #             zf.write(file_path, arcname=filename)
    
# # # # # # # # # #     memory_file.seek(0)
    
# # # # # # # # # #     return send_file(memory_file, as_attachment=True, download_name=f'version_{version}.zip', mimetype='application/zip')

# # # # # # # # # # if __name__ == '__main__':
# # # # # # # # # #     app.run(debug=True)






# # # # # # # # # from flask import Flask, request, render_template, send_file, redirect, url_for, session
# # # # # # # # # from werkzeug.utils import secure_filename
# # # # # # # # # import os
# # # # # # # # # import zipfile
# # # # # # # # # from io import BytesIO
# # # # # # # # # from PIL import Image, ImageEnhance, ImageOps
# # # # # # # # # import numpy as np

# # # # # # # # # app = Flask(__name__)
# # # # # # # # # app.secret_key = 'secret_key'

# # # # # # # # # UPLOAD_FOLDER = 'uploaded_images'
# # # # # # # # # AUGMENTED_FOLDER = 'augmented_images'
# # # # # # # # # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# # # # # # # # # app.config['AUGMENTED_FOLDER'] = AUGMENTED_FOLDER

# # # # # # # # # if not os.path.exists(UPLOAD_FOLDER):
# # # # # # # # #     os.makedirs(UPLOAD_FOLDER)

# # # # # # # # # if not os.path.exists(AUGMENTED_FOLDER):
# # # # # # # # #     os.makedirs(AUGMENTED_FOLDER)

# # # # # # # # # def apply_augmentations(image, techniques, params):
# # # # # # # # #     for technique in techniques:
# # # # # # # # #         if technique == 'rotation':
# # # # # # # # #             angle = float(params.get('rotation_angle', 0))
# # # # # # # # #             image = image.rotate(angle)
# # # # # # # # #         elif technique == 'scaling':
# # # # # # # # #             factor = float(params.get('scaling_factor', 1))
# # # # # # # # #             image = image.resize((int(image.width * factor), int(image.height * factor)))
# # # # # # # # #         elif technique == 'brightness':
# # # # # # # # #             enhancer = ImageEnhance.Brightness(image)
# # # # # # # # #             image = enhancer.enhance(float(params.get('brightness_factor', 1)))
# # # # # # # # #         elif technique == 'contrast':
# # # # # # # # #             enhancer = ImageEnhance.Contrast(image)
# # # # # # # # #             image = enhancer.enhance(float(params.get('contrast_factor', 1)))
# # # # # # # # #         elif technique == 'flipping':
# # # # # # # # #             image = ImageOps.mirror(image)
# # # # # # # # #     return image

# # # # # # # # # @app.route('/')
# # # # # # # # # def index():
# # # # # # # # #     return render_template('index.html')

# # # # # # # # # @app.route('/upload', methods=['POST'])
# # # # # # # # # def upload():
# # # # # # # # #     files = request.files.getlist('images')
# # # # # # # # #     for file in files:
# # # # # # # # #         filename = secure_filename(file.filename)
# # # # # # # # #         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
# # # # # # # # #     session['uploaded_files'] = os.listdir(app.config['UPLOAD_FOLDER'])
# # # # # # # # #     return redirect(url_for('select_augmentations'))

# # # # # # # # # @app.route('/select_augmentations')
# # # # # # # # # def select_augmentations():
# # # # # # # # #     return render_template('select_augmentations.html')

# # # # # # # # # @app.route('/set_augmentation_count', methods=['POST'])
# # # # # # # # # def set_augmentation_count():
# # # # # # # # #     augmentations = request.form.to_dict()
# # # # # # # # #     max_images = len(session.get('uploaded_files', [])) * 5  # Allow up to 5x augmentation
# # # # # # # # #     return render_template('set_augmentation_count.html', augmentations=augmentations, max_images=max_images)

# # # # # # # # # @app.route('/apply_augmentations', methods=['POST'])
# # # # # # # # # def apply_augmentations_route():
# # # # # # # # #     techniques = request.form.getlist('augmentations')
# # # # # # # # #     params = request.form.to_dict()
# # # # # # # # #     augment_count = int(params.pop('augment_count', 1))

# # # # # # # # #     version = len(os.listdir(app.config['AUGMENTED_FOLDER'])) + 1
# # # # # # # # #     version_folder = os.path.join(app.config['AUGMENTED_FOLDER'], f'version_{version}')
# # # # # # # # #     os.makedirs(version_folder)

# # # # # # # # #     for filename in session.get('uploaded_files', []):
# # # # # # # # #         image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
# # # # # # # # #         image = Image.open(image_path)
# # # # # # # # #         for i in range(augment_count):
# # # # # # # # #             augmented_image = apply_augmentations(image, techniques, params)
# # # # # # # # #             augmented_image.save(os.path.join(version_folder, f"{filename.split('.')[0]}_aug_{i}.png"))

# # # # # # # # #     return redirect(url_for('download'))

# # # # # # # # # @app.route('/download')
# # # # # # # # # def download():
# # # # # # # # #     versions = [folder.split('_')[-1] for folder in os.listdir(app.config['AUGMENTED_FOLDER']) if folder.startswith('version_')]
# # # # # # # # #     versions.sort(key=int)
# # # # # # # # #     return render_template('download.html', versions=versions)

# # # # # # # # # @app.route('/download_zip/<int:version>')
# # # # # # # # # def download_zip(version):
# # # # # # # # #     version_folder = os.path.join(app.config['AUGMENTED_FOLDER'], f'version_{version}')
    
# # # # # # # # #     memory_file = BytesIO()
# # # # # # # # #     with zipfile.ZipFile(memory_file, 'w') as zf:
# # # # # # # # #         for filename in os.listdir(version_folder):
# # # # # # # # #             file_path = os.path.join(version_folder, filename)
# # # # # # # # #             zf.write(file_path, arcname=filename)
    
# # # # # # # # #     memory_file.seek(0)
    
# # # # # # # # #     return send_file(memory_file, as_attachment=True, download_name=f'version_{version}.zip', mimetype='application/zip')

# # # # # # # # # if __name__ == '__main__':
# # # # # # # # #     app.run(debug=True)





# # # # # # # # import json
# # # # # # # # import random
# # # # # # # # from flask import Flask, request, render_template, send_file, redirect, url_for, session
# # # # # # # # from werkzeug.utils import secure_filename
# # # # # # # # import os
# # # # # # # # import zipfile
# # # # # # # # from io import BytesIO
# # # # # # # # from PIL import Image, ImageEnhance, ImageOps

# # # # # # # # app = Flask(__name__)
# # # # # # # # app.secret_key = 'secret_key'

# # # # # # # # UPLOAD_FOLDER = 'uploaded_images'
# # # # # # # # AUGMENTED_FOLDER = 'augmented_images'
# # # # # # # # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# # # # # # # # app.config['AUGMENTED_FOLDER'] = AUGMENTED_FOLDER

# # # # # # # # if not os.path.exists(UPLOAD_FOLDER):
# # # # # # # #     os.makedirs(UPLOAD_FOLDER)

# # # # # # # # if not os.path.exists(AUGMENTED_FOLDER):
# # # # # # # #     os.makedirs(AUGMENTED_FOLDER)

# # # # # # # # def apply_augmentations(image, techniques, params):
# # # # # # # #     for technique in techniques:
# # # # # # # #         if technique == 'rotation':
# # # # # # # #             angle = float(params.get('rotation_angle', 0))
# # # # # # # #             image = image.rotate(angle)
# # # # # # # #         elif technique == 'scaling':
# # # # # # # #             factor = float(params.get('scaling_factor', 1))
# # # # # # # #             image = image.resize((int(image.width * factor), int(image.height * factor)))
# # # # # # # #         elif technique == 'brightness':
# # # # # # # #             enhancer = ImageEnhance.Brightness(image)
# # # # # # # #             image = enhancer.enhance(float(params.get('brightness_factor', 1)))
# # # # # # # #         elif technique == 'contrast':
# # # # # # # #             enhancer = ImageEnhance.Contrast(image)
# # # # # # # #             image = enhancer.enhance(float(params.get('contrast_factor', 1)))
# # # # # # # #         elif technique == 'flipping':
# # # # # # # #             image = ImageOps.mirror(image)
# # # # # # # #     return image

# # # # # # # # @app.route('/')
# # # # # # # # def index():
# # # # # # # #     return render_template('index.html')

# # # # # # # # @app.route('/upload', methods=['POST'])
# # # # # # # # def upload():
# # # # # # # #     files = request.files.getlist('images')
# # # # # # # #     for file in files:
# # # # # # # #         filename = secure_filename(file.filename)
# # # # # # # #         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
# # # # # # # #     session['uploaded_files'] = os.listdir(app.config['UPLOAD_FOLDER'])
# # # # # # # #     return redirect(url_for('select_augmentations'))

# # # # # # # # @app.route('/select_augmentations')
# # # # # # # # def select_augmentations():
# # # # # # # #     return render_template('select_augmentations.html')

# # # # # # # # @app.route('/set_augmentation_count', methods=['POST'])
# # # # # # # # def set_augmentation_count():
# # # # # # # #     augmentations = request.form.to_dict()
# # # # # # # #     uploaded_images = len(session.get('uploaded_files', []))  # Get total uploaded images
# # # # # # # #     return render_template('set_augmentation_count.html', augmentations=augmentations, uploaded_images=uploaded_images)

# # # # # # # # @app.route('/apply_augmentations', methods=['POST'])
# # # # # # # # def apply_augmentations_route():
# # # # # # # #     techniques = request.form.getlist('augmentations')
# # # # # # # #     params = request.form.to_dict()
# # # # # # # #     augment_count = int(params.pop('augment_count', 1))

# # # # # # # #     version = len(os.listdir(app.config['AUGMENTED_FOLDER'])) + 1
# # # # # # # #     version_folder = os.path.join(app.config['AUGMENTED_FOLDER'], f'version_{version}')
# # # # # # # #     os.makedirs(version_folder)

# # # # # # # #     uploaded_files = session.get('uploaded_files', [])
# # # # # # # #     selected_files = random.sample(uploaded_files, min(augment_count, len(uploaded_files)))

# # # # # # # #     augmented_images = []
# # # # # # # #     for filename in selected_files:
# # # # # # # #         image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
# # # # # # # #         image = Image.open(image_path)
# # # # # # # #         augmented_image = apply_augmentations(image, techniques, params)
# # # # # # # #         save_path = os.path.join(version_folder, f"{filename.split('.')[0]}_aug.png")
# # # # # # # #         augmented_image.save(save_path)
# # # # # # # #         augmented_images.append(save_path)

# # # # # # # #     metadata = {
# # # # # # # #         "version": version,
# # # # # # # #         "total_augmented_images": len(augmented_images),
# # # # # # # #         "selected_augmentations": techniques,
# # # # # # # #         "augmentation_params": params
# # # # # # # #     }

# # # # # # # #     with open(os.path.join(version_folder, "metadata.json"), "w") as f:
# # # # # # # #         json.dump(metadata, f, indent=4)

# # # # # # # #     return redirect(url_for('download'))

# # # # # # # # @app.route('/download')
# # # # # # # # def download():
# # # # # # # #     versions = {}
    
# # # # # # # #     # Iterate over version folders
# # # # # # # #     for folder in os.listdir(app.config['AUGMENTED_FOLDER']):
# # # # # # # #         if folder.startswith('version_'):
# # # # # # # #             version_number = int(folder.split('_')[-1])
# # # # # # # #             metadata_path = os.path.join(app.config['AUGMENTED_FOLDER'], folder, "metadata.json")

# # # # # # # #             # Read metadata
# # # # # # # #             if os.path.exists(metadata_path):
# # # # # # # #                 with open(metadata_path, 'r') as f:
# # # # # # # #                     metadata = json.load(f)
# # # # # # # #             else:
# # # # # # # #                 metadata = {"total_augmented_images": 0, "selected_augmentations": [], "augmentation_params": {}}

# # # # # # # #             versions[version_number] = metadata

# # # # # # # #     # Sort versions in ascending order
# # # # # # # #     sorted_versions = dict(sorted(versions.items()))

# # # # # # # #     return render_template('download.html', versions=sorted_versions)


# # # # # # # # @app.route('/download_zip/<int:version>')
# # # # # # # # def download_zip(version):
# # # # # # # #     version_folder = os.path.join(app.config['AUGMENTED_FOLDER'], f'version_{version}')
    
# # # # # # # #     memory_file = BytesIO()
# # # # # # # #     with zipfile.ZipFile(memory_file, 'w') as zf:
# # # # # # # #         for filename in os.listdir(version_folder):
# # # # # # # #             file_path = os.path.join(version_folder, filename)
# # # # # # # #             zf.write(file_path, arcname=filename)
    
# # # # # # # #     memory_file.seek(0)
    
# # # # # # # #     return send_file(memory_file, as_attachment=True, download_name=f'version_{version}.zip', mimetype='application/zip')

# # # # # # # # if __name__ == '__main__':
# # # # # # # #     app.run(debug=True)





# # # # # # # import os
# # # # # # # import json
# # # # # # # import random
# # # # # # # import zipfile
# # # # # # # from flask import Flask, request, render_template, send_file, redirect, url_for, session
# # # # # # # from werkzeug.utils import secure_filename
# # # # # # # from io import BytesIO
# # # # # # # from PIL import Image, ImageEnhance, ImageOps

# # # # # # # app = Flask(__name__)
# # # # # # # app.secret_key = 'secret_key'

# # # # # # # UPLOAD_FOLDER = 'uploaded_images'
# # # # # # # AUGMENTED_FOLDER = 'augmented_images'
# # # # # # # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# # # # # # # app.config['AUGMENTED_FOLDER'] = AUGMENTED_FOLDER

# # # # # # # if not os.path.exists(UPLOAD_FOLDER):
# # # # # # #     os.makedirs(UPLOAD_FOLDER)

# # # # # # # if not os.path.exists(AUGMENTED_FOLDER):
# # # # # # #     os.makedirs(AUGMENTED_FOLDER)

# # # # # # # def apply_augmentations(image, techniques, params):
# # # # # # #     if "rotation" in techniques:
# # # # # # #         image = image.rotate(float(params.get("rotation_angle", 0)))
# # # # # # #     if "scaling" in techniques:
# # # # # # #         scale = float(params.get("scaling_factor", 1))
# # # # # # #         image = image.resize((int(image.width * scale), int(image.height * scale)))
# # # # # # #     if "flipping" in techniques:
# # # # # # #         image = ImageOps.mirror(image)
# # # # # # #     if "brightness" in techniques:
# # # # # # #         enhancer = ImageEnhance.Brightness(image)
# # # # # # #         image = enhancer.enhance(float(params.get("brightness_factor", 1)))
# # # # # # #     if "contrast" in techniques:
# # # # # # #         enhancer = ImageEnhance.Contrast(image)
# # # # # # #         image = enhancer.enhance(float(params.get("contrast_factor", 1)))
# # # # # # #     if "grayscale" in techniques:
# # # # # # #         image = ImageOps.grayscale(image)
# # # # # # #     return image

# # # # # # # @app.route('/')
# # # # # # # def index():
# # # # # # #     return render_template('index.html')

# # # # # # # @app.route('/upload', methods=['POST'])
# # # # # # # def upload():
# # # # # # #     files = request.files.getlist('images')
# # # # # # #     for file in files:
# # # # # # #         filename = secure_filename(file.filename)
# # # # # # #         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
# # # # # # #     session['uploaded_files'] = os.listdir(app.config['UPLOAD_FOLDER'])
# # # # # # #     return redirect(url_for('select_augmentations'))

# # # # # # # @app.route('/select_augmentations')
# # # # # # # def select_augmentations():
# # # # # # #     return render_template('select_augmentations.html')

# # # # # # # @app.route('/set_augmentation_count', methods=['POST'])
# # # # # # # def set_augmentation_count():
# # # # # # #     augmentations = request.form.to_dict()
# # # # # # #     uploaded_images = len(session.get('uploaded_files', []))
# # # # # # #     return render_template('set_augmentation_count.html', augmentations=augmentations, uploaded_images=uploaded_images)

# # # # # # # @app.route('/apply_augmentations', methods=['POST'])
# # # # # # # def apply_augmentations_route():
# # # # # # #     techniques = request.form.getlist('augmentations')
# # # # # # #     params = request.form.to_dict()
# # # # # # #     augment_count = int(params.pop('augment_count', 1))

# # # # # # #     version = len(os.listdir(app.config['AUGMENTED_FOLDER'])) + 1
# # # # # # #     version_folder = os.path.join(app.config['AUGMENTED_FOLDER'], f'version_{version}')
# # # # # # #     os.makedirs(version_folder)

# # # # # # #     uploaded_files = session.get('uploaded_files', [])
# # # # # # #     selected_files = random.sample(uploaded_files, min(augment_count, len(uploaded_files)))

# # # # # # #     augmented_images = []
# # # # # # #     for filename in selected_files:
# # # # # # #         image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
# # # # # # #         image = Image.open(image_path)
# # # # # # #         augmented_image = apply_augmentations(image, techniques, params)
# # # # # # #         save_path = os.path.join(version_folder, f"{filename.split('.')[0]}_aug.png")
# # # # # # #         augmented_image.save(save_path)
# # # # # # #         augmented_images.append(save_path)

# # # # # # #     metadata = {
# # # # # # #         "version": version,
# # # # # # #         "total_augmented_images": len(augmented_images),
# # # # # # #         "selected_augmentations": techniques,
# # # # # # #         "augmentation_params": params
# # # # # # #     }

# # # # # # #     with open(os.path.join(version_folder, "metadata.json"), "w") as f:
# # # # # # #         json.dump(metadata, f, indent=4)

# # # # # # #     return redirect(url_for('download'))

# # # # # # # if __name__ == '__main__':
# # # # # # #     app.run(debug=True)



# # # # # # import os
# # # # # # import json
# # # # # # import random
# # # # # # import zipfile
# # # # # # from flask import Flask, request, render_template, send_file, redirect, url_for, session
# # # # # # from werkzeug.utils import secure_filename
# # # # # # from io import BytesIO
# # # # # # from PIL import Image, ImageEnhance, ImageOps

# # # # # # app = Flask(__name__)
# # # # # # app.secret_key = 'secret_key'

# # # # # # UPLOAD_FOLDER = 'uploaded_images'
# # # # # # AUGMENTED_FOLDER = 'augmented_images'
# # # # # # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# # # # # # app.config['AUGMENTED_FOLDER'] = AUGMENTED_FOLDER

# # # # # # if not os.path.exists(UPLOAD_FOLDER):
# # # # # #     os.makedirs(UPLOAD_FOLDER)

# # # # # # if not os.path.exists(AUGMENTED_FOLDER):
# # # # # #     os.makedirs(AUGMENTED_FOLDER)

# # # # # # def apply_augmentations(image, techniques, params):
# # # # # #     if "rotation" in techniques and "rotation_angle" in params:
# # # # # #         image = image.rotate(float(params["rotation_angle"]), expand=True)

# # # # # #     if "scaling" in techniques and "scaling_factor" in params:
# # # # # #         scale = float(params["scaling_factor"])
# # # # # #         image = image.resize((int(image.width * scale), int(image.height * scale)))

# # # # # #     if "translation" in techniques and "translation_x" in params and "translation_y" in params:
# # # # # #         x_offset = int(params["translation_x"])
# # # # # #         y_offset = int(params["translation_y"])
# # # # # #         image = ImageOps.expand(image, border=(x_offset, y_offset, 0, 0), fill="black")

# # # # # #     if "flipping" in techniques:
# # # # # #         image = ImageOps.mirror(image)

# # # # # #     if "brightness" in techniques and "brightness_factor" in params:
# # # # # #         enhancer = ImageEnhance.Brightness(image)
# # # # # #         image = enhancer.enhance(float(params["brightness_factor"]))

# # # # # #     if "contrast" in techniques and "contrast_factor" in params:
# # # # # #         enhancer = ImageEnhance.Contrast(image)
# # # # # #         image = enhancer.enhance(float(params["contrast_factor"]))

# # # # # #     if "grayscale" in techniques:
# # # # # #         image = ImageOps.grayscale(image)

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
# # # # # #     session['uploaded_files'] = os.listdir(app.config['UPLOAD_FOLDER'])
# # # # # #     return redirect(url_for('select_augmentations'))

# # # # # # @app.route('/select_augmentations')
# # # # # # def select_augmentations():
# # # # # #     return render_template('select_augmentations.html')

# # # # # # @app.route('/set_augmentation_count', methods=['POST'])
# # # # # # def set_augmentation_count():
# # # # # #     augmentations = request.form.to_dict()
# # # # # #     uploaded_images = len(session.get('uploaded_files', []))
# # # # # #     return render_template('set_augmentation_count.html', augmentations=augmentations, uploaded_images=uploaded_images)

# # # # # # def apply_augmentations(image, techniques, params):
# # # # # #     """Applies selected augmentation techniques to an image."""
    
# # # # # #     if "rotation" in techniques and "rotation_angle" in params:
# # # # # #         angle = float(params["rotation_angle"])
# # # # # #         image = image.rotate(angle, expand=True)  # Ensures rotated image fits properly
    
# # # # # #     if "scaling" in techniques and "scaling_factor" in params:
# # # # # #         scale = float(params["scaling_factor"])
# # # # # #         new_size = (int(image.width * scale), int(image.height * scale))
# # # # # #         image = image.resize(new_size, Image.ANTIALIAS)

# # # # # #     if "translation" in techniques and "translation_x" in params and "translation_y" in params:
# # # # # #         x_offset = int(params["translation_x"])
# # # # # #         y_offset = int(params["translation_y"])
# # # # # #         new_image = Image.new("RGB", (image.width + abs(x_offset), image.height + abs(y_offset)), "black")
# # # # # #         new_image.paste(image, (max(0, x_offset), max(0, y_offset)))
# # # # # #         image = new_image

# # # # # #     if "flipping" in techniques:
# # # # # #         image = ImageOps.mirror(image)

# # # # # #     if "brightness" in techniques and "brightness_factor" in params:
# # # # # #         enhancer = ImageEnhance.Brightness(image)
# # # # # #         image = enhancer.enhance(float(params["brightness_factor"]))

# # # # # #     if "contrast" in techniques and "contrast_factor" in params:
# # # # # #         enhancer = ImageEnhance.Contrast(image)
# # # # # #         image = enhancer.enhance(float(params["contrast_factor"]))

# # # # # #     if "grayscale" in techniques:
# # # # # #         image = ImageOps.grayscale(image)

# # # # # #     return image


# # # # # # @app.route('/download')
# # # # # # def download():
# # # # # #     versions = {}

# # # # # #     # Iterate over version folders
# # # # # #     for folder in os.listdir(app.config['AUGMENTED_FOLDER']):
# # # # # #         if folder.startswith('version_'):
# # # # # #             version_number = int(folder.split('_')[-1])
# # # # # #             metadata_path = os.path.join(app.config['AUGMENTED_FOLDER'], folder, "metadata.json")

# # # # # #             # Read metadata
# # # # # #             if os.path.exists(metadata_path):
# # # # # #                 with open(metadata_path, 'r') as f:
# # # # # #                     metadata = json.load(f)
# # # # # #             else:
# # # # # #                 metadata = {"total_augmented_images": 0, "selected_augmentations": [], "augmentation_params": {}}

# # # # # #             versions[version_number] = metadata

# # # # # #     # Sort versions in ascending order
# # # # # #     sorted_versions = dict(sorted(versions.items()))

# # # # # #     return render_template('download.html', versions=sorted_versions)

# # # # # # @app.route('/download_zip/<version>')
# # # # # # def download_zip(version):
# # # # # #     version_folder = os.path.join(app.config['AUGMENTED_FOLDER'], version)
# # # # # #     zip_filename = f"{version}.zip"

# # # # # #     # Create an in-memory ZIP file
# # # # # #     memory_file = BytesIO()
# # # # # #     with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
# # # # # #         for root, _, files in os.walk(version_folder):
# # # # # #             for file in files:
# # # # # #                 if file.endswith('.png') or file.endswith('.jpg'):
# # # # # #                     file_path = os.path.join(root, file)
# # # # # #                     zipf.write(file_path, os.path.relpath(file_path, version_folder))

# # # # # #     memory_file.seek(0)

# # # # # #     return send_file(memory_file, download_name=zip_filename, as_attachment=True)

# # # # # # if __name__ == '__main__':
# # # # # #     app.run(debug=True)



# # # # # import os
# # # # # import json
# # # # # import zipfile
# # # # # from flask import Flask, request, render_template, send_file, redirect, url_for, session
# # # # # from werkzeug.utils import secure_filename
# # # # # from io import BytesIO
# # # # # from PIL import Image, ImageEnhance, ImageOps

# # # # # app = Flask(__name__)
# # # # # app.secret_key = 'your_secret_key_here'  # Replace with a secure, random key for production

# # # # # UPLOAD_FOLDER = 'uploaded_images'
# # # # # AUGMENTED_FOLDER = 'augmented_images'
# # # # # ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
# # # # # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# # # # # app.config['AUGMENTED_FOLDER'] = AUGMENTED_FOLDER

# # # # # # Ensure the upload and augmented directories exist
# # # # # os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# # # # # os.makedirs(AUGMENTED_FOLDER, exist_ok=True)

# # # # # def allowed_file(filename):
# # # # #     """Check if the file has an allowed extension."""
# # # # #     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# # # # # def apply_augmentations(image, techniques, params):
# # # # #     """Applies selected augmentation techniques to an image."""

# # # # #     # Geometric Transformations
# # # # #     if "rotation" in techniques and "rotation_angle" in params:
# # # # #         angle = float(params["rotation_angle"])
# # # # #         image = image.rotate(angle, expand=True)

# # # # #     if "scaling" in techniques and "scaling_factor" in params:
# # # # #         scale = float(params["scaling_factor"])
# # # # #         new_size = (int(image.width * scale), int(image.height * scale))
# # # # #         image = image.resize(new_size, Image.LANCZOS)

# # # # #     if "translation" in techniques and "translation_x" in params and "translation_y" in params:
# # # # #         x_offset = int(params["translation_x"])
# # # # #         y_offset = int(params["translation_y"])
# # # # #         new_width = image.width + abs(x_offset)
# # # # #         new_height = image.height + abs(y_offset)
# # # # #         new_image = Image.new("RGB", (new_width, new_height), "black")
# # # # #         new_image.paste(image, (max(0, x_offset), max(0, y_offset)))
# # # # #         image = new_image

# # # # #     if "flipping" in techniques:
# # # # #         image = ImageOps.mirror(image)

# # # # #     # Color Transformations
# # # # #     if "brightness" in techniques and "brightness_factor" in params:
# # # # #         enhancer = ImageEnhance.Brightness(image)
# # # # #         image = enhancer.enhance(float(params["brightness_factor"]))

# # # # #     if "contrast" in techniques and "contrast_factor" in params:
# # # # #         enhancer = ImageEnhance.Contrast(image)
# # # # #         image = enhancer.enhance(float(params["contrast_factor"]))

# # # # #     if "grayscale" in techniques:
# # # # #         image = ImageOps.grayscale(image)

# # # # #     return image

# # # # # @app.route('/')
# # # # # def index():
# # # # #     return render_template('index.html')

# # # # # @app.route('/upload', methods=['POST'])
# # # # # def upload():
# # # # #     files = request.files.getlist('images')
# # # # #     for file in files:
# # # # #         if file and allowed_file(file.filename):
# # # # #             filename = secure_filename(file.filename)
# # # # #             filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
# # # # #             file.save(filepath)
# # # # #     session['uploaded_files'] = os.listdir(app.config['UPLOAD_FOLDER'])
# # # # #     return redirect(url_for('select_augmentations'))

# # # # # @app.route('/select_augmentations', methods=['GET', 'POST'])
# # # # # def select_augmentations():
# # # # #     if request.method == 'POST':
# # # # #         augmentations = request.form.to_dict()
# # # # #         session['augmentations'] = augmentations
# # # # #         uploaded_images = len(session.get('uploaded_files', []))
# # # # #         return render_template('set_augmentation_count.html', augmentations=augmentations, uploaded_images=uploaded_images)
# # # # #     return render_template('select_augmentations.html')

# # # # # @app.route('/set_augmentation_count', methods=['POST'])
# # # # # def set_augmentation_count():
# # # # #     augment_count = int(request.form.get('augment_count', 1))
# # # # #     session['augment_count'] = augment_count
# # # # #     return redirect(url_for('apply_augmentations_route'))

# # # # # @app.route('/apply_augmentations', methods=['GET', 'POST'])
# # # # # def apply_augmentations_route():
# # # # #     uploaded_files = session.get('uploaded_files', [])
# # # # #     augmentations = session.get('augmentations', {})
# # # # #     augment_count = session.get('augment_count', 1)
# # # # #     params = augmentations.copy()

# # # # #     # Prepare techniques list
# # # # #     techniques = [key for key, value in augmentations.items() if value == 'yes']

# # # # #     # Prepare versioning
# # # # #     existing_versions = [int(d.split('_')[-1]) for d in os.listdir(app.config['AUGMENTED_FOLDER']) if d.startswith('version_')]
# # # # #     version_number = max(existing_versions + [0]) + 1
# # # # #     version_folder = os.path.join(app.config['AUGMENTED_FOLDER'], f"version_{version_number}")
# # # # #     os.makedirs(version_folder, exist_ok=True)

# # # # #     total_augmented_images = 0

# # # # #     # Apply augmentations
# # # # #     for i in range(augment_count):
# # # # #         for filename in uploaded_files:
# # # # #             filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
# # # # #             image = Image.open(filepath)

# # # # #             augmented_image = apply_augmentations(image, techniques, params)
# # # # #             file_root, file_ext = os.path.splitext(filename)
# # # # #             augmented_filename = f"{file_root}_aug_{i}{file_ext}"
# # # # #             augmented_filepath = os.path.join(version_folder, augmented_filename)
# # # # #             augmented_image.save(augmented_filepath)
# # # # #             total_augmented_images += 1

# # # # #     # Save metadata
# # # # #     metadata = {
# # # # #         "total_augmented_images": total_augmented_images,
# # # # #         "selected_augmentations": techniques,
# # # # #         "augmentation_params": params
# # # # #     }
# # # # #     with open(os.path.join(version_folder, "metadata.json"), 'w') as f:
# # # # #         json.dump(metadata, f, indent=4)

# # # # #     # Clear uploaded images after processing
# # # # #     session.pop('uploaded_files', None)
# # # # #     session.pop('augmentations', None)
# # # # #     session.pop('augment_count', None)

# # # # #     # Optionally, clear the uploaded_images folder after processing
# # # # #     for file in os.listdir(app.config['UPLOAD_FOLDER']):
# # # # #         os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))

# # # # #     return redirect(url_for('download'))

# # # # # @app.route('/download')
# # # # # def download():
# # # # #     versions = {}

# # # # #     # Iterate over version folders
# # # # #     for folder in os.listdir(app.config['AUGMENTED_FOLDER']):
# # # # #         if folder.startswith('version_'):
# # # # #             version_number = int(folder.split('_')[-1])
# # # # #             metadata_path = os.path.join(app.config['AUGMENTED_FOLDER'], folder, "metadata.json")

# # # # #             # Read metadata
# # # # #             if os.path.exists(metadata_path):
# # # # #                 with open(metadata_path, 'r') as f:
# # # # #                     metadata = json.load(f)
# # # # #             else:
# # # # #                 metadata = {"total_augmented_images": 0, "selected_augmentations": [], "augmentation_params": {}}

# # # # #             versions[version_number] = metadata

# # # # #     # Sort versions in descending order (most recent first)
# # # # #     sorted_versions = dict(sorted(versions.items(), reverse=True))

# # # # #     return render_template('download.html', versions=sorted_versions)

# # # # # @app.route('/download_zip/<version>')
# # # # # def download_zip(version):
# # # # #     version_folder = os.path.join(app.config['AUGMENTED_FOLDER'], version)
# # # # #     zip_filename = f"{version}.zip"

# # # # #     # Create an in-memory ZIP file
# # # # #     memory_file = BytesIO()
# # # # #     with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
# # # # #         for root, _, files in os.walk(version_folder):
# # # # #             for file in files:
# # # # #                 if file.endswith(('.png', '.jpg', '.jpeg', '.gif')):
# # # # #                     file_path = os.path.join(root, file)
# # # # #                     zipf.write(file_path, os.path.relpath(file_path, version_folder))

# # # # #     memory_file.seek(0)

# # # # #     return send_file(memory_file, download_name=zip_filename, as_attachment=True)

# # # # # if __name__ == '__main__':
# # # # #     app.run(debug=True)




# # # # import os
# # # # import json
# # # # import zipfile
# # # # from flask import Flask, request, render_template, send_file, redirect, url_for, session
# # # # from werkzeug.utils import secure_filename
# # # # from io import BytesIO
# # # # from PIL import Image, ImageEnhance, ImageOps

# # # # app = Flask(__name__)
# # # # app.secret_key = 'your_secret_key_here'  # Replace with a secure, random key for production

# # # # UPLOAD_FOLDER = 'uploaded_images'
# # # # AUGMENTED_FOLDER = 'augmented_images'
# # # # ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
# # # # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# # # # app.config['AUGMENTED_FOLDER'] = AUGMENTED_FOLDER

# # # # # Ensure the upload and augmented directories exist
# # # # os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# # # # os.makedirs(AUGMENTED_FOLDER, exist_ok=True)

# # # # def allowed_file(filename):
# # # #     """Check if the file has an allowed extension."""
# # # #     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# # # # def apply_augmentations(image, techniques, params):
# # # #     """Applies selected augmentation techniques to an image."""

# # # #     # Geometric Transformations
# # # #     if "rotation" in techniques and "rotation_angle" in params:
# # # #         angle = float(params["rotation_angle"])
# # # #         image = image.rotate(angle, expand=True)

# # # #     if "scaling" in techniques and "scaling_factor" in params:
# # # #         scale = float(params["scaling_factor"])
# # # #         new_size = (int(image.width * scale), int(image.height * scale))
# # # #         image = image.resize(new_size, Image.LANCZOS)

# # # #     if "translation" in techniques and "translation_x" in params and "translation_y" in params:
# # # #         x_offset = int(params["translation_x"])
# # # #         y_offset = int(params["translation_y"])
# # # #         new_width = image.width + abs(x_offset)
# # # #         new_height = image.height + abs(y_offset)
# # # #         new_image = Image.new("RGB", (new_width, new_height), "black")
# # # #         new_image.paste(image, (max(0, x_offset), max(0, y_offset)))
# # # #         image = new_image

# # # #     if "flipping_horizontal" in techniques:
# # # #         image = ImageOps.mirror(image)  # Horizontal flip

# # # #     if "flipping_vertical" in techniques:
# # # #         image = ImageOps.flip(image)  # Vertical flip

# # # #     # Color Transformations
# # # #     if "brightness" in techniques and "brightness_factor" in params:
# # # #         enhancer = ImageEnhance.Brightness(image)
# # # #         image = enhancer.enhance(float(params["brightness_factor"]))

# # # #     if "contrast" in techniques and "contrast_factor" in params:
# # # #         enhancer = ImageEnhance.Contrast(image)
# # # #         image = enhancer.enhance(float(params["contrast_factor"]))

# # # #     if "grayscale" in techniques:
# # # #         image = ImageOps.grayscale(image)
# # # #     # Geometric Transformations

# # # #     if "cropping" in techniques:
# # # #         # Get crop dimensions from params
# # # #         left = int(params.get("crop_left", 0))
# # # #         top = int(params.get("crop_top", 0))
# # # #         right = int(params.get("crop_right", 0))
# # # #         bottom = int(params.get("crop_bottom", 0))
# # # #         width, height = image.size
# # # #         image = image.crop((left, top, width - right, height - bottom))

# # # #     # Padding
# # # #     if "padding" in techniques:
# # # #         padding = int(params.get("padding_size", 0))
# # # #         padding_color = params.get("padding_color", "#000000")  # Default to black
# # # #         image = ImageOps.expand(image, border=padding, fill=padding_color)

# # # #     return image


# # # # @app.route('/')
# # # # def index():
# # # #     return render_template('index.html')

# # # # @app.route('/upload', methods=['POST'])
# # # # def upload():
# # # #     files = request.files.getlist('images')
# # # #     for file in files:
# # # #         if file and allowed_file(file.filename):
# # # #             filename = secure_filename(file.filename)
# # # #             filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
# # # #             file.save(filepath)
# # # #     session['uploaded_files'] = os.listdir(app.config['UPLOAD_FOLDER'])
# # # #     return redirect(url_for('select_augmentations'))

# # # # @app.route('/select_augmentations', methods=['GET', 'POST'])
# # # # def select_augmentations():
# # # #     if request.method == 'POST':
# # # #         augmentations = request.form.to_dict()
# # # #         session['augmentations'] = augmentations
# # # #         uploaded_images = len(session.get('uploaded_files', []))
# # # #         return render_template('set_augmentation_count.html', augmentations=augmentations, uploaded_images=uploaded_images)
# # # #     return render_template('select_augmentations.html')

# # # # @app.route('/set_augmentation_count', methods=['POST'])
# # # # def set_augmentation_count():
# # # #     augment_count = int(request.form.get('augment_count', 1))
# # # #     session['augment_count'] = augment_count
# # # #     return redirect(url_for('apply_augmentations_route'))

# # # # @app.route('/apply_augmentations', methods=['GET', 'POST'])
# # # # def apply_augmentations_route():
# # # #     uploaded_files = session.get('uploaded_files', [])
# # # #     augmentations = session.get('augmentations', {})
# # # #     augment_count = session.get('augment_count', 1)
# # # #     params = augmentations.copy()

# # # #     # Prepare techniques list
# # # #     techniques = [key for key, value in augmentations.items() if value == 'yes']

# # # #     # Prepare versioning
# # # #     existing_versions = [int(d.split('_')[-1]) for d in os.listdir(app.config['AUGMENTED_FOLDER']) if d.startswith('version_')]
# # # #     version_number = max(existing_versions + [0]) + 1
# # # #     version_folder = os.path.join(app.config['AUGMENTED_FOLDER'], f"version_{version_number}")
# # # #     os.makedirs(version_folder, exist_ok=True)

# # # #     total_augmented_images = 0

# # # #     # Apply augmentations
# # # #     for i in range(augment_count):
# # # #         for filename in uploaded_files:
# # # #             filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
# # # #             image = Image.open(filepath)

# # # #             augmented_image = apply_augmentations(image, techniques, params)
# # # #             file_root, file_ext = os.path.splitext(filename)
# # # #             augmented_filename = f"{file_root}_aug_{i}{file_ext}"
# # # #             augmented_filepath = os.path.join(version_folder, augmented_filename)
# # # #             augmented_image.save(augmented_filepath)
# # # #             total_augmented_images += 1

# # # #     # Save metadata
# # # #     metadata = {
# # # #         "total_augmented_images": total_augmented_images,
# # # #         "selected_augmentations": techniques,
# # # #         "augmentation_params": params
# # # #     }
# # # #     with open(os.path.join(version_folder, "metadata.json"), 'w') as f:
# # # #         json.dump(metadata, f, indent=4)

# # # #     # Clear uploaded images after processing
# # # #     session.pop('uploaded_files', None)
# # # #     session.pop('augmentations', None)
# # # #     session.pop('augment_count', None)

# # # #     # Optionally, clear the uploaded_images folder after processing
# # # #     for file in os.listdir(app.config['UPLOAD_FOLDER']):
# # # #         os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))

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

# # # #     # Sort versions in descending order (most recent first)
# # # #     sorted_versions = dict(sorted(versions.items(), reverse=True))

# # # #     return render_template('download.html', versions=sorted_versions)

# # # # @app.route('/download_zip/<version>')
# # # # def download_zip(version):
# # # #     version_folder = os.path.join(app.config['AUGMENTED_FOLDER'], version)
# # # #     zip_filename = f"{version}.zip"

# # # #     # Create an in-memory ZIP file
# # # #     memory_file = BytesIO()
# # # #     with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
# # # #         for root, _, files in os.walk(version_folder):
# # # #             for file in files:
# # # #                 if file.endswith(('.png', '.jpg', '.jpeg', '.gif')):
# # # #                     file_path = os.path.join(root, file)
# # # #                     zipf.write(file_path, os.path.relpath(file_path, version_folder))

# # # #     memory_file.seek(0)

# # # #     return send_file(memory_file, download_name=zip_filename, as_attachment=True)

# # # # if __name__ == '__main__':
# # # #     app.run(debug=True)




# # # import os
# # # import json
# # # import zipfile
# # # import random
# # # import numpy as np
# # # import cv2  # Ensure OpenCV is installed: pip install opencv-python
# # # from flask import Flask, request, render_template, send_file, redirect, url_for, session
# # # from werkzeug.utils import secure_filename
# # # from io import BytesIO
# # # from PIL import Image, ImageEnhance, ImageOps

# # # app = Flask(__name__)
# # # app.secret_key = 'your_secret_key_here'  # Replace with a secure, random key for production

# # # UPLOAD_FOLDER = 'uploaded_images'
# # # AUGMENTED_FOLDER = 'augmented_images'
# # # ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
# # # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# # # app.config['AUGMENTED_FOLDER'] = AUGMENTED_FOLDER

# # # # Ensure the upload and augmented directories exist
# # # os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# # # os.makedirs(AUGMENTED_FOLDER, exist_ok=True)

# # # def allowed_file(filename):
# # #     """Check if the file has an allowed extension."""
# # #     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# # # def add_gaussian_noise(image, mean=0, var=0.01):
# # #     img_array = np.array(image).astype(np.float32) / 255.0
# # #     noise = np.random.normal(mean, var ** 0.5, img_array.shape)
# # #     img_noisy = img_array + noise
# # #     img_noisy = np.clip(img_noisy, 0, 1)
# # #     img_noisy = (img_noisy * 255).astype(np.uint8)
# # #     return Image.fromarray(img_noisy)

# # # def add_salt_pepper_noise(image, amount=0.005, salt_vs_pepper=0.5):
# # #     img_array = np.array(image)
# # #     num_salt = np.ceil(amount * img_array.size * salt_vs_pepper).astype(int)
# # #     num_pepper = np.ceil(amount * img_array.size * (1.0 - salt_vs_pepper)).astype(int)

# # #     # Add Salt noise
# # #     coords = [np.random.randint(0, i - 1, num_salt) for i in img_array.shape]
# # #     img_array[tuple(coords)] = 255

# # #     # Add Pepper noise
# # #     coords = [np.random.randint(0, i - 1, num_pepper) for i in img_array.shape]
# # #     img_array[tuple(coords)] = 0

# # #     return Image.fromarray(img_array)

# # # def add_speckle_noise(image):
# # #     img_array = np.array(image).astype(np.float32) / 255.0
# # #     noise = np.random.randn(*img_array.shape)
# # #     img_noisy = img_array + img_array * noise
# # #     img_noisy = np.clip(img_noisy, 0, 1)
# # #     img_noisy = (img_noisy * 255).astype(np.uint8)
# # #     return Image.fromarray(img_noisy)

# # # def add_motion_blur(image, size=9):
# # #     # Create a motion blur kernel
# # #     kernel = np.zeros((size, size))
# # #     kernel[int((size - 1)/2), :] = np.ones(size)
# # #     kernel = kernel / size
# # #     img_array = np.array(image)
# # #     img_blur = cv2.filter2D(img_array, -1, kernel)
# # #     return Image.fromarray(img_blur)

# # # def apply_cutout(image, mask_size):
# # #     img_array = np.array(image)
# # #     h, w = img_array.shape[:2]
# # #     y = np.random.randint(h)
# # #     x = np.random.randint(w)

# # #     y1 = np.clip(y - mask_size // 2, 0, h)
# # #     y2 = np.clip(y + mask_size // 2, 0, h)
# # #     x1 = np.clip(x - mask_size // 2, 0, w)
# # #     x2 = np.clip(x + mask_size // 2, 0, w)

# # #     img_array[y1:y2, x1:x2] = 0  # Black box
# # #     return Image.fromarray(img_array)

# # # def apply_random_erasing(image, sl=0.02, sh=0.4, r1=0.3):
# # #     img_array = np.array(image)
# # #     h, w = img_array.shape[:2]
# # #     s = np.random.uniform(sl, sh) * h * w
# # #     r = np.random.uniform(r1, 1/r1)
# # #     w_e = int(np.sqrt(s * r))
# # #     h_e = int(np.sqrt(s / r))
# # #     if w_e == 0 or h_e == 0:
# # #         return Image.fromarray(img_array)
# # #     x_e = np.random.randint(0, w - w_e)
# # #     y_e = np.random.randint(0, h - h_e)
# # #     img_array[y_e:y_e+h_e, x_e:x_e+w_e] = np.random.randint(0, 256, (h_e, w_e, 3))
# # #     return Image.fromarray(img_array)

# # # def apply_mixup(image, other_image, alpha=0.4):
# # #     lam = np.random.beta(alpha, alpha)
# # #     image_array = np.array(image).astype(np.float32)
# # #     other_array = np.array(other_image.resize(image.size)).astype(np.float32)
# # #     mixed_array = lam * image_array + (1 - lam) * other_array
# # #     mixed_image = Image.fromarray(mixed_array.astype(np.uint8))
# # #     return mixed_image

# # # def apply_cutmix(image, other_image):
# # #     img_array = np.array(image)
# # #     other_array = np.array(other_image.resize(image.size))
# # #     h, w, _ = img_array.shape
# # #     lam = np.random.beta(1.0, 1.0)
# # #     bbx1 = np.random.randint(0, w)
# # #     bby1 = np.random.randint(0, h)
# # #     bbx2 = np.clip(bbx1 + int(w * np.sqrt(1 - lam)), 0, w)
# # #     bby2 = np.clip(bby1 + int(h * np.sqrt(1 - lam)), 0, h)
# # #     img_array[bby1:bby2, bbx1:bbx2, :] = other_array[bby1:bby2, bbx1:bbx2, :]
# # #     return Image.fromarray(img_array)

# # # def apply_augmentations(image, techniques, params, uploaded_files):
# # #     """Applies selected augmentation techniques to an image."""

# # #     # Geometric Transformations
# # #     if "rotation" in techniques and "rotation_angle" in params:
# # #         angle = float(params["rotation_angle"])
# # #         image = image.rotate(angle, expand=True)

# # #     if "scaling" in techniques and "scaling_factor" in params:
# # #         scale = float(params["scaling_factor"])
# # #         new_size = (int(image.width * scale), int(image.height * scale))
# # #         image = image.resize(new_size, Image.LANCZOS)

# # #     if "translation" in techniques and "translation_x" in params and "translation_y" in params:
# # #         x_offset = int(params["translation_x"])
# # #         y_offset = int(params["translation_y"])
# # #         new_width = image.width + abs(x_offset)
# # #         new_height = image.height + abs(y_offset)
# # #         new_image = Image.new("RGB", (new_width, new_height), "black")
# # #         new_image.paste(image, (max(0, x_offset), max(0, y_offset)))
# # #         image = new_image

# # #     if "flipping_horizontal" in techniques:
# # #         image = ImageOps.mirror(image)  # Horizontal flip

# # #     if "flipping_vertical" in techniques:
# # #         image = ImageOps.flip(image)  # Vertical flip

# # #     if "cropping" in techniques:
# # #         # Get crop dimensions from params
# # #         left = int(params.get("crop_left", 0))
# # #         top = int(params.get("crop_top", 0))
# # #         right = int(params.get("crop_right", 0))
# # #         bottom = int(params.get("crop_bottom", 0))
# # #         width, height = image.size
# # #         image = image.crop((left, top, width - right, height - bottom))

# # #     if "padding" in techniques:
# # #         padding = int(params.get("padding_size", 0))
# # #         padding_color = params.get("padding_color", "#000000")  # Default to black
# # #         image = ImageOps.expand(image, border=padding, fill=padding_color)

# # #     # Color Transformations
# # #     if "brightness" in techniques and "brightness_factor" in params:
# # #         enhancer = ImageEnhance.Brightness(image)
# # #         image = enhancer.enhance(float(params["brightness_factor"]))

# # #     if "contrast" in techniques and "contrast_factor" in params:
# # #         enhancer = ImageEnhance.Contrast(image)
# # #         image = enhancer.enhance(float(params["contrast_factor"]))

# # #     if "grayscale" in techniques:
# # #         image = ImageOps.grayscale(image)

# # #     if "saturation" in techniques and "saturation_factor" in params:
# # #         enhancer = ImageEnhance.Color(image)
# # #         image = enhancer.enhance(float(params["saturation_factor"]))

# # #     # Noise Transformations
# # #     if "gaussian_noise" in techniques:
# # #         var = float(params.get("gaussian_variance", 0.01))
# # #         image = add_gaussian_noise(image, var=var)

# # #     if "salt_pepper_noise" in techniques:
# # #         amount = float(params.get("sap_amount", 0.005))
# # #         image = add_salt_pepper_noise(image, amount=amount)

# # #     if "speckle_noise" in techniques:
# # #         image = add_speckle_noise(image)

# # #     if "motion_blur" in techniques:
# # #         size = int(params.get("motion_blur_size", 9))
# # #         image = add_motion_blur(image, size=size)

# # #     # Occlusion Transformations
# # #     if "cutout" in techniques:
# # #         size = int(params.get("cutout_size", 50))
# # #         image = apply_cutout(image, size)

# # #     if "random_erasing" in techniques:
# # #         image = apply_random_erasing(image)

# # #     if "mixup" in techniques or "cutmix" in techniques:
# # #         if uploaded_files:
# # #             other_filename = random.choice(uploaded_files)
# # #             other_filepath = os.path.join(app.config['UPLOAD_FOLDER'], other_filename)
# # #             other_image = Image.open(other_filepath)
# # #             if "mixup" in techniques:
# # #                 alpha = float(params.get("mixup_alpha", 0.4))
# # #                 image = apply_mixup(image, other_image, alpha)
# # #             if "cutmix" in techniques:
# # #                 image = apply_cutmix(image, other_image)

# # #     return image

# # # @app.route('/')
# # # def index():
# # #     return render_template('index.html')

# # # @app.route('/upload', methods=['POST'])
# # # def upload():
# # #     files = request.files.getlist('images')
# # #     for file in files:
# # #         if file and allowed_file(file.filename):
# # #             filename = secure_filename(file.filename)
# # #             filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
# # #             file.save(filepath)
# # #     session['uploaded_files'] = os.listdir(app.config['UPLOAD_FOLDER'])
# # #     return redirect(url_for('select_augmentations'))

# # # @app.route('/select_augmentations', methods=['GET', 'POST'])
# # # def select_augmentations():
# # #     if request.method == 'POST':
# # #         augmentations = request.form.to_dict()
# # #         session['augmentations'] = augmentations
# # #         uploaded_images = len(session.get('uploaded_files', []))
# # #         return render_template('set_augmentation_count.html', augmentations=augmentations, uploaded_images=uploaded_images)
# # #     return render_template('select_augmentations.html')

# # # @app.route('/set_augmentation_count', methods=['POST'])
# # # def set_augmentation_count():
# # #     augment_count = int(request.form.get('augment_count', 1))
# # #     session['augment_count'] = augment_count
# # #     return redirect(url_for('apply_augmentations_route'))

# # # @app.route('/apply_augmentations', methods=['GET', 'POST'])
# # # def apply_augmentations_route():
# # #     uploaded_files = session.get('uploaded_files', [])
# # #     augmentations = session.get('augmentations', {})
# # #     augment_count = session.get('augment_count', 1)
# # #     params = augmentations.copy()

# # #     # Prepare techniques list
# # #     techniques = [key for key, value in augmentations.items() if value == 'yes']

# # #     # Prepare versioning
# # #     existing_versions = [int(d.split('_')[-1]) for d in os.listdir(app.config['AUGMENTED_FOLDER']) if d.startswith('version_')]
# # #     version_number = max(existing_versions + [0]) + 1
# # #     version_folder = os.path.join(app.config['AUGMENTED_FOLDER'], f"version_{version_number}")
# # #     os.makedirs(version_folder, exist_ok=True)

# # #     total_augmented_images = 0

# # #     # Apply augmentations
# # #     for i in range(augment_count):
# # #         for filename in uploaded_files:
# # #             filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
# # #             image = Image.open(filepath)

# # #             augmented_image = apply_augmentations(image.copy(), techniques, params, uploaded_files)
# # #             file_root, file_ext = os.path.splitext(filename)
# # #             augmented_filename = f"{file_root}_aug_{i}{file_ext}"
# # #             augmented_filepath = os.path.join(version_folder, augmented_filename)
# # #             augmented_image.save(augmented_filepath)
# # #             total_augmented_images += 1

# # #     # Save metadata
# # #     metadata = {
# # #         "total_augmented_images": total_augmented_images,
# # #         "selected_augmentations": techniques,
# # #         "augmentation_params": params
# # #     }
# # #     with open(os.path.join(version_folder, "metadata.json"), 'w') as f:
# # #         json.dump(metadata, f, indent=4)

# # #     # Clear uploaded images after processing
# # #     session.pop('uploaded_files', None)
# # #     session.pop('augmentations', None)
# # #     session.pop('augment_count', None)

# # #     # Optionally, clear the uploaded_images folder after processing
# # #     for file in os.listdir(app.config['UPLOAD_FOLDER']):
# # #         os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))

# # #     return redirect(url_for('download'))

# # # @app.route('/download')
# # # def download():
# # #     versions = {}

# # #     # Iterate over version folders
# # #     for folder in os.listdir(app.config['AUGMENTED_FOLDER']):
# # #         if folder.startswith('version_'):
# # #             version_number = int(folder.split('_')[-1])
# # #             metadata_path = os.path.join(app.config['AUGMENTED_FOLDER'], folder, "metadata.json")

# # #             # Read metadata
# # #             if os.path.exists(metadata_path):
# # #                 with open(metadata_path, 'r') as f:
# # #                     metadata = json.load(f)
# # #             else:
# # #                 metadata = {"total_augmented_images": 0, "selected_augmentations": [], "augmentation_params": {}}

# # #             versions[version_number] = metadata

# # #     # Sort versions in descending order (most recent first)
# # #     sorted_versions = dict(sorted(versions.items(), reverse=True))

# # #     return render_template('download.html', versions=sorted_versions)

# # # @app.route('/download_zip/<version>')
# # # def download_zip(version):
# # #     version_folder = os.path.join(app.config['AUGMENTED_FOLDER'], f"version_{version}")
# # #     zip_filename = f"augmented_images_{version}.zip"

# # #     # Create an in-memory ZIP file
# # #     memory_file = BytesIO()
# # #     with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
# # #         for root, _, files in os.walk(version_folder):
# # #             for file in files:
# # #                 if file.endswith(('.png', '.jpg', '.jpeg', '.gif')):
# # #                     file_path = os.path.join(root, file)
# # #                     zipf.write(file_path, os.path.relpath(file_path, version_folder))
# # #         # Add metadata.json
# # #         metadata_path = os.path.join(version_folder, "metadata.json")
# # #         zipf.write(metadata_path, os.path.relpath(metadata_path, version_folder))

# # #     memory_file.seek(0)

# # #     return send_file(memory_file, download_name=zip_filename, as_attachment=True)

# # # if __name__ == '__main__':
# # #     app.run(debug=True)



# # import os
# # import json
# # import zipfile
# # import random
# # import numpy as np
# # import cv2  # Ensure OpenCV is installed: pip install opencv-python
# # from flask import Flask, request, render_template, send_file, redirect, url_for, session
# # from werkzeug.utils import secure_filename
# # from io import BytesIO
# # from PIL import Image, ImageEnhance, ImageOps

# # app = Flask(__name__)
# # app.secret_key = 'your_secret_key_here'  # Replace with a secure, random key for production

# # UPLOAD_FOLDER = 'uploaded_images'
# # AUGMENTED_FOLDER = 'augmented_images'
# # ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
# # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# # app.config['AUGMENTED_FOLDER'] = AUGMENTED_FOLDER

# # # Ensure the upload and augmented directories exist
# # os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# # os.makedirs(AUGMENTED_FOLDER, exist_ok=True)

# # def allowed_file(filename):
# #     """Check if the file has an allowed extension."""
# #     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# # # [All the augmentation functions remain the same, including apply_augmentations]

# # # ... (Include the augmentation functions and apply_augmentations function here)

# # @app.route('/')
# # def index():
# #     return render_template('index.html')

# # @app.route('/upload', methods=['POST'])
# # def upload():
# #     files = request.files.getlist('images')
# #     for file in files:
# #         if file and allowed_file(file.filename):
# #             filename = secure_filename(file.filename)
# #             filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
# #             file.save(filepath)
# #     session['uploaded_files'] = os.listdir(app.config['UPLOAD_FOLDER'])
# #     return redirect(url_for('select_augmentations'))

# # @app.route('/select_augmentations', methods=['GET', 'POST'])
# # def select_augmentations():
# #     if request.method == 'POST':
# #         augmentations = request.form.to_dict()
# #         session['augmentations'] = augmentations
# #         uploaded_images = len(session.get('uploaded_files', []))
# #         return render_template('set_augmentation_count.html', augmentations=augmentations, uploaded_images=uploaded_images)
# #     return render_template('select_augmentations.html')

# # @app.route('/set_augmentation_count', methods=['POST'])
# # def set_augmentation_count():
# #     images_to_augment = int(request.form.get('images_to_augment', 1))
# #     augment_count = int(request.form.get('augment_count', 1))
# #     session['images_to_augment'] = images_to_augment
# #     session['augment_count'] = augment_count
# #     return redirect(url_for('apply_augmentations_route'))

# # @app.route('/apply_augmentations', methods=['GET', 'POST'])
# # def apply_augmentations_route():
# #     uploaded_files = session.get('uploaded_files', [])
# #     augmentations = session.get('augmentations', {})
# #     images_to_augment = session.get('images_to_augment', len(uploaded_files))
# #     augment_count = session.get('augment_count', 1)
# #     params = augmentations.copy()

# #     # Prepare techniques list
# #     techniques = [key for key, value in augmentations.items() if value == 'yes']

# #     # Prepare versioning
# #     existing_versions = [int(d.split('_')[-1]) for d in os.listdir(app.config['AUGMENTED_FOLDER']) if d.startswith('version_')]
# #     version_number = max(existing_versions + [0]) + 1
# #     version_folder = os.path.join(app.config['AUGMENTED_FOLDER'], f"version_{version_number}")
# #     os.makedirs(version_folder, exist_ok=True)

# #     total_augmented_images = 0

# #     # Ensure images_to_augment does not exceed the number of uploaded files
# #     if images_to_augment > len(uploaded_files):
# #         images_to_augment = len(uploaded_files)

# #     # Randomly select images to augment
# #     images_to_augment_list = random.sample(uploaded_files, images_to_augment)

# #     # Apply augmentations
# #     for i in range(augment_count):
# #         for filename in images_to_augment_list:
# #             filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
# #             image = Image.open(filepath)

# #             augmented_image = apply_augmentations(image.copy(), techniques, params, uploaded_files)
# #             file_root, file_ext = os.path.splitext(filename)
# #             augmented_filename = f"{file_root}_aug_{i}{file_ext}"
# #             augmented_filepath = os.path.join(version_folder, augmented_filename)
# #             augmented_image.save(augmented_filepath)
# #             total_augmented_images += 1

# #     # Save metadata
# #     metadata = {
# #         "total_augmented_images": total_augmented_images,
# #         "selected_augmentations": techniques,
# #         "augmentation_params": params
# #     }
# #     with open(os.path.join(version_folder, "metadata.json"), 'w') as f:
# #         json.dump(metadata, f, indent=4)

# #     # Clear session data
# #     session.pop('uploaded_files', None)
# #     session.pop('augmentations', None)
# #     session.pop('augment_count', None)
# #     session.pop('images_to_augment', None)

# #     # Optionally, clear the uploaded_images folder after processing
# #     for file in os.listdir(app.config['UPLOAD_FOLDER']):
# #         os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))

# #     return redirect(url_for('download'))

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

# #     # Sort versions in descending order (most recent first)
# #     sorted_versions = dict(sorted(versions.items(), reverse=True))

# #     return render_template('download.html', versions=sorted_versions)

# # @app.route('/download_zip/<version>')
# # def download_zip(version):
# #     version_folder = os.path.join(app.config['AUGMENTED_FOLDER'], f"version_{version}")
# #     zip_filename = f"augmented_images_{version}.zip"

# #     # Create an in-memory ZIP file
# #     memory_file = BytesIO()
# #     with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
# #         for root, _, files in os.walk(version_folder):
# #             for file in files:
# #                 if file.endswith(('.png', '.jpg', '.jpeg', '.gif')):
# #                     file_path = os.path.join(root, file)
# #                     zipf.write(file_path, os.path.relpath(file_path, version_folder))
# #         # Add metadata.json
# #         metadata_path = os.path.join(version_folder, "metadata.json")
# #         zipf.write(metadata_path, os.path.relpath(metadata_path, version_folder))

# #     memory_file.seek(0)

# #     return send_file(memory_file, download_name=zip_filename, as_attachment=True)

# # if __name__ == '__main__':
# #     app.run(debug=True)





# import os
# import json
# import zipfile
# import random
# import numpy as np
# import cv2  # Ensure OpenCV is installed: pip install opencv-python
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

# # Augmentation functions (same as before)
# def add_gaussian_noise(image, mean=0, var=0.01):
#     # Function implementation...
#     img_array = np.array(image).astype(np.float32) / 255.0
#     noise = np.random.normal(mean, var ** 0.5, img_array.shape)
#     img_noisy = img_array + noise
#     img_noisy = np.clip(img_noisy, 0, 1)
#     img_noisy = (img_noisy * 255).astype(np.uint8)
#     return Image.fromarray(img_noisy)

# def add_salt_pepper_noise(image, amount=0.005, salt_vs_pepper=0.5):
#     # Function implementation...
#     img_array = np.array(image)
#     num_salt = np.ceil(amount * img_array.size * salt_vs_pepper).astype(int)
#     num_pepper = np.ceil(amount * img_array.size * (1.0 - salt_vs_pepper)).astype(int)

#     # Add Salt noise
#     coords = [np.random.randint(0, i - 1, num_salt) for i in img_array.shape]
#     img_array[tuple(coords)] = 255

#     # Add Pepper noise
#     coords = [np.random.randint(0, i - 1, num_pepper) for i in img_array.shape]
#     img_array[tuple(coords)] = 0

#     return Image.fromarray(img_array)

# def add_speckle_noise(image):
#     # Function implementation...
#     img_array = np.array(image).astype(np.float32) / 255.0
#     noise = np.random.randn(*img_array.shape)
#     img_noisy = img_array + img_array * noise
#     img_noisy = np.clip(img_noisy, 0, 1)
#     img_noisy = (img_noisy * 255).astype(np.uint8)
#     return Image.fromarray(img_noisy)

# def add_motion_blur(image, size=9):
#     # Function implementation...
#     kernel = np.zeros((size, size))
#     kernel[int((size - 1)/2), :] = np.ones(size)
#     kernel = kernel / size
#     img_array = np.array(image)
#     img_blur = cv2.filter2D(img_array, -1, kernel)
#     return Image.fromarray(img_blur)

# def apply_cutout(image, mask_size):
#     # Function implementation...
#     img_array = np.array(image)
#     h, w = img_array.shape[:2]
#     y = np.random.randint(h)
#     x = np.random.randint(w)

#     y1 = np.clip(y - mask_size // 2, 0, h)
#     y2 = np.clip(y + mask_size // 2, 0, h)
#     x1 = np.clip(x - mask_size // 2, 0, w)
#     x2 = np.clip(x + mask_size // 2, 0, w)

#     img_array[y1:y2, x1:x2] = 0  # Black box
#     return Image.fromarray(img_array)

# def apply_random_erasing(image, sl=0.02, sh=0.4, r1=0.3):
#     # Function implementation...
#     img_array = np.array(image)
#     h, w = img_array.shape[:2]
#     s = np.random.uniform(sl, sh) * h * w
#     r = np.random.uniform(r1, 1/r1)
#     w_e = int(np.sqrt(s * r))
#     h_e = int(np.sqrt(s / r))
#     if w_e == 0 or h_e == 0:
#         return Image.fromarray(img_array)
#     x_e = np.random.randint(0, w - w_e)
#     y_e = np.random.randint(0, h - h_e)
#     img_array[y_e:y_e+h_e, x_e:x_e+w_e] = np.random.randint(0, 256, (h_e, w_e, 3))
#     return Image.fromarray(img_array)

# def apply_mixup(image, other_image, alpha=0.4):
#     # Function implementation...
#     lam = np.random.beta(alpha, alpha)
#     image_array = np.array(image).astype(np.float32)
#     other_array = np.array(other_image.resize(image.size)).astype(np.float32)
#     mixed_array = lam * image_array + (1 - lam) * other_array
#     mixed_image = Image.fromarray(mixed_array.astype(np.uint8))
#     return mixed_image

# def apply_cutmix(image, other_image):
#     # Function implementation...
#     img_array = np.array(image)
#     other_array = np.array(other_image.resize(image.size))
#     h, w, _ = img_array.shape
#     lam = np.random.beta(1.0, 1.0)
#     bbx1 = np.random.randint(0, w)
#     bby1 = np.random.randint(0, h)
#     bbx2 = np.clip(bbx1 + int(w * np.sqrt(1 - lam)), 0, w)
#     bby2 = np.clip(bby1 + int(h * np.sqrt(1 - lam)), 0, h)
#     img_array[bby1:bby2, bbx1:bbx2, :] = other_array[bby1:bby2, bbx1:bbx2, :]
#     return Image.fromarray(img_array)

# def apply_augmentations(image, techniques, params, uploaded_files):
#     """Applies selected augmentation techniques to an image."""
#     # The function implementation remains as before, including all the augmentations

#     # Geometric Transformations
#     # ... (rotation, scaling, translation, flipping, cropping, padding)

#     # Color Transformations
#     # ... (brightness, contrast, saturation, grayscale)

#     # Noise Transformations
#     # ... (gaussian_noise, salt_pepper_noise, speckle_noise, motion_blur)

#     # Occlusion Transformations
#     # ... (cutout, random_erasing, mixup, cutmix)

#     return image  # Return the augmented image after applying selected techniques

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
#     # Store the list of uploaded files in the session
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
#     images_to_augment = int(request.form.get('images_to_augment', 1))
#     augment_count = int(request.form.get('augment_count', 1))
#     session['images_to_augment'] = images_to_augment
#     session['augment_count'] = augment_count
#     return redirect(url_for('apply_augmentations_route'))

# @app.route('/apply_augmentations', methods=['GET', 'POST'])
# def apply_augmentations_route():
#     uploaded_files = session.get('uploaded_files', [])
#     augmentations = session.get('augmentations', {})
#     images_to_augment = session.get('images_to_augment', len(uploaded_files))
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

#     # Ensure images_to_augment does not exceed the number of uploaded files
#     if images_to_augment > len(uploaded_files):
#         images_to_augment = len(uploaded_files)

#     # Randomly select images to augment
#     images_to_augment_list = random.sample(uploaded_files, images_to_augment)

#     # Apply augmentations
#     for filename in images_to_augment_list:
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         image = Image.open(filepath)
#         for i in range(augment_count):
#             augmented_image = apply_augmentations(image.copy(), techniques, params, uploaded_files)
#             file_root, file_ext = os.path.splitext(filename)
#             augmented_filename = f"{file_root}_aug_{i}{file_ext}"
#             augmented_filepath = os.path.join(version_folder, augmented_filename)
#             augmented_image.save(augmented_filepath)
#             total_augmented_images += 1

#     # Save metadata
#     metadata = {
#         "total_augmented_images": total_augmented_images,
#         "images_to_augment": images_to_augment,
#         "augment_count": augment_count,
#         "selected_augmentations": techniques,
#         "augmentation_params": params
#     }
#     with open(os.path.join(version_folder, "metadata.json"), 'w') as f:
#         json.dump(metadata, f, indent=4)

#     # Clear session data
#     session.pop('uploaded_files', None)
#     session.pop('augmentations', None)
#     session.pop('augment_count', None)
#     session.pop('images_to_augment', None)

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
#     version_folder = os.path.join(app.config['AUGMENTED_FOLDER'], f"version_{version}")
#     zip_filename = f"augmented_images_{version}.zip"

#     # Create an in-memory ZIP file
#     memory_file = BytesIO()
#     with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
#         for root, _, files in os.walk(version_folder):
#             for file in files:
#                 if file.endswith(('.png', '.jpg', '.jpeg', '.gif')):
#                     file_path = os.path.join(root, file)
#                     zipf.write(file_path, os.path.relpath(file_path, version_folder))
#         # Add metadata.json
#         metadata_path = os.path.join(version_folder, "metadata.json")
#         zipf.write(metadata_path, os.path.relpath(metadata_path, version_folder))

#     memory_file.seek(0)

#     return send_file(memory_file, download_name=zip_filename, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)




import os
import json
import zipfile
import random
import numpy as np
import cv2  # Ensure OpenCV is installed: pip install opencv-python
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

# Augmentation functions
def add_gaussian_noise(image, mean=0, var=0.01):
    img_array = np.array(image).astype(np.float32) / 255.0
    noise = np.random.normal(mean, var ** 0.5, img_array.shape)
    img_noisy = img_array + noise
    img_noisy = np.clip(img_noisy, 0, 1)
    img_noisy = (img_noisy * 255).astype(np.uint8)
    return Image.fromarray(img_noisy)

def add_salt_pepper_noise(image, amount=0.005, salt_vs_pepper=0.5):
    img_array = np.array(image)
    num_salt = np.ceil(amount * img_array.size * salt_vs_pepper).astype(int)
    num_pepper = np.ceil(amount * img_array.size * (1.0 - salt_vs_pepper)).astype(int)

    # Add Salt noise
    coords = [np.random.randint(0, i - 1, num_salt) for i in img_array.shape]
    img_array[tuple(coords)] = 255

    # Add Pepper noise
    coords = [np.random.randint(0, i - 1, num_pepper) for i in img_array.shape]
    img_array[tuple(coords)] = 0

    return Image.fromarray(img_array)

def add_speckle_noise(image):
    img_array = np.array(image).astype(np.float32) / 255.0
    noise = np.random.randn(*img_array.shape)
    img_noisy = img_array + img_array * noise
    img_noisy = np.clip(img_noisy, 0, 1)
    img_noisy = (img_noisy * 255).astype(np.uint8)
    return Image.fromarray(img_noisy)

def add_motion_blur(image, size=9):
    # Create a motion blur kernel
    kernel = np.zeros((size, size))
    kernel[int((size - 1)/2), :] = np.ones(size)
    kernel = kernel / size
    img_array = np.array(image)
    img_blur = cv2.filter2D(img_array, -1, kernel)
    return Image.fromarray(img_blur)

def apply_cutout(image, mask_size):
    img_array = np.array(image)
    h, w = img_array.shape[:2]
    y = np.random.randint(h)
    x = np.random.randint(w)

    y1 = np.clip(y - mask_size // 2, 0, h)
    y2 = np.clip(y + mask_size // 2, 0, h)
    x1 = np.clip(x - mask_size // 2, 0, w)
    x2 = np.clip(x + mask_size // 2, 0, w)

    img_array[y1:y2, x1:x2] = 0  # Black box
    return Image.fromarray(img_array)

def apply_random_erasing(image, sl=0.02, sh=0.4, r1=0.3):
    img_array = np.array(image)
    h, w = img_array.shape[:2]
    s = np.random.uniform(sl, sh) * h * w
    r = np.random.uniform(r1, 1/r1)
    w_e = int(np.sqrt(s * r))
    h_e = int(np.sqrt(s / r))
    if w_e == 0 or h_e == 0:
        return Image.fromarray(img_array)
    x_e = np.random.randint(0, w - w_e)
    y_e = np.random.randint(0, h - h_e)
    img_array[y_e:y_e+h_e, x_e:x_e+w_e] = np.random.randint(0, 256, (h_e, w_e, 3))
    return Image.fromarray(img_array)

def apply_mixup(image, other_image, alpha=0.4):
    lam = np.random.beta(alpha, alpha)
    image_array = np.array(image).astype(np.float32)
    other_array = np.array(other_image.resize(image.size)).astype(np.float32)
    mixed_array = lam * image_array + (1 - lam) * other_array
    mixed_image = Image.fromarray(mixed_array.astype(np.uint8))
    return mixed_image

def apply_cutmix(image, other_image):
    img_array = np.array(image)
    other_array = np.array(other_image.resize(image.size))
    h, w, _ = img_array.shape
    lam = np.random.beta(1.0, 1.0)
    bbx1 = np.random.randint(0, w)
    bby1 = np.random.randint(0, h)
    bbx2 = np.clip(bbx1 + int(w * np.sqrt(1 - lam)), 0, w)
    bby2 = np.clip(bby1 + int(h * np.sqrt(1 - lam)), 0, h)
    img_array[bby1:bby2, bbx1:bbx2, :] = other_array[bby1:bby2, bbx1:bbx2, :]
    return Image.fromarray(img_array)

def apply_augmentations(image, techniques, params, uploaded_files):
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

    if "cropping" in techniques:
        # Get crop dimensions from params
        left = int(params.get("crop_left", 0))
        top = int(params.get("crop_top", 0))
        right = int(params.get("crop_right", 0))
        bottom = int(params.get("crop_bottom", 0))
        width, height = image.size
        image = image.crop((left, top, width - right, height - bottom))

    if "padding" in techniques:
        padding = int(params.get("padding_size", 0))
        padding_color = params.get("padding_color", "#000000")  # Default to black
        image = ImageOps.expand(image, border=padding, fill=padding_color)

    # Color Transformations
    if "brightness" in techniques and "brightness_factor" in params:
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(float(params["brightness_factor"]))

    if "contrast" in techniques and "contrast_factor" in params:
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(float(params["contrast_factor"]))

    if "grayscale" in techniques:
        image = ImageOps.grayscale(image)

    if "saturation" in techniques and "saturation_factor" in params:
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(float(params["saturation_factor"]))

    # Noise Transformations
    if "gaussian_noise" in techniques:
        var = float(params.get("gaussian_variance", 0.01))
        image = add_gaussian_noise(image, var=var)

    if "salt_pepper_noise" in techniques:
        amount = float(params.get("sap_amount", 0.005))
        image = add_salt_pepper_noise(image, amount=amount)

    if "speckle_noise" in techniques:
        image = add_speckle_noise(image)

    if "motion_blur" in techniques:
        size = int(params.get("motion_blur_size", 9))
        image = add_motion_blur(image, size=size)

    # Occlusion Transformations
    if "cutout" in techniques:
        size = int(params.get("cutout_size", 50))
        image = apply_cutout(image, size)

    if "random_erasing" in techniques:
        image = apply_random_erasing(image)

    if "mixup" in techniques or "cutmix" in techniques:
        if uploaded_files:
            other_filename = random.choice(uploaded_files)
            other_filepath = os.path.join(app.config['UPLOAD_FOLDER'], other_filename)
            other_image = Image.open(other_filepath)
            if "mixup" in techniques:
                alpha = float(params.get("mixup_alpha", 0.4))
                image = apply_mixup(image, other_image, alpha)
            if "cutmix" in techniques:
                image = apply_cutmix(image, other_image)

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
    images_to_augment = int(request.form.get('images_to_augment', 1))
    session['images_to_augment'] = images_to_augment
    return redirect(url_for('apply_augmentations_route'))

@app.route('/apply_augmentations', methods=['GET', 'POST'])
def apply_augmentations_route():
    uploaded_files = session.get('uploaded_files', [])
    augmentations = session.get('augmentations', {})
    images_to_augment = session.get('images_to_augment', len(uploaded_files))
    params = augmentations.copy()

    # Prepare techniques list
    techniques = [key for key, value in augmentations.items() if value == 'yes']

    # Prepare versioning
    existing_versions = [int(d.split('_')[-1]) for d in os.listdir(app.config['AUGMENTED_FOLDER']) if d.startswith('version_')]
    version_number = max(existing_versions + [0]) + 1
    version_folder = os.path.join(app.config['AUGMENTED_FOLDER'], f"version_{version_number}")
    os.makedirs(version_folder, exist_ok=True)

    total_augmented_images = 0

    # Ensure images_to_augment does not exceed the number of uploaded files
    if images_to_augment > len(uploaded_files):
        images_to_augment = len(uploaded_files)

    # Randomly select images to augment
    images_to_augment_list = random.sample(uploaded_files, images_to_augment)

    # Apply augmentations
    for filename in images_to_augment_list:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image = Image.open(filepath)

        augmented_image = apply_augmentations(image.copy(), techniques, params, uploaded_files)
        file_root, file_ext = os.path.splitext(filename)
        augmented_filename = f"{file_root}_aug{file_ext}"
        augmented_filepath = os.path.join(version_folder, augmented_filename)
        augmented_image.save(augmented_filepath)
        total_augmented_images += 1

    # Save metadata
    metadata = {
        "total_augmented_images": total_augmented_images,
        "images_to_augment": images_to_augment,
        "selected_augmentations": techniques,
        "augmentation_params": params
    }
    with open(os.path.join(version_folder, "metadata.json"), 'w') as f:
        json.dump(metadata, f, indent=4)

    # Clear session data
    session.pop('uploaded_files', None)
    session.pop('augmentations', None)
    session.pop('images_to_augment', None)

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
    # Check if the version parameter already includes "version_"
    if not version.startswith("version_"):
        version = f"version_{version}"

    version_folder = os.path.join(app.config['AUGMENTED_FOLDER'], version)
    zip_filename = f"augmented_images_{version.split('_')[-1]}.zip"

    # Create an in-memory ZIP file
    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(version_folder):
            for file in files:
                if file.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, version_folder))
        # Add metadata.json
        metadata_path = os.path.join(version_folder, "metadata.json")
        if os.path.exists(metadata_path):  # Ensure metadata exists
            zipf.write(metadata_path, os.path.relpath(metadata_path, version_folder))
        else:
            return f"Metadata file not found in {version_folder}", 404

    memory_file.seek(0)

    return send_file(memory_file, download_name=zip_filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)

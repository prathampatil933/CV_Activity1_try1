from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import cv2
import numpy as np
import os

app = Flask(__name__)

# Set the folder where uploaded images will be stored
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], 'input.jpg')
        file.save(filename)

        # Process the uploaded image using your existing code
        image = cv2.imread(filename, 0)

        # Define transformation parameters
        translation_matrix = np.float32([[1, 0, 50], [0, 1, 30]])  # Translate 50 pixels right and 30 pixels down
        rotation_angle = 45  # Rotate by 45 degrees
        scaling_factors = (2, 2)  # Scale by a factor of 2 in both x and y directions
        shearing_matrix = np.float32([[1, 0.5, 0], [0.5, 1, 0]])  # Shear in x-direction

        # Apply the transformations
        translated_image = cv2.warpAffine(image, translation_matrix, (image.shape[1], image.shape[0]))
        rotated_image = cv2.warpAffine(image, cv2.getRotationMatrix2D((image.shape[1] / 2, image.shape[0] / 2), rotation_angle, 1), (image.shape[1], image.shape[0]))
        scaled_image = cv2.resize(image, None, fx=scaling_factors[0], fy=scaling_factors[1])
        sheared_image = cv2.warpAffine(image, shearing_matrix, (image.shape[1], image.shape[0]))

        # Save the transformed images
        cv2.imwrite('translated_image.jpg', translated_image)
        cv2.imwrite('rotated_image.jpg', rotated_image)
        cv2.imwrite('scaled_image.jpg', scaled_image)
        cv2.imwrite('sheared_image.jpg', sheared_image)

        return render_template('result.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)

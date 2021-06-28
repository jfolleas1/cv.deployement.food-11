import os
import cv2

import numpy as np
from PIL import Image
import tensorflow as tf

from werkzeug.utils import  secure_filename
from flask import Flask, request, redirect, render_template

import config 
from api_responces import get_error_responce, ErrorType,\
    get_classification_responce

# Create app and indicate the folder where the images will be stored
app = Flask(__name__, static_url_path='/static')

app.config["IMAGE_UPLOADS"] = config.LOCAL_SAVE_IM_PATH
app.config["ALLOWED_IMAGE_EXTENSIONS"] = config.ALLOWED_EXTENTIONS

# Load the model from the folder deep learning model
food_prediction_model = tf.keras.models.load_model('./deeplearning_model')


def allowed_image(filename):
    """
    Verify if the image that you want to upload is allowed or not based on its
    extention.

    Params:
        - filename {str} : The name of the file you want to upload.

    Return:
        - {bool}: True if the extention is accepted, False otherwise.
    """
    # If there is no '.' in the filename, we can't find the extention and 
    # therfore we return False as default value.
    if not "." in filename:
        return False
    # Extract the extention from the filename.
    ext = filename.rsplit(".", 1)[1]  
    # Check if the extention is among the accepted ones.
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

if not config.API_CALL_ONLY:

    @app.route("/", methods=["GET", "POST"])
    def upload_image() :
        """
        View to upload an image with interface.
        """
        if request.method == "POST":
            # If we recieve a POST request we check that it contains files
            if request.files:
                # We extract the 'image' field from the POST request
                image = request.files["image"]
                # If the 'image' field if empy we redirect to the uploading
                # page.
                if image.filename == "":
                    return redirect(request.url)
                # We check the the image is valide
                if allowed_image(image.filename):
                    # Extract the filename and check that it can be use in a 
                    # file system.
                    filename = secure_filename(image.filename)
                    if config.LOCAL_SAVE_IM_PATH:
                        # Save the uploaded image localy
                        image.save(os.path.join(app.config["IMAGE_UPLOADS"],
                            filename))
                    elif config.GS_SAVE_IM_PATH:
                        # TODO
                        pass
                    # Redirect to the page to display the image
                    return redirect(f'/showing-image/{filename}')
                # If the image is not valide
                else:
                    # Redirect to the upload page, to ask for a new image.
                    return redirect(request.url)
        # if the request is a GET or doesn't contains any files, redirect to the 
        # uploading page.
        return render_template("upload_images.html")

    @app.route("/showing-image/<image_name>", methods=["GET", "POST"])
    def showing_image(image_name):
        """
        Display the uploaded image and allow to get the model prediction.
        """
        # If the request is a POST request trigered by the predict button 
        if request.method == 'POST':
            # We load the image given in parameters
            image_path = os.path.join(app.config["IMAGE_UPLOADS"], image_name)
            image = cv2.imread(image_path) #BGR
            img = image.copy()
            # We put the color encoding in the right order
            image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # We resize the image
            image = cv2.resize(image, config.IM_RESIZE_DIMENSION)
            # We scale the pixel values between 0 and 1.
            image = image.astype("float32")
            image = image / 255.0
            # We extend the dimension to create a batch of one image, as
            # expected by the model
            np_image = np.expand_dims(image, axis=0)
            # We run the model to get the probabilitic predictions
            predictions = food_prediction_model(np_image)
            # We get the index of the highest proability
            predicted_class_idx = np.argmax(predictions)
            # We get the highest probability
            probability = np.max(predictions)
            # We get the class name of the highest probability
            predicted_class = config.MODEL_OUTPUT_CLASSES[predicted_class_idx]
            # Return the page to visualise the results
            return render_template("prediction_result.html",
                image_name=image_name, predicted_class=predicted_class,
                probability=probability)
        # If the request is GET, we just display the image
        return render_template("showing_image.html", value=image_name)

@app.route("/api-call", methods=["POST"])
def get_prediction_from_api_call(image_name):
    """
    Return the prediction of the model via a simple API call.
    """
    # If we recieve a POST request we check that it contains files
    if request.files:
        # We extract the 'image' field from the POST request
        upload_image = request.files["image"]
        # If the 'image' field if empy we redirect to the uploading
        # page.
        if upload_image.filename == "":
            return get_error_responce(ErrorType.wrong_file_received)
        # We check the the image is valide
        if allowed_image(upload_image.filename):
            # Extract the filename and check that it can be use in a 
            # file system.
            filename = secure_filename(upload_image.filename)
            if config.LOCAL_SAVE_IM_PATH:
                # Save the uploaded image localy
                upload_image.save(os.path.join(app.config["IMAGE_UPLOADS"],
                    filename))
            elif config.GS_SAVE_IM_PATH:
                # Save the uploaded file in Google Storage
                # TODO
                pass
        else:
            return get_error_responce(ErrorType.wrong_file_received)
        # We load the image given in parameters
        np_image = np.array(Image.open(upload_image))
        # We resize the image
        np_image = cv2.resize(np_image, config.IM_RESIZE_DIMENSION)
        # We scale the pixel values between 0 and 1.
        np_image = np_image.astype("float32")
        np_image = np_image / 255.0
        # We extend the dimension to create a batch of one image, as expected 
        # by the model
        np_image = np.expand_dims(np_image, axis=0)
        # We run the model to get the probabilitic predictions
        predictions = food_prediction_model(np_image)
        # We get the api reponse based on model prediction and return it.
        return get_classification_responce(predictions)
    else:
        return get_error_responce(ErrorType.wrong_file_received)


if __name__ == '__main__':
    # Start the flask app.
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))



    



import config
import numpy as np

class ErrorType:
    wrong_file_received = 1

def get_error_responce(error_type):
    if error_type == ErrorType.wrong_file_received:
        return {"status": "ERROR",
                "message": "Field 'image' must be filled by a file " +\
                        f" on type {config.ALLOWED_EXTENTIONS}"}

def get_classification_responce(predictions):
    predicted_class_idx = np.argmax(predictions)
    # We get the highest probability
    probability = np.max(predictions)
    # We get the class name of the highest probability
    predicted_class = config.MODEL_OUTPUT_CLASSES[predicted_class_idx]
    return {"status": "OK",
            "data": {
                "predicted_class": predicted_class,
                "predicted_class_probability": probability,
                "raw_predictions": dict(zip(config.MODEL_OUTPUT_CLASSES,
                        list(predictions)))
            }}
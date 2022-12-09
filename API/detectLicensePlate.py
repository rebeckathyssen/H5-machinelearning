from itertools import count
import cv2
from google.cloud.aiplatform.gapic.schema import predict
from google.cloud import aiplatform
import base64
import os
from dotenv import load_dotenv

load_dotenv()


def predict_license_plate(
    project: str,
    endpoint_id: str,
    filename: str,
    location: str = "us-central1",
    api_endpoint: str = "us-central1-aiplatform.googleapis.com",
):
    # The AI Platform services require regional API endpoints.
    client_options = {"api_endpoint": api_endpoint}
    # Initialize client that will be used to create and send requests.
    # This client only needs to be created once, and can be reused for multiple requests.
    client = aiplatform.gapic.PredictionServiceClient(
        client_options=client_options)
    with open(filename, "rb") as f:
        file_content = f.read()

    # The format of each instance should conform to the deployed model's prediction input schema.
    encoded_content = base64.b64encode(file_content).decode("utf-8")
    instance = predict.instance.ImageObjectDetectionPredictionInstance(
        content=encoded_content,
    ).to_value()
    instances = [instance]
    # See gs://google-cloud-aiplatform/schema/predict/params/image_object_detection_1.0.0.yaml for the format of the parameters.
    parameters = predict.params.ImageObjectDetectionPredictionParams(
        confidence_threshold=0.5, max_predictions=5,
    ).to_value()
    endpoint = client.endpoint_path(
        project=project, location=location, endpoint=endpoint_id
    )
    response = client.predict(
        endpoint=endpoint, instances=instances, parameters=parameters
    )
    # print("response")
    # print(" deployed_model_id:", response.deployed_model_id)
    # See gs://google-cloud-aiplatform/schema/predict/prediction/image_object_detection_1.0.0.yaml for the format of the predictions.
    predictions = response.predictions
    # for prediction in predictions:
    #     print(" prediction:", dict(prediction))
    return predictions


def detect_license_plate(path, suffix):
    from cropImage import crop_image

    predicts = predict_license_plate(
        project="172246408209",
        endpoint_id="7251085671136231424",
        location="europe-west4",
        filename=path,
        api_endpoint="europe-west4-aiplatform.googleapis.com",
    )

    # look in the first prediction - is there a bounding box?
    if predicts[0]["bboxes"].__len__() > 0:
        return crop_image(path=path, x1=predicts[0]["bboxes"][0][0], y1=predicts[0]["bboxes"][0][2], x2=predicts[0]["bboxes"][0][1], y2=predicts[0]["bboxes"][0][3], name="Cropped_license_plate", suffix=suffix)
    # bboxes holds the new coordinates to the license plate, which will be sent to crop_image again
    return None

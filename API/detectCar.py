from cropImage import crop_image
import os
from dotenv import load_dotenv
load_dotenv()


def crop_cars(path):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """

    from google.cloud import vision_v1p3beta1 as vision
    client = vision.ImageAnnotatorClient()

    # Read the incoming image
    with open(path, 'rb') as image_file:
        content = image_file.read()  # content in bytes
    # sdk to create the picture google wants
    image = vision.Image(content=content)

    objects = client.object_localization(
        image=image).localized_object_annotations  # sends the final picture to the google client

    count = 1
    paths = []

    for object_ in objects:
        # skip object if it is not a Car in object.name
        if "Car" not in object_.name:
            continue

        cords = []
        for vertex in object_.bounding_poly.normalized_vertices:
            # save the coords where a car has been found
            cords.append((vertex.x, vertex.y))

        paths.append(crop_image(path=path, x1=cords[0][0], x2=cords[1][0],
                     y1=cords[0][1], y2=cords[2][1], name="Cropped_car", suffix=count))

        count += 1

    return paths  # the paths to the new cropped car images

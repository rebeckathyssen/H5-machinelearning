from fastapi import FastAPI, File, UploadFile
import aiofiles
from detectText import detect_text
from detectCar import crop_cars
from detectLicensePlate import detect_license_plate


app = FastAPI()


@app.post("/upload")
async def create_upload_image(image: UploadFile = File(...)):
    # Set the destination for the incoming image
    destination_file_path = "temp/" + image.filename
    # Read the incoming image
    async with aiofiles.open(destination_file_path, 'wb') as out_file:
        while content := await image.read(1024):
            await out_file.write(content)

    # Send the image above to the crop_cars method
    # Returns the cropped cars as a 'path'
    crop_cars_paths = crop_cars(destination_file_path)

    license_plates = []
    count = 1
    for path in crop_cars_paths:
        license_plate = detect_license_plate(path, count)
        count += 1
        if license_plate is not None:
            license_plates.append(license_plate)

    texts = []
    for license_plate in license_plates:
        text = detect_text(license_plate)
        if text is not None:
            texts.append(text)

    return {"license-plates": texts}

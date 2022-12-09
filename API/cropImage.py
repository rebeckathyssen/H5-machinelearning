def crop_image(path, x1, x2, y1, y2, name, suffix):
    # Create a cropped car image from above coords, name and number
    import cv2

    img = cv2.imread(path)

    height, width, channels = img.shape

    crop = img[int(y1*height):int(y2*height),
               int(x1*width):int(x2*width)]

    pathstring = "temp/" + name + str(suffix) + ".jpg"

    cv2.imwrite(pathstring, crop)  # save the new cropped image

    return pathstring  # the new cropped image

import os
import time
import argparse
from PIL import Image, ImageDraw

from google.cloud import vision
from google.oauth2 import service_account

def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Serach for any objects in the picture by google object detection."
    )
    parser.add_argument(
        "--image-path", "-p",
        help="full path of the image",
        required=True
    )
    parser.add_argument(
        "--behavior", "-b",
        help="should the output be cropped images or just draw a box around each object",
        default="polygon",
        choices=["polygon", "crop"]
    )
    parser.add_argument(
        "--border-width", "-w",
        help="border width around the objects",
        default=4,
        type=int
    )
    parser.add_argument(
        "--border-color", "-c",
        help="border color around the objects",
        default="red",
        choices=["red", "green", "gray", "black", "white"]
    )
    return parser.parse_args()

def get_google_client() -> vision.ImageAnnotatorClient:
    credentials = service_account.Credentials.from_service_account_file(
        os.environ.get("GCP_KEYFILE_JSON"),
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    return vision.ImageAnnotatorClient(credentials=credentials)

def localize_objects(path: str, client: vision.ImageAnnotatorClient):
    with open(path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    start = time.time()
    objects = client.object_localization(image=image).localized_object_annotations
    print(f"The script took {time.time() - start} seconds!")
    print(f"Number of objects found: {len(objects)}")
    return objects

def prepare_output(path: str, objects, save=True, border_width=4, border_color="red"):  
    image_data = Image.open(path)
    img_result = ImageDraw.Draw(image_data)   
    width, height = image_data.size
    for index, object_ in enumerate(objects):
        data = {"name": object_.name, "score": object_.score, "box": []}
        for vertex in object_.bounding_poly.normalized_vertices:
            data["box"].append({"X": vertex.x * width, "Y": vertex.y * height})
        bbox = [data["box"][0]["X"], data["box"][0]["Y"], data["box"][2]["X"], data["box"][2]["Y"]]
        if save:
            img_result.rectangle(bbox, outline=border_color, width=border_width)
        else:
            croped_image = image_data.crop(bbox)
            croped_image.save(path.split("/")[-1].replace(".jpg", f"_N{index}_C{int(object_.score * 100)}.jpg"))
    if save:
        image_data.save(path.split("/")[-1])

if __name__ == "__main__":
    args = get_args()
    google_client = get_google_client()
    image_objects = localize_objects(args.image_path, google_client)
    prepare_output(args.image_path,
                   image_objects,
                   border_color=args.border_color,
                   border_width=args.border_width,
                   save=True if args.behavior == "polygon" else False
                   )

## Install dependencies  
Install dependencies with `pip install -r requirements.txt`  

**N.B** Make sure you have added google credential as environment variable `GCP_KEYFILE_JSON=path`

```shell
usage: main.py [-h] --image-path IMAGE_PATH [--behavior {polygon,crop}] [--border-width BORDER_WIDTH] [--border-color {red,green,gray,black,white}]

Serach for any objects in the picture by google object detection.

optional arguments:
  -h, --help            show this help message and exit
  --image-path IMAGE_PATH, -p IMAGE_PATH
                        full path of the image
  --behavior {polygon,crop}, -b {polygon,crop}
                        should the output be cropped images or just draw a box around each object
  --border-width BORDER_WIDTH, -w BORDER_WIDTH
                        border width around the objects
  --border-color {red,green,gray,black,white}, -c {red,green,gray,black,white}
                        border color around the objects
```

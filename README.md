# pdf-creator
Creates PDF from image files in a directory.

## Requirements

Pillow and OpenCV were used, which can be installed using the 'requirements.txt' file.

```bash
pip install -r requirements.txt
```

## Usage

Copy your image files into the "input_files" directory and run main.py to generate a PDF file, which will be saved in a folder named "output_files". (python=3.8 was used)

```bash
python main.py
```

By default, the program fits each image in an A4 sized page. If original resolutions and image sizes are to be maintained, pass the "--original_sizes" argument.

```bash
python main.py --original_sizes
```

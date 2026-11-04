# ColorCat

Personal toolkit for producing LINE emoji sets: fill line art with colors,
reorder the set, and export files named the way LINE expects (`001.png`, `002.png`, ...).

## Setup

```bash
pip install -r requirements.txt
```

## Workflow

1. Put line art (RGBA PNGs) in `linearts/`.
2. Color them with the pipeline -> `outputs/`.
3. Open the reorder tool, arrange the emoji, and save to a new folder as `001.png` ... `040.png`.

## Usage

### Full Pipeline
```bash
python run_pipeline.py colors.txt linearts/ outputs/
```

Configure colors in `colors.txt`:
```
background: #00ff00
line: #030403
fill: #ffffff
```

### Image Reorder Tool
GUI (PySide6) for arranging the emoji order before export:
```bash
python image_reorder_app.py
```
- Auto-loads `linearts/` if it exists; otherwise use the load button to pick a folder.
- Drag and drop thumbnails to reorder.
- **Background** buttons (Gray / Red / Blue) switch the thumbnail background to check
  how the art looks on different colors.
- Thumbnails at position 41 and beyond are dimmed: a LINE emoji set holds at most 40.
- Save copies the images to an output folder renamed to `001.png`, `002.png`, ...
  (originals are untouched).

## Individual Scripts

### Find Fill Areas
Generate masks for fillable regions from RGBA line art:
```bash
python find_fill_area.py input.png output_mask.png [--preview] [--shrink=N]
```
- `--preview`: Output colored preview instead of black/white mask
- `--shrink=N`: Erode mask by N pixels to avoid bleeding

### Composite Images
Combine line art with colored fill using a mask:
```bash
python composite.py lineart.png mask.png output.png [#RRGGBB]
```
- Color format: hex color like `#ff00ff` (default: magenta)

### Parse Colors
Extract color palette from reference images:
```bash
python parse_colors.py image.png
```

### Rename to 3-Digit Filenames
Rename every PNG in a folder using the first number in its name:
```bash
python rename_to_digits.py [folder]
```
- Example: `image_00034_out.png` -> `034.png`
- Defaults to the current directory; skips files whose target name already exists.

## Notes

- `archive/` holds past emoji sets and is git-ignored (images are never committed).

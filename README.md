# ColorCat

Image coloring pipeline that fills line art with specified colors.

## Setup

```bash
pip install -r requirements.txt
```

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

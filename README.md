# ColorCat

Image coloring pipeline that fills line art with specified colors.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
python run_pipeline.py colors.txt linearts/ outputs/
```

Configure colors in `colors.txt`:
```
background: #00ff00
line: #030403
fill: #ffffff
```
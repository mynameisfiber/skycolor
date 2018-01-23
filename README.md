# Sky Color

Want to know the color of the sky in RGB? Here you go.

## Installation

1. Install virtualenv: `virtualenv -p python3.6 venv`
2. Activate virtualenv: `source ./venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `python skycolor.py`


## Endpoints

- `/color/<preset>`: Get the sky color for a preset
- `/color/<x0,x1>/<y0,y1>?webcam=<url>`: Get the sky color for given coordinate
  range for a certain webcam url (link directly to a screenshot)
- `/debug/<preset>`: Get the debug image for a preset
- `/debug/<x0,x1>/<y0,y1>?webcam=<url>`: Get the debug image for a given
  coordinate range for a certain webcam url (link directly to a screenshot)
- `/presets`: List preset values

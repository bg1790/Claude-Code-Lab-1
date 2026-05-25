# Claude-Code-Lab-1

Python CLI app that:
- collects industry and number of professionals with a PhD
- collects volunteer names and art activities (`puzzles`, `drawing`, `music`, `bookreading`)
- generates an SVG graph with X axis = volunteer name and Y axis = art activity

## Run

```bash
cd <repository-root>
python app.py
```

The graph is saved as `volunteer_activity_graph.svg` in the current directory.

## Test

```bash
cd <repository-root>
python -m unittest discover -s tests -v
```

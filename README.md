# simplePOS

This is a simple POS coded by Codex.

## Setup

The application uses an SQLite database stored in `pos.db`.

## Running the POS

```
python pos.py
```

A small menu-driven interface lets you add products, list products, record sales, and view sales.

## Testing

Install pytest if needed and run:

```
pytest
```

## Deployment with Docker

Build an image and run the POS inside a container:

```
docker build -t simplepos .
docker run -it --rm -v $(pwd)/pos.db:/app/pos.db simplepos
```

The volume mount keeps `pos.db` on the host so data persists between runs.

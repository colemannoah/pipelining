
# Pipelining

A lightweight, object-orientated pipeline framework in Python, with Rich-powered logging, and abstract semantics.

## Features

- **Modular Stages**: Each processing step can be defined by subclassing the simple `Stage` interface.
- **Pipeline Orchestration**: Stages can be composed into ordered pipelines with automatic logging injection.
- **Pretty Logging**: Good looking logging, powered by [Rich](https://rich.readthedocs.io/en/stable/logging.html)

## Installation

This package is built for **Python 3.13**, as that is the version I use the most. I am happy to extend it for other versions.

Install `pipelining-colemann` through [PyPi](https://pypi.org/project/pipelining-colemann/) with:

```bash
$ pip install pipelining-colemann
...
```

## Example

```python
class TextStage(Stage):
    def __init__(self, name: str, message: str) -> None:
        super().__init__(name)
        self.message = message

    def run(self, context: dict[str, Any]) -> None:
        self.logger.info(f"{self.name}: {self.message}")


pipeline = Pipeline(
    [TextStage("Stage 1", "Hello, World!"), TextStage("Stage 2", "Goodbye, World!")],
    name="Example Pipeline",
)

pipeline.run()
```

A simple example like this will output:

```text
[2025-05-07 17:52:18] INFO     Starting Example Pipeline                                                                                                                           
                      INFO     Running stage: TextStage                                                                                                                            
                      INFO     Stage 1: Hello, World!                                                                                                                              
                      INFO     Stage TextStage completed successfully!                                                                                                             
                      INFO     Running stage: TextStage                                                                                                                            
                      INFO     Stage 2: Goodbye, World!                                                                                                                            
                      INFO     Stage TextStage completed successfully!                                                                                                             
                      INFO     Example Pipeline completed successfully!                                                                                                            
```

## Development

To setup a Python environment for this project, I recommend using Pixi - I use it and like it. You can enter the workspace using:

```bash
$ pixi shell
...
```

The following self-explanatory tasks are available for usage.

- `ruff`
- `mypy`
- `test`
- `coverage`

## Testing

Tests can be run through [Pixi](https://pixi.sh/latest/) with:

```bash
$ pixi run test
...
```

They can be run with coverage too, this will generate a coverage report under the `htmlcov` directory.

```bash
$ pixi run coverage
...
```

## Contributing

Feel free to contribute to the project! I would appreciate any feedback or comments. Although this project has been built with my own usage in mind, I'm open to changes and improvements.

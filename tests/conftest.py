"""Conftest.py contains fixtures and helper classes for testing the pipelining library.

This module provides dummy stages that can be used in tests to verify the execution flow
of the pipeline without implementing actual processing logic.
"""

from collections.abc import Callable
from typing import Any

from pipelining.core.stage import Stage


class DummyStage(Stage):
    """A dummy stage for testing purposes.

    This stage does not perform any actual processing but serves as a
    placeholder in the pipeline. It can be used to test the pipeline's
    execution flow without implementing real logic.

    Parameters
    ----------
    name : str
        The name of the stage.

    """

    def __init__(self, name: str, action: Callable) -> None:
        """DummyStage constructor.

        Parameters
        ----------
        name : str
            The name of the stage.
        action : Callable
            A callable that takes the context as an argument and performs some action.

        """
        super().__init__(name)
        self.name = name
        self.action = action

    def run(self, context: dict[str, Any]) -> None:
        """Run the dummy stage.

        Parameters
        ----------
        context : dict[str, Any]
            The context dictionary that is passed through the pipeline.

        """
        context.setdefault("order", []).append(self.name)

        if callable(self.action):
            self.action(context)


class LogStage(Stage):
    """A logging stage for testing purposes.

    This stage does not perform any actual processing but serves as a
    placeholder in the pipeline. It can be used to test the pipeline's
    execution flow without implementing real logic.

    Parameters
    ----------
    name : str
        The name of the stage.

    """

    def __init__(self, name: str, message: str) -> None:
        """LogStage constructor.

        Parameters
        ----------
        name : str
            The name of the stage.
        message : str
            The message to log when the stage is run.

        """
        super().__init__(name)
        self.name = name
        self.message = message

    def run(self, _: dict) -> None:
        self.logger.info(self.message)

from collections.abc import Callable, Iterable
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

from pipelining.core.stage import Stage


class MultiStepStage(Stage):
    """A stage with multiple steps.

    Parameters
    ----------
    name : str
        A name for the stage.
    steps : Iterable[Callable]
        An iterable containing callables to be run throughout the stage
    parallel : bool, optional
        If True, the steps will be run in parallel. Default is False.
    max_workers : int, optional
        The maximum number of workers to use for parallel execution. Default is 4.

    Attributes
    ----------
    logger : logging.Logger
        Logger instance for this stage, injected by the Pipeline.
    steps : list[Callable]
        List of callables to be executed in this stage.
    parallel : bool
        If True, the steps will be run in parallel.
    max_workers : int
        The maximum number of workers to use for parallel execution.

    """

    def __init__(
        self,
        name: str,
        steps: Iterable[Callable],
        *,
        parallel: bool = False,
        max_workers: int = 4,
    ) -> None:
        """Create a MultiStepStage.

        Parameters
        ----------
        name : str
            A name for the stage.
        steps : Iterable[Callable]
            An iterable containing callables to be run throughout the stage
        parallel : bool, optional
            If True, the steps will be run in parallel. Default is False.
        max_workers : int, optional
            The maximum number of workers to use for parallel execution. Default is 4.

        """
        super().__init__(name)
        self.steps: list[Callable] = list(steps)
        self.parallel = parallel
        self.max_workers = max_workers

    def run(self, context: dict[str, Any]) -> None:
        """Run the steps for this stage.

        Context will be passed to each step, allowing them to share data.
        Each step is expected to be a callable that at least takes a single
        argument, which is the context dictionary.

        Parameters
        ----------
        context : dict
            Shared context dictionary that carries data between stages.

        Raises
        ------
        Exception
            Any exception raised here will be caught and re-raised by the Pipeline
            after logging.

        """
        if self.parallel:
            self.logger.info(
                f"Running {self.name} in parallel mode with {len(self.steps)} step(s).",
            )

            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {executor.submit(step, context): step for step in self.steps}

                for future in as_completed(futures):
                    step = futures[future]

                    try:
                        future.result()
                    except Exception:
                        self.logger.exception(f"Error in step {step.__name__}")
                        raise

                    self.logger.info(
                        f"\tStep '{step.__name__}' completed successfully!",
                    )
        else:
            sequential_log_message = (
                f"Running {self.name} in sequential mode with "
                f"{len(self.steps)} step(s)."
            )
            self.logger.info(sequential_log_message)

            for step in self.steps:
                self.logger.info(f"\tRunning step: {step.__name__}")

                try:
                    step(context)
                except Exception:
                    self.logger.exception(f"Error in step {step.__name__}")
                    raise

                self.logger.info(f"\tStep '{step.__name__}' completed successfully!")

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable, Iterable
from pipelining.core.stage import Stage


class MultiStepStage(Stage):
    """
    A stage with multiple steps.

    Parameters
    ----------
    name : str
        A name for the stage.
    steps : Iterable[Callable]
        An iterable containing callables to be run throughout the stage
    parallel : bool, optional
        If True, the steps will be run in parallel. Default is False.

    Attributes
    ----------
    logger : logging.Logger
        Logger instance for this stage, injected by the Pipeline.
    """

    def __init__(
        self, name: str, steps: Iterable[Callable], parallel: bool = False
    ) -> None:
        super().__init__(name)
        self.steps: list[Callable] = list(steps)
        self.parallel = parallel

    def run(self, context: dict[str, Any]) -> None:
        """
        Run the steps for this stage.

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
                f"Running {self.name} in parallel mode with {len(self.steps)} step(s)."
            )

            with ThreadPoolExecutor() as executor:
                futures = {executor.submit(step, context): step for step in self.steps}

                for future in as_completed(futures):
                    self.logger.info(f"\tRunning step: {futures[future].__name__}")
                    step = futures[future]

                    try:
                        future.result()
                    except Exception as e:
                        self.logger.error(f"Error in step {step.__name__}: {e}")
                        raise

                    self.logger.info(
                        f"\tStep '{step.__name__}' completed successfully!"
                    )
        else:
            self.logger.info(
                f"Running {self.name} in sequential mode with {len(self.steps)} step(s)."
            )

            for step in self.steps:
                self.logger.info(f"\tRunning step: {step.__name__}")

                try:
                    step(context)
                except Exception as e:
                    self.logger.error(f"Error in step {step.__name__}: {e}")
                    raise

                self.logger.info(f"\tStep '{step.__name__}' completed successfully!")

from threading import Lock
from threading import Thread
import time


class WorkerPool:
    """Manages pool of synchronized workers."""

    def __init__(self, worker, tasks, min_interval, context, max_workers):
        """Create new WorkerPool.
        Args:
            worker (function): func which will be used inside of
                _SynchronizedWorker.
            tasks (Queue): queue of tasks.
            min_interval (float): Minimal interval between task executions in
                seconds.
            context (object): Context object shared across all workers in pool.
            max_workers (int): Maximal number of workers.
        """
        self.workers = []
        self.tasks = tasks
        self.context = context
        self.max_workers = max_workers
        self.clock = _SharedValue(0)
        self.lock = Lock()
        for i in range(max_workers):
            new_worker = _SynchronizedWorker(
                worker, tasks, min_interval, self.lock, self.clock,
                context=context)
            self.workers.append(new_worker)

    def start(self):
        """Start all workers."""
        for worker in self.workers:
            worker.start()

    def wait_until_done(self):
        """Wait until all tasks done and workers are joined."""
        self.tasks.join()
        for worker in self.workers:
            worker.join()


class _SynchronizedWorker(Thread):
    """Runs target function (worker) over tasks queue until it ends.
    Each execution of a target function can start running no earlier than
    `min_interval` from previous execution.
    """

    def __init__(
            self, worker, tasks, min_interval, lock, clock, context=None,
            **kwargs):
        """Create new _SynchronizedWorker.
        Args:
            worker (function): target function.
            tasks (Queue): queue of tasks.
            min_interval (float): Minimal interval between task executions in
                seconds.
            lock (Lock): Lock used for synchronizing workers.
            clock (_SharedValue): Time of last worker execution (from epoch).
            context (object): Context object shared across all workers in pool.
        """
        self.tasks = tasks
        self.min_interval = min_interval
        self.lock = lock
        self.clock = clock
        kwargs['target'] = self._patch(worker)
        if context is not None:
            kwargs['args'] = (context, )
        super().__init__(daemon=True, **kwargs)

    def _patch(self, target):
        """For updating Thread target function.
        Args:
            target (function): Thread target.
        """
        def wrapper(*args, **kwargs):
            while not self.tasks.empty():
                task = self.tasks.get()

                with self.lock:
                    interval = time.time() - self.clock.value
                    time.sleep(max(0, self.min_interval - interval))
                    self.clock.value = time.time()

                new_task = target(task, *args, **kwargs)

                self.tasks.task_done()
                if new_task:
                    self.tasks.put(new_task)
        return wrapper


class _SharedValue:
    """Class that contains single value."""

    def __init__(self, value):
        """Create new SharedValue.
        Args:
            value (any): Any value.
        """
        self.value = value

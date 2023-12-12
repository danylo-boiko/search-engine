from os.path import exists
from pickle import dump, load
from queue import Queue, Empty

from crawler.utils import extract_domain


class SerializableQueue(Queue):
    def __init__(self, head: str | None, queue_prefix: str | None) -> None:
        super().__init__()

        self.queue_prefix = extract_domain(head) if head else queue_prefix
        self.__preload_from_file()

        if head:
            self.queue.insert(0, head)

        if not self.qsize():
            raise ValueError("Queue is empty")

    def head(self) -> str | None:
        if not self.qsize():
            return None

        with self.mutex:
            return self.queue[0]

    def get(self, block: bool = True, timeout: float = None) -> str | None:
        try:
            return super().get(block, timeout)
        except Empty:
            return None

    def save_to_file(self) -> None:
        with open(self.__get_file_name(), "wb") as file:
            dump(self.queue, file)

    def __preload_from_file(self) -> None:
        file_name = self.__get_file_name()

        if not exists(file_name):
            return

        with open(file_name, "rb") as file:
            loaded_queue = load(file)

            if loaded_queue:
                self.queue = loaded_queue

    def __get_file_name(self) -> str:
        return f"{self.queue_prefix}_queue.pkl"

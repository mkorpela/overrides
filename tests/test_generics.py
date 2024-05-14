from typing import Callable

from overrides import override


class Thing:
    pass


class Animal(Thing):
    pass


class Dog(Animal):
    pass


class AnimalHerd:
    def feed_animals(self, feed: Callable[[Animal], None]) -> None:
        pass

    def breed_animal(self, breeder: Callable[[], Animal]) -> None:
        pass

    def transform_animal(self, transformer: Callable[[Animal], Animal]) -> None:
        pass


def test_more_specific_function_input_is_fine():
    class DogHerd(AnimalHerd):
        @override
        def feed_animals(self, feed: Callable[[Dog], None]) -> None:
            pass


def test_more_abstract_function_output_is_fine():
    class ThingsHerd(AnimalHerd):
        @override
        def breed_animal(self, breeder: Callable[[], Thing]) -> None:
            pass


def test_function_input():
    class Herd(AnimalHerd):
        @override
        def transform_animal(self, transformer: Callable[[Dog], Thing]) -> None:
            pass

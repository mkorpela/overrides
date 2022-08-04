from overrides import overrides


class Parent:
    def metoda(self) -> None:
        pass


class Child(Parent):
    @overrides
    def metoda(self) -> "Child":
        return self

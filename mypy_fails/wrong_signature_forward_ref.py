from overrides import override


class Parent:
    def metoda(self) -> None:
        pass


class Child(Parent):
    @override
    def metoda(self) -> "Child":
        return self

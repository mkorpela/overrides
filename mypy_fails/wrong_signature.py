from overrides import overrides


class Parent:
    def metodi(self, x: int) -> str:
        return f"{x}"


class Child(Parent):
    @overrides
    def metodi(self, x: str) -> int:
        return int(x)

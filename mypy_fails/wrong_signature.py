from overrides import override


class Parent:
    def metodi(self, x: int) -> str:
        return f"{x}"


class Child(Parent):
    @override
    def metodi(self, x: str) -> int:
        return int(x)

from overrides import final


class SomeClass(object):
    def somewhat_fun_method(self):
        """LULZ"""
        return "LOL"

    @final
    def somewhat_finalized_method(self):
        return "some_final"

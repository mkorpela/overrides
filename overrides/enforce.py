from abc import ABCMeta


class EnforceOverridesMeta(ABCMeta):
    def __new__(mcls, name, bases, namespace, **kwargs):
        cls = super().__new__(mcls, name, bases, namespace, **kwargs)
        for name, value in namespace.items():
            # Actually checking the direct parent should be enough,
            # otherwise the error would have emerged during the parent class checking
            if name.startswith('__'):
                continue
            is_override = getattr(value, '__override__', False)
            for base in bases:
                base_class_method = getattr(base, name, False)
                if not base_class_method:
                    continue
                assert is_override, \
                    'Method %s overrides but does not have @overrides decorator' % (name)
                # `__finalized__` is added by `@final` decorator
                assert not getattr(base_class_method, '__finalized__', False), \
                    'Method %s is finalized in %s, it cannot be overridden' % (base_class_method, base) 
        return cls

class EnforceOverrides(metaclass=EnforceOverridesMeta):
    "Use this as the parent class for your custom classes"
    pass
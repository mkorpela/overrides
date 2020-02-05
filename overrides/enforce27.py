from abc import ABCMeta


class EnforceOverridesMeta(ABCMeta):
    def __new__(mcls, name, bases, namespace, **kwargs):
        cls = super(EnforceOverridesMeta, mcls).__new__(mcls, name, bases, namespace, **kwargs)
        cls_name = name
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
                    '%s method %s overrides but does not have @overrides decorator' % (
                        cls_name, name)
                # `__finalized__` is added by `@final` decorator
                assert not getattr(base_class_method, '__finalized__', False), \
                    '%s method %s is finalized in %s, it cannot be overridden' % (
                        cls_name, base_class_method, base)
        return cls

class EnforceOverrides(object):
    "Use this as the parent class for your custom classes"
    __metaclass__ = EnforceOverridesMeta
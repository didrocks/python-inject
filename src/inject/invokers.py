'''Invoker can invoke an unbound method. If not an unbound method is passed
to it, it is returned untouched.
'''
from inject.points import InjectionPoint


class Invoker(object):
    
    '''Invoker calls an unbound method by getting its class instance from
    an injection, and passing it as self. Optional scope can be given for
    a class injection.
    
    Example::
    
        >>> class A(object):
        ...     def method(self, arg):
        ...         return 'arg: %s' % arg
        ...
        >>> invoker = Invoker(A.method)
        >>> invoker('value')
        'arg: value'
    
    When not an unbound method is passed to C{Invoker}, it is returned
    untouched. For example::
    
        >>> def func(): pass
        >>> invoker = Invoker(func)
        >>> invoker is func
        True
    
    Also C{Invoker} is a transparent wrapper around an unbound method.
    I.e. it has the same hash as the method and redirects all equality 
    requests to it.
    
        >>> class B(object):
        ...     def method(self, arg):
        ...         return arg
        ...
        >>> invoker = Invoker(B.method)
        
        >>> invoker == B.method
        True
        
        >>> d = {}
        >>> d[invoker] = 'value'
        >>> d[B.method]
        'value'
        
    '''
    
    __slots__ = ('method', 'injection', '_hash')
    
    injection_point_class = InjectionPoint
    
    def __new__(cls, method):
        '''If method is an unbound method, create an invoker and return it,
        otherwise return the untouched method.
        '''
        if hasattr(method, 'im_class') and \
           hasattr(method, 'im_self') and \
           hasattr(method, 'im_func') and \
           method.im_self is None:
            return super(Invoker, cls).__new__(cls)
        
        return method
    
    def __init__(self, method):
        self.method = method
        self.injection = self.injection_point_class(method.im_class)
        self._hash = None
    
    def __call__(self, *args, **kwargs):
        '''Invoke the unbound method, return the result.'''
        inst = self.injection.get_instance()
        return self.method(inst, *args, **kwargs)
    
    def __hash__(self):
        _hash = self._hash
        if _hash is None:
            _hash = hash(self.method)
            self._hash = _hash
        return _hash
    
    def __eq__(self, other):
        return self.method == other
    
    def __ne__(self, other):
        return self.method != other
def add_attribute(cls: type):
    setattr(cls, 'name', 1)
    return cls

class Foo:
    pass

print(Foo.__dict__)

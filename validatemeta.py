#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


class Field:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__dict__[key] = value

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner=None):
        if not instance:
            return self
        return instance.__dict__[self._name]

    def __set__(self, instance, value):
        # self.validate(value)
        instance.__dict__[self._name] = value

    def validate(self, value):
        raise NotImplementedError()


class ValidateMeta(type):
    def __new__(mcls, clsname, bases, clsdict, **kwargs):
        fields = {}
        name: str
        for name, value in clsdict.items():
            if isinstance(value, Field):
                field: Field = value
                field.__set_name__(None, name)
                fields[name] = field
                # del clsdict[name]
        clsdict["_fields"] = fields
        return super().__new__(mcls, clsname, bases, clsdict, **kwargs)


class SizedField(Field):
    def __init__(self, **kwargs):
        if "size" not in kwargs:
            raise TypeError("`size' not set")
        super().__init__(**kwargs)


class Typed(Field):
    field_type: type = type(None)

    def __set__(self, instance, value):
        if not isinstance(value, self.field_type):
            raise TypeError(f"{value}: must be of type {self.field_type}")
        super().__set__(instance, value)


class TypedMeta(type):
    def __new__(mcls, name, bases, namespace, **kwargs):
        cls = super().__new__(mcls, name, bases, namespace, **kwargs)

        # Check only subclasses of Typed (but not Typed itself)
        if any(issubclass(base, Typed) for base in bases) and cls is not Typed:
            if "field_type" not in namespace:
                raise TypeError(f"{name} must define 'field_type'")

        return cls


class Integer(Typed, metaclass=TypedMeta):
    field_type = int


class Float(Typed, metaclass=TypedMeta):
    field_type = float


class Unsigned(Field):
    def __set__(self, instance, value):
        if value < 0:
            raise ValueError(f"{value}: must be >= 0")
        super().__set__(instance, value)


class UnsignedInteger(Integer, Unsigned):
    pass


class UnsignedFloat(Float, Unsigned):
    pass


class String(Typed, metaclass=TypedMeta):
    field_type = str


class SizedString(String, SizedField):
    def __set__(self, instance, value):
        if len(value) >= self.size:
            raise ValueError(f"{value}: longer than {self.size} chars")
        super().__set__(instance, value)


class Model(metaclass=ValidateMeta):
    def as_csv(self) -> str:
        return ", ".join(f"{key}={value}" for key, value in self.__dict__.items())


class Exercise(Model):
    exercise_name = SizedString(size=12)
    weight = UnsignedFloat()
    reps = UnsignedInteger()

    def __init__(self, exercise_name, weight, reps):
        self.exercise_name = exercise_name
        self.weight = weight
        self.reps = reps


if __name__ == "__main__":
    exer = Exercise("Bench press", 108.5, 2)
    print(exer.as_csv())

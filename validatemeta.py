#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


class Field:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__dict__[key] = value

    def __get__(self, instance, owner=None):
        if not instance:
            return self
        return instance.__dict__[self._name]

    def __set__(self, instance, value):
        self.validate(value)
        instance.__dict__[self._name] = value

    def validate(self, value):
        raise NotImplementedError()


class ValidateMeta(type):
    def __new__(mcls, clsname, bases, clsdict, **kwargs):
        fields = {}
        for name, value in clsdict.items():
            if isinstance(value, Field):
                fields[name] = value
                del clsdict[name]
        clsdict["_fields"] = fields
        return super().__new__(mcls, bases, clsdict, **kwargs)


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


class Integer(Field):
    field_type = int


class Float(Field):
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


class String(Field):
    field_type = str


class SizedString(String, SizedField):
    def __set__(self, instance, value):
        if len(value) >= self.size:
            raise ValueError(f"{value}: longer than {self.size} chars")


class Model(metaclass=ValidateMeta):
    pass


class Exercise(Model):
    pass


class Exercise(Model):
    exercise_name = SizedString(12)
    weight = UnsignedFloat()
    reps = UnsignedInteger()

    def __init__(self, exer_name, weight, reps):
        self.exer_name = exer_name
        self.weight = weight
        self.reps = reps


if __name__ == "__main__":
    drill = Exercise("Bench press", 108.5, 2)

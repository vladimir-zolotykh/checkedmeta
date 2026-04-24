#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


class Field:
    def __init__(self, name, **kwargs):
        self._name = name
        for key, value in kwargs.items():
            self.__dict__[key] = value

    def __set__(self, instance, value):
        instance.__dict__[self._name] = value


def Typed(expected_type):
    def cls_deco(cls):
        super_set = cls.__set__

        def __set__(self, instance, value):
            if not isinstance(value, expected_type):
                raise TypeError()
            super_set(instance, value)

        cls.__set__ = __set__
        return cls

    return cls_deco


def Unsigned(cls):
    sset = cls.__set__

    def set(self, instance, value):
        if value < 0:
            raise (f"{value}: must be >= 0")
        sset(instance, value)

    cls.__set__ = set
    return cls


def Sized(size):
    def cls_deco(cls):
        sinit = cls.__init__

        def init(self, *args, **kwargs):
            if "size" not in kwargs:
                raise TypeError("{cls}: Specify `size'")
            sinit(*args, **kwargs)

        cls.__init__ = init
        sset = cls.__set__

        def set(self, instance, value):
            if len(value) >= self.size:
                raise ValueError(f"{value}: must not exceed {self.size} chars")
            sset(instance, value)

        cls.__set__ = set
        return cls

    return cls_deco


@Unsigned
@Typed(int)
class UnsignedInteger:
    pass


@Unsigned
@Typed(float)
class UnsignedFloat:
    pass


@Sized(12)
@Typed(str)
class SizedString:
    pass


class Exercise:
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

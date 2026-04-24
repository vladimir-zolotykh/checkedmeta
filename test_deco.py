#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import pytest

from typed_deco import (
    UnsignedInteger,
    UnsignedFloat,
    SizedString,
    Exercise,
)


# -------------------------
# Typed decorator
# -------------------------


def test_typed_accepts_correct_type():
    class A:
        x = UnsignedInteger("x")

    obj = A()
    obj.x = 10
    assert obj.x == 10


def test_typed_rejects_wrong_type():
    class A:
        x = UnsignedInteger("x")

    obj = A()
    with pytest.raises(TypeError):
        obj.x = "not int"


# -------------------------
# Unsigned decorator
# -------------------------


def test_unsigned_accepts_positive():
    class A:
        x = UnsignedInteger("x")

    obj = A()
    obj.x = 5
    assert obj.x == 5


def test_unsigned_rejects_negative():
    class A:
        x = UnsignedInteger("x")

    obj = A()

    # NOTE: your code raises a *string*, which is invalid.
    # Python will actually raise TypeError instead.
    with pytest.raises(TypeError):
        obj.x = -1


# -------------------------
# Sized decorator
# -------------------------


def test_sized_accepts_valid_length():
    class A:
        s = SizedString("s", size=5)

    obj = A()
    obj.s = "abcd"
    assert obj.s == "abcd"


def test_sized_rejects_too_long():
    class A:
        s = SizedString("s", size=5)

    obj = A()

    with pytest.raises(ValueError):
        obj.s = "abcdef"


def test_sized_requires_size_argument():
    # This should fail because size is missing
    with pytest.raises(TypeError):
        SizedString("s")


# -------------------------
# Integration: Exercise
# -------------------------


def test_exercise_valid():
    e = Exercise("Bench press", 100.0, 5)

    assert e.exercise_name == "Bench press"
    assert e.weight == 100.0
    assert e.reps == 5


def test_exercise_invalid_weight_type():
    with pytest.raises(TypeError):
        Exercise("Bench press", "heavy", 5)


def test_exercise_negative_weight():
    with pytest.raises(TypeError):
        Exercise("Bench press", -10.0, 5)


def test_exercise_invalid_reps_type():
    with pytest.raises(TypeError):
        Exercise("Bench press", 100.0, 2.5)


def test_exercise_name_too_long():
    with pytest.raises(ValueError):
        Exercise("Very very long exercise name", 100.0, 5)

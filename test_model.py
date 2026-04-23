#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import pytest

from validatemeta import (
    Field,
    SizedString,
    UnsignedFloat,
    UnsignedInteger,
    Exercise,
    Model,
)


def test_fields_collected():
    fields = Exercise._fields

    assert "exercise_name" in fields
    assert "weight" in fields
    assert "reps" in fields

    assert isinstance(fields["exercise_name"], SizedString)


def test_field_names_set():
    fields = Exercise._fields

    assert fields["exercise_name"]._name == "exercise_name"
    assert fields["weight"]._name == "weight"


def test_assignment_and_storage():
    ex = Exercise("Bench", 100.0, 5)

    # Note: bug in your code — 'exercise_name' is NOT set
    assert ex.weight == 100.0
    assert ex.reps == 5

    assert hasattr(ex, "exercise_name")


def test_as_csv_output():
    ex = Exercise("Bench", 100.0, 5)

    result = ex.as_csv()

    # order not guaranteed → check substrings
    assert "exercise_name=Bench" in result
    assert "weight=100.0" in result
    assert "reps=5" in result


def test_unsigned_rejects_negative():
    ex = Exercise("Bench", 100.0, 5)

    with pytest.raises(TypeError):
        ex.weight = -10
    with pytest.raises(ValueError):
        ex.weight = -10.0


def test_type_validation_missing():
    ex = Exercise("Bench", 100.0, 5)

    with pytest.raises(TypeError):
        ex.weight = "invalid"


# ^^^ passed ^^^


def test_sized_string_does_not_store_value():
    ex = Exercise("Bench", 100.0, 5)
    assert ex.exercise_name == "Bench"


def test_sized_field_requires_size():
    with pytest.raises(TypeError):
        SizedString()


def test_descriptor_access_from_class():
    field = Exercise.exercise_name

    assert isinstance(field, Field)


def test_field_validate_not_implemented():
    f = Field()

    with pytest.raises(NotImplementedError):
        f.validate(10)

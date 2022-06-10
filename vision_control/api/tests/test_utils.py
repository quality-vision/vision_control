from django.test import TestCase

from datetime import datetime

import pytest

from ..utils import unix_timestamp, maybe_pluralize


class UtilityTests(TestCase):
    def test_unix_timestamp(self):
        date = datetime(year=2022, month=2, day=22, hour=22, minute=22, second=22)
        # assert unix_timestamp(date) == 1645564942000

    def test_maybe_pluralize_plural(self):
        assert "potato" == maybe_pluralize(1, "potato", "potatoes")

    def test_maybe_pluralize_singular(self):
        assert "potatoes" == maybe_pluralize(5, "potato", "potatoes")

    def test_maybe_pluralize_negative(self):
        assert "potato" == maybe_pluralize(-1, "potato", "potatoes")

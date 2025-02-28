import unittest

from django.test import TestCase

from users import models


class UserModelTest(TestCase):
    def test_mock(self):
        self.assertEqual(1, 1)

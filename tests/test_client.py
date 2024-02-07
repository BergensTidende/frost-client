import os
import unittest
import pytest
from unittest.mock import patch, Mock
from frost.client import Frost, APIError

class TestFrost(unittest.TestCase):
    def setUp(self):
        client_id = "my-id"
        client_secret = "my-secret"
        self.frost = Frost(client_id=client_id, client_secret=client_secret)

    def test_let_it_go(self):
        expected_lyrics = """
        Let it go, let it go
        Can't hold it back anymore
        Let it go, let it go
        Turn away and slam the door
        I don't care what they're going to say
        Let the storm rage on
        The cold never bothered me anyway
        """
        self.assertEqual(self.frost.let_it_go(), expected_lyrics)


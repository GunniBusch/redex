#!/usr/bin/env python3

import argparse
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import redex


class TestValidateArgs(unittest.TestCase):
    def test_autodetects_redex_binary_during_validation(self) -> None:
        args = argparse.Namespace(
            sign=False,
            unpack_only=False,
            redex_binary=None,
            config="config.json",
        )

        with mock.patch.object(redex.shutil, "which", return_value="/tmp/redex-all"):
            with mock.patch.object(redex, "isfile", return_value=True):
                with mock.patch.object(redex.os, "access", return_value=True):
                    redex.validate_args(args)

        self.assertEqual(args.redex_binary, "/tmp/redex-all")

    def test_find_redex_binary_returns_none_when_not_found(self) -> None:
        with mock.patch.object(redex.shutil, "which", return_value=None):
            with mock.patch.object(redex, "isfile", return_value=False):
                self.assertIsNone(redex.find_redex_binary(None))


if __name__ == "__main__":
    unittest.main()

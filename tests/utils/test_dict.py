from unittest import TestCase

from gluepy.utils.dict import merge


class DictTestCase(TestCase):
    def test_merge_dicts(self):
        res = merge(a={"a": 1, "b": {"foo": "a"}}, b={"b": {"bar": "b"}})
        self.assertEqual(res, {"a": 1, "b": {"foo": "a", "bar": "b"}})

    def test_merge_lists(self):
        # Previously merge extended lists, in current version we replace lists.
        res = merge(
            a={
                "a": [
                    1,
                    2,
                    3,
                ]
            },
            b={
                "a": [
                    4,
                    5,
                    6,
                ],
                "b": "foobar",
            },
        )
        self.assertEqual(res, {"a": [4, 5, 6], "b": "foobar"})

    def test_merge_none(self):
        """Test that if one value is None it takes the other value"""
        res = merge(
            a={"a": None},
            b={
                "a": [
                    4,
                    5,
                    6,
                ],
                "b": "foobar",
            },
        )
        self.assertEqual(res, {"a": [4, 5, 6], "b": "foobar"})

    def test_merge_no_dict_with_dict(self):
        """Test that it can merge None with {}"""
        res = merge(a=None, b={"a": "foobar"})
        self.assertEqual(res, {"a": "foobar"})

    def test_merge_conflict_types(self):
        """Test that error is raised if try to patch with new type"""
        with self.assertRaises(ValueError):
            merge(
                a={"a": 1},
                b={"a": "1"},
            )

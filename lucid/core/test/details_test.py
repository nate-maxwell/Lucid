"""
# Domain Details Unit Test
"""


import unittest
import enum
from dataclasses import dataclass

import lucid.core.details
import lucid.core.exceptions
import lucid.core.const


class TestDomainDetails(unittest.TestCase):
    def setUp(self) -> None:
        @dataclass
        class SampleDetails(lucid.core.details.DomainDetails):
            name: str = 'default'
            width: int = 512

        self.SampleDetails = SampleDetails

    def test_eq_with_same_fields(self) -> None:
        a = self.SampleDetails(name='thing', width=256)
        b = self.SampleDetails(name='thing', width=256)
        self.assertEqual(a, b)

    def test_eq_with_different_fields(self) -> None:
        a = self.SampleDetails(name='thing1', width=512)
        b = self.SampleDetails(name='thing2', width=512)
        self.assertNotEqual(a, b)

    def test_validate_tokens_valid(self) -> None:
        a = self.SampleDetails(name='thing', width=128)
        self.assertTrue(a.validate_tokens())

    def test_validate_tokens_invalid_enum(self) -> None:
        class FakeEnum(enum.Enum):
            BAD = lucid.core.const.UNASSIGNED

        d = self.SampleDetails(name='thing', width=128)
        d.__dict__['enum'] = FakeEnum.BAD
        self.assertFalse(d.validate_tokens())

    def test_to_dict_returns_serialized_data(self) -> None:
        d = self.SampleDetails(name='thing', width=128)
        result = d.to_dict()
        self.assertIsInstance(result, dict)
        self.assertEqual(result['name'], 'thing')
        self.assertEqual(result['width'], 128)

    def test_verify_details_type_success(self) -> None:
        d = self.SampleDetails(name='test', width=256)
        result = lucid.core.details.verify_details_type(self.SampleDetails, d)
        self.assertIs(result, d)

    def test_verify_details_type_failure(self) -> None:
        @dataclass
        class OtherDetails(lucid.core.details.DomainDetails):
            x: int = 0

        d = OtherDetails()
        with self.assertRaises(lucid.core.exceptions.DomainDetailsException):
            lucid.core.details.verify_details_type(self.SampleDetails, d)

    def test_from_dict_not_implemented(self) -> None:
        with self.assertRaises(NotImplementedError):
            lucid.core.details.DomainDetails.from_dict({'some': 'value'})


if __name__ == '__main__':
    unittest.main()

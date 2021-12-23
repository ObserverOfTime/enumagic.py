#!/usr/bin/env python3

import unittest as ut

import enumagic as em


class IterTestCase(ut.TestCase):
    class _IterFixture(em.IterEnum):
        A = 1
        B = 2
        C = 3

    def test_iter(self):
        it = iter(self._IterFixture)
        self.assertEqual(next(it), ('A', 1))
        self.assertListEqual(
            list(self._IterFixture),
            [('A', 1), ('B', 2), ('C', 3)]
        )

    def test_contains_str(self):
        self.assertIn('B', self._IterFixture)
        self.assertNotIn('D', self._IterFixture)

    def test_contains_enum(self):
        C = self._IterFixture.C
        self.assertIn(C, self._IterFixture)
        C = em.IterEnum('_E', 'C').C
        self.assertNotIn(C, self._IterFixture)


class MappingTestCase(ut.TestCase):
    class _MappingFixture(em.MappingEnum):
        A = 1, 'Alice'
        B = 2, 'Bob'

    def test_init_attrs(self):
        B = self._MappingFixture.B
        self.assertEqual(B.index, 2)
        self.assertEqual(B.label, 'Bob')

    def test_init_dupes(self):
        with self.assertRaises(ValueError):
            class _DupIndex(em.MappingEnum):
                A = 1, 'A'
                B = 1, 'B'
        with self.assertRaises(ValueError):
            class _DupLabel(em.MappingEnum):
                A = 1, 'A'
                B = 2, 'A'

    def test_init_args(self):
        with self.assertRaises(TypeError):
            class _LessArgs(em.MappingEnum):
                A = 1
        with self.assertRaises(TypeError):
            class _MoreArgs(em.MappingEnum):
                A = 1, 2, 3

    def test_iter(self):
        it = iter(self._MappingFixture)
        self.assertEqual(next(it), (1, 'Alice'))
        self.assertListEqual(
            list(self._MappingFixture),
            [(1, 'Alice'), (2, 'Bob')]
        )

    def test_call_int(self):
        self.assertEqual(
            self._MappingFixture(1),
            self._MappingFixture.A
        )
        with self.assertRaises(ValueError):
            self._MappingFixture(0)

    def test_call_str(self):
        self.assertEqual(
            self._MappingFixture('Alice'),
            self._MappingFixture.A
        )
        with self.assertRaises(ValueError):
            self._MappingFixture('N/A')

    def test_call_tuple(self):
        self.assertEqual(
            self._MappingFixture((2, 'Bob')),
            self._MappingFixture.B
        )
        with self.assertRaises(ValueError):
            self._MappingFixture((0, 'N/A'))

    def test_call_invalid(self):
        with self.assertRaises(ValueError):
            self._MappingFixture(1.0)
        with self.assertRaises(TypeError):
            self._MappingFixture()

    def test_str(self):
        A = self._MappingFixture.A
        self.assertEqual(str(A), 'Alice')

    def test_int(self):
        A = self._MappingFixture.A
        self.assertEqual(int(A), 1)

    def test_index(self):
        test = [1, 10, 100, 1000]
        A = self._MappingFixture.A
        self.assertEqual(test[A], 10)

    def test_items(self):
        items = self._MappingFixture.items
        self.assertDictEqual(items, {'Alice': 1, 'Bob': 2})

    def test_indices(self):
        indices = self._MappingFixture.indices
        self.assertTupleEqual(indices, (1, 2))

    def test_labels(self):
        labels = self._MappingFixture.labels
        self.assertTupleEqual(labels, ('Alice', 'Bob'))


class StrTestCase(ut.TestCase):
    class _StrFixture(em.StrEnum):
        A = 'Alice'
        B = 'Bob'

    def test_instance(self):
        A = self._StrFixture.A
        self.assertIsInstance(A, str)

    def test_str(self):
        B = self._StrFixture.B
        self.assertEqual(str(B), 'Bob')


if __name__ == '__main__':
    ut.main(module=None)

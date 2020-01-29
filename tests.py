#!/usr/bin/env python3

import unittest as ut
from importlib.util import find_spec
from sys import version_info

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

    @ut.skipIf(version_info < (3, 8), 'requires Python 3.8')
    def test_contains_invalid(self):
        with self.assertRaises(TypeError):
            1 in self._IterFixture


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


class ChoiceTestCase(ut.TestCase):
    class _ChoiceFixture(em.django.ChoiceEnum):
        A = 'Alice'
        B = 'Bob'

    def test_instance(self):
        A = self._ChoiceFixture.A
        self.assertIsInstance(A, str)
        cls = self._ChoiceFixture.__class__
        self.assertIs(cls.__base__, em.IterMeta)

    def test_new(self):
        attr = 'do_not_call_in_templates'
        self.assertTrue(hasattr(self._ChoiceFixture, attr))
        self.assertTrue(getattr(self._ChoiceFixture, attr))

    def test_getitem(self):
        B = self._ChoiceFixture['B']
        self.assertEqual(B, 'Bob')

    def test_str(self):
        B = self._ChoiceFixture.B
        self.assertEqual(str(B), 'B')

    def test_hash(self):
        A = self._ChoiceFixture.A
        self.assertEqual(hash(A), hash('A'))

    def test_eq(self):
        A1 = self._ChoiceFixture.A
        A2 = em.django.ChoiceEnum('_A', 'A').A
        self.assertEqual(A1, A2)

    @ut.skipUnless(find_spec('django'), 'requires Django')
    def test_choices(self):
        from django.conf import settings
        from django.db.models import CharField, Model
        settings.configure(INSTALLED_APPS=[__name__])
        __import__('django').setup()
        person = type('_Person', (Model,), {
            'name': CharField(choices=self._ChoiceFixture),
            '__module__': __name__
        })(name=self._ChoiceFixture.A)
        name = person._meta.get_field('name')
        display = person.get_name_display()
        self.assertEqual(person.name, 'A')
        self.assertEqual(display, 'Alice')
        self.assertListEqual(
            list(self._ChoiceFixture),
            list(name.choices)
        )


if __name__ == '__main__':
    ut.main()

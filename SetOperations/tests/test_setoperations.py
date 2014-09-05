'''
Created on 04-Sep-2014

@author: Rahul

Description: Holds all of our unit tests related to set operations.
'''
from unittest.case import TestCase
from SetOperations.core.hset import HSet
from SetOperations.core.operations import union, intersect, difference,\
    symm_difference, perform_operation
from SetOperations.core.exceptions import NotAnHSet


class TestSetOperations(TestCase):
    '''
        Tests to make sure all the operations are working as expected.
    '''
    def setUp(self):
        '''
            Initial data fixtures
        '''
        self.shapes = HSet(["circle", "square", "rectangle", "heart", "diamond"])  # @IgnorePep8
        self.pocker = HSet(["heart", "diamond", "spade", "turn"])

    def test_add_member_should_add_a_new_element(self):
        '''
            Tests the functionality for adding a new member.
        '''
        self.shapes.add("triangle")
        self.assertIn("triangle", self.shapes, "Problem adding a new element!")

    def test_add_membesr_should_add_all_new_element(self):
        '''
            Tests the functionality for adding more than one element.
        '''
        self.shapes.add_all(["triangle", "star"])
        self.assertIn("triangle", self.shapes)
        self.assertIn("star", self.shapes)

    def test_remove_member_should_remove_element_from_set(self):
        '''
            Tests remove_member removes one the element from the set.
        '''
        self.shapes.remove("circle")
        self.assertNotIn("circle", self.shapes)

    def test_remove_members_should_remove_all_elements_from_set(self):
        '''
            Tests remove_members removes all the elements from the set.
        '''
        self.shapes.remove_all(["circle", "rectangle"])
        self.assertNotIn("circle", self.shapes)
        self.assertNotIn("rectangle", self.shapes)

    def test_removing_non_existent_element_should_not_change_cardinality(self):
        '''
            Tests, removing an element not present in the set should have no
            effect on cardinality.
        '''
        original_card = self.shapes.cardinality
        self.shapes.remove("unknown")
        self.assertEqual(original_card, self.shapes.cardinality)

    def test_the_set_cardinality(self):
        '''
            Asserts the expected cardinality matches with the expected value.
        '''
        self.assertEqual(5, self.shapes.cardinality)
        self.assertEqual(4, self.pocker.cardinality)

    def test_adding_new_element_should_update_cardinality(self):
        '''
            Adding a new element in the set should update the cardinality.
        '''
        original_card = self.shapes.cardinality
        self.shapes.add("triangle")
        self.assertEqual(original_card + 1, self.shapes.cardinality)

    def test_adding_duplicate_element_should_not_change_cardinality(self):
        '''
            Adding an element which is already present should not change
            cardinality.
        '''
        original_card = self.shapes.cardinality
        self.shapes.add("circle")
        self.assertEqual(original_card, self.shapes.cardinality)

    def test_membership_for_valid_element(self):
        '''
            Asserts the membership check succeeds for element present in the
            set.
        '''
        self.assertTrue(self.shapes.contains("circle"))

    def test_membership_for_invalid_element(self):
        '''
            Asserts the membership check fails for element absent in the set.
        '''
        self.assertFalse(self.shapes.contains("unknown"))

    def test_union_operation(self):
        '''
            Tests the results of union operation between two sets.
        '''
        res_set = union(self.shapes, self.pocker)
        self.assertListEqual(["circle", "diamond", "heart", "rectangle", "spade", "square", "turn"], sorted(res_set.members))  # @IgnorePep8

    def test_intersection_operation(self):
        '''
            Tests the results of intersection between two sets.
        '''
        res_set = intersect(self.shapes, self.pocker)
        self.assertListEqual(["diamond", "heart"], sorted(res_set.members))

    def test_difference_operation(self):
        '''
            Tests the results of difference operation between two sets.
        '''
        res_set = difference(self.shapes, self.pocker)
        self.assertListEqual(["circle", "rectangle", "square"], sorted(res_set.members))  # @IgnorePep8

    def test_symm_difference_operation(self):
        '''
            Tests the results of symmetric difference between two sets.
        '''
        res_set = symm_difference(self.shapes, self.pocker)
        self.assertListEqual(["circle", "rectangle", "spade", "square", "turn"], sorted(res_set.members))  # @IgnorePep8

    def test_union_of_set_with_none(self):
        '''
            Tests the results of union operation between a set and None.
        '''
        with self.assertRaises(NotAnHSet):
            union(self.shapes, None)

    def test_intersection_of_set_with_none(self):
        '''
            Tests the results of intersection between a set and None.
        '''
        with self.assertRaises(NotAnHSet):
            intersect(self.shapes, None)

    def test_difference_of_set_with_none(self):
        '''
            Tests the results of difference operation between a set and None.
        '''
        with self.assertRaises(NotAnHSet):
            difference(self.shapes, None)

    def test_symm_difference_of_set_with_none(self):
        '''
            Tests the results of symmetric difference between a set and None.
        '''
        with self.assertRaises(NotAnHSet):
            symm_difference(self.shapes, None)

    def test_membership_with_none_type(self):
        '''
            Tests the membership behavior with None type.
        '''
        self.assertFalse(self.shapes.contains(None))

    def test_perform_operation_delegates_to_correct_function(self):
        '''
            Tests the wrapper method perform operation delegates to the correct
            method with the correct parameters.
        '''
        res_set = perform_operation(intersect, self.shapes, self.pocker)
        self.assertListEqual(["diamond", "heart"], sorted(res_set.members))


import unittest
from unittest.mock import patch
from io import StringIO

from artefact_management import (
    get_required_input,
    get_condition,
    generate_artefact_id,
    add_artefact,
    view_artefacts,
    find_artefacts,
    find_artefact_by_id,
    update_condition
)


class TestArtefactManagement(unittest.TestCase):

    def setUp(self):
        """Create sample records before each test."""
        self.artefacts = [
            {
                "id": "A001",
                "name": "Old Photograph",
                "category": "Photograph",
                "location": "Display Case B",
                "condition": "Good"
            },
            {
                "id": "A002",
                "name": "Ancient Vase",
                "category": "Pottery",
                "location": "Display Case A",
                "condition": "Damage"
            }
        ]

    # TEST 1: Required text input
    @patch("builtins.input", return_value="Old Photograph")
    def test_required_input(self, mock_input):
        result = get_required_input("Enter name: ")
        self.assertEqual(result, "Old Photograph")

    # TEST 2: Blank input validation
    @patch("builtins.input", side_effect=["", "Ancient Vase"])
    def test_blank_input(self, mock_input):
        with patch("sys.stdout", new=StringIO()):
            result = get_required_input("Enter name: ")

        self.assertEqual(result, "Ancient Vase")

    # TEST 3: Valid condition selection
    @patch("builtins.input", return_value="1")
    def test_valid_condition(self, mock_input):
        with patch("sys.stdout", new=StringIO()):
            result = get_condition()

        self.assertEqual(result, "Good")

    # TEST 4: Invalid condition followed by valid input
    @patch("builtins.input", side_effect=["9", "3"])
    def test_invalid_condition(self, mock_input):
        with patch("sys.stdout", new=StringIO()):
            result = get_condition()

        self.assertEqual(result, "Under Repair")

    # TEST 5: Generate next artefact ID
    def test_generate_id(self):
        result = generate_artefact_id(self.artefacts)
        self.assertEqual(result, "A003")

    # TEST 6: Generate ID for empty collection
    def test_generate_first_id(self):
        result = generate_artefact_id([])
        self.assertEqual(result, "A001")

    # TEST 7: Add a new artefact
    @patch(
        "builtins.input",
        side_effect=[
            "Historic Coin",
            "Coin",
            "Display Case C",
            "1"
        ]
    )
    def test_add_artefact(self, mock_input):
        with patch("sys.stdout", new=StringIO()):
            add_artefact(self.artefacts)

        self.assertEqual(len(self.artefacts), 3)
        self.assertEqual(
            self.artefacts[2]["id"], "A003"
        )
        self.assertEqual(
            self.artefacts[2]["name"], "Historic Coin"
        )
        self.assertEqual(
            self.artefacts[2]["condition"], "Good"
        )

    # TEST 8: View existing artefacts
    def test_view_artefacts(self):
        output = StringIO()

        with patch("sys.stdout", new=output):
            view_artefacts(self.artefacts)

        self.assertIn("Old Photograph", output.getvalue())
        self.assertIn("Ancient Vase", output.getvalue())

    # TEST 9: View empty collection
    def test_view_empty_collection(self):
        output = StringIO()

        with patch("sys.stdout", new=output):
            view_artefacts([])

        self.assertNotIn("Old Photograph", output.getvalue())

    # TEST 10: Search existing artefact
    def test_search_existing_artefact(self):
        results = find_artefacts(
            self.artefacts, "Old Photograph"
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], "A001")

    # TEST 11: Case-insensitive search
    def test_case_insensitive_search(self):
        results = find_artefacts(
            self.artefacts, "old photograph"
        )

        self.assertEqual(len(results), 1)

    # TEST 12: Partial name search
    def test_partial_search(self):
        results = find_artefacts(
            self.artefacts, "Vase"
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], "A002")

    # TEST 13: Search nonexistent artefact
    def test_search_nonexistent(self):
        results = find_artefacts(
            self.artefacts, "Unknown Item"
        )

        self.assertEqual(len(results), 0)

    # TEST 14: Find artefact using valid ID
    def test_find_by_valid_id(self):
        result = find_artefact_by_id(
            self.artefacts, "A001"
        )

        self.assertIsNotNone(result)
        self.assertEqual(
            result["name"], "Old Photograph"
        )

    # TEST 15: Find artefact using invalid ID
    def test_find_by_invalid_id(self):
        result = find_artefact_by_id(
            self.artefacts, "A999"
        )

        self.assertIsNone(result)

    # TEST 16: Update artefact condition
    @patch("builtins.input", side_effect=["A001", "3"])
    def test_update_condition(self, mock_input):
        with patch("sys.stdout", new=StringIO()):
            update_condition(self.artefacts)

        self.assertEqual(
            self.artefacts[0]["condition"],
            "Under Repair"
        )

    # TEST 17: Invalid ID must not change records
    @patch("builtins.input", return_value="A999")
    def test_invalid_update_id(self, mock_input):
        with patch("sys.stdout", new=StringIO()):
            update_condition(self.artefacts)

        self.assertEqual(
            self.artefacts[0]["condition"], "Good"
        )
        self.assertEqual(
            self.artefacts[1]["condition"], "Damage"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)

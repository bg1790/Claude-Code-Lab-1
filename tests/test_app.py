import os
import tempfile
import unittest
from unittest.mock import patch

from app import ACTIVITIES, collect_survey_data, generate_svg_graph


class AppTests(unittest.TestCase):
    def test_collect_survey_data_with_activity_retry(self):
        inputs = iter(
            [
                "Healthcare",
                "12",
                "1",
                "Alex",
                "invalid",
                "music",
            ]
        )

        with patch("builtins.input", side_effect=lambda _: next(inputs)):
            data = collect_survey_data()

        self.assertEqual(data.industry, "Healthcare")
        self.assertEqual(data.phd_professional_count, 12)
        self.assertEqual(len(data.volunteers), 1)
        self.assertEqual(data.volunteers[0].name, "Alex")
        self.assertEqual(data.volunteers[0].activity, "music")

    def test_generate_svg_graph_contains_expected_labels(self):
        inputs = iter(
            [
                "Technology",
                "6",
                "2",
                "Nora",
                "drawing",
                "Sam",
                "puzzles",
            ]
        )

        with patch("builtins.input", side_effect=lambda _: next(inputs)):
            data = collect_survey_data()

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = os.path.join(tmp_dir, "graph.svg")
            result_path = generate_svg_graph(data, output_path=output_path)

            self.assertEqual(result_path, output_path)
            with open(output_path, "r", encoding="utf-8") as svg_file:
                content = svg_file.read()

        self.assertIn("Volunteer Name (X axis)", content)
        self.assertIn("Art Activity (Y axis)", content)
        self.assertIn("Nora", content)
        self.assertIn("Sam", content)
        for activity in ACTIVITIES:
            self.assertIn(activity, content)


if __name__ == "__main__":
    unittest.main()

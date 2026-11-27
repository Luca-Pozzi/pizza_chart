import os
import unittest
from unittest.mock import patch

os.environ.setdefault("FLASK_SECRET_KEY", "test-only-secret")
os.environ.setdefault("GITHUB_CLIENT_ID", "test-only-client")
os.environ.setdefault("GITHUB_CLIENT_SECRET", "test-only-client-secret")
os.environ.setdefault("MPLBACKEND", "Agg")

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from app.app import app
from pizza_chart.pizza_chart import plot


class CustomChartTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    @patch("app.app.create_pizza_chart")
    def test_draws_chart_for_anonymous_custom_input(self, create_chart):
        create_chart.return_value = Figure()

        response = self.client.post(
            "/custom-chart",
            data={
                "pizza_name": ["Friday special"],
                "pizza_count": ["3"],
                "pizza_visual": ["salame_piccante"],
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"data:image/png;base64,", response.data)
        create_chart.assert_called_once_with(
            [("Friday special", 3)],
            images=["salame_piccante"],
            cutoff=0,
            show=False,
            theme="dark",
        )

    @patch("app.app.create_pizza_chart")
    @patch("app.app.render_home", return_value="invalid input")
    def test_rejects_non_positive_counts(self, render_home, create_chart):
        response = self.client.post(
            "/custom-chart",
            data={
                "pizza_name": ["Margherita"],
                "pizza_count": ["0"],
                "pizza_visual": ["margherita"],
            },
        )

        self.assertEqual(response.status_code, 400)
        render_home.assert_called_once()
        create_chart.assert_not_called()

    @patch("app.app.create_pizza_chart")
    @patch("app.app.render_home", return_value="invalid input")
    def test_rejects_visuals_not_in_the_asset_list(self, render_home, create_chart):
        response = self.client.post(
            "/custom-chart",
            data={
                "pizza_name": ["Margherita"],
                "pizza_count": ["1"],
                "pizza_visual": ["../../outside"],
            },
        )

        self.assertEqual(response.status_code, 400)
        render_home.assert_called_once()
        create_chart.assert_not_called()

    @patch("pizza_chart.pizza_chart._img_to_pie")
    def test_chart_uses_selected_visual_for_free_text_label(self, add_visual):
        figure = plot(
            [("Friday special", 3)],
            images=["salame_piccante"],
            cutoff=0,
            show=False,
            theme="dark",
        )
        try:
            image_path = add_visual.call_args.args[0]
            self.assertTrue(image_path.endswith("_salame_piccante.png"))
        finally:
            plt.close(figure)


if __name__ == "__main__":
    unittest.main()

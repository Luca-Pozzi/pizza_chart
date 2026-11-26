"""Generate a standalone HTML export of the pizza-day heatmap."""

from pathlib import Path

from pizza_chart.heatmap import create_heatmap_figure


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    csv_path = root / "data" / "data.csv"
    excel_path = csv_path.with_suffix(".xlsx")
    data_path = csv_path if csv_path.exists() else excel_path
    if not data_path.exists():
        raise FileNotFoundError(f"No data file found at {csv_path} or {excel_path}")

    figure = create_heatmap_figure(data_path)
    docs_dir = root / "docs"
    docs_dir.mkdir(exist_ok=True)
    figure.write_html(
        docs_dir / "heatmap.html",
        include_plotlyjs="cdn",
        full_html=False,
        config={"displayModeBar": False, "responsive": True},
    )
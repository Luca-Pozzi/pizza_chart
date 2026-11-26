"""Build the interactive pizza-day heatmap."""

from datetime import datetime
from pathlib import Path
from typing import Optional, Union

import numpy as np
import pandas as pd
import plotly.graph_objs as go


def create_heatmap_figure(
    data_path: Union[str, Path],
    today: Optional[datetime] = None,
) -> go.Figure:
    """Create a Plotly heatmap for pizza orders in the previous 51 weeks."""
    data_path = Path(data_path)
    if data_path.suffix.lower() == ".csv":
        df = pd.read_csv(data_path)
    elif data_path.suffix.lower() in {".xls", ".xlsx"}:
        df = pd.read_excel(data_path, sheet_name="Orders", usecols=[0, 1, 2, 3])
    else:
        raise ValueError(f"Unsupported data file: {data_path}")

    df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")
    today = pd.Timestamp(today or datetime.today()).normalize()

    daily_totals = df.groupby("Date")["#"].sum()
    dates = pd.date_range(
        start=today - pd.DateOffset(weeks=51),
        end=today,
        freq="D",
    )
    dates = dates.union([dates[-1] + pd.Timedelta(days=6 - today.weekday())])

    heatmap_df = (
        daily_totals.reindex(dates, fill_value=0)
        .rename("#")
        .rename_axis("Date")
        .reset_index()
    )
    heatmap_df["month"] = heatmap_df["Date"].dt.month_name()
    heatmap_df["weekday"] = heatmap_df["Date"].dt.day_name()
    heatmap_df["week"] = heatmap_df["Date"].dt.isocalendar().week

    orders_per_day = (
        df.groupby(["Date", "Pizza"])["#"]
        .sum()
        .reset_index()
    )
    orders_per_day["desc"] = (
        "• " + orders_per_day["Pizza"] + " x" + orders_per_day["#"].astype(str)
    )
    orders_summary = orders_per_day.groupby("Date")["desc"].apply(
        lambda orders: "<br>".join(orders)
    )
    heatmap_df["orders"] = heatmap_df["Date"].map(orders_summary).fillna("")
    heatmap_df["date_str"] = heatmap_df["Date"].dt.strftime("%d-%m-%Y")

    weeks_ordered = heatmap_df["week"].unique().tolist()

    def pivot_heatmap(values: str) -> pd.DataFrame:
        return (
            heatmap_df.pivot_table(
                index="weekday",
                columns="week",
                values=values,
                aggfunc="sum" if values == "#" else "first",
                fill_value=0 if values == "#" else "",
            )[weeks_ordered]
            .reindex(
                [
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday",
                    "Sunday",
                ]
            )
        )

    totals_pivoted = pivot_heatmap("#")
    dates_pivoted = pivot_heatmap("date_str")
    orders_pivoted = pivot_heatmap("orders")

    figure = go.Figure(
        go.Heatmap(
            x=[str(week) for week in weeks_ordered],
            y=totals_pivoted.index,
            z=totals_pivoted.values,
            customdata=np.dstack((dates_pivoted.values, orders_pivoted.values)),
            xgap=5,
            ygap=5,
            showscale=False,
            hoverongaps=False,
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "<extra>We had %{z} pizzas on this day<br>"
                "%{customdata[1]}</extra>"
            ),
            colorscale=[
                [0.00, "rgb(128, 128, 128)"],
                [0.10, "rgb(250, 244, 220)"],
                [0.25, "rgb(250, 244, 220)"],
                [0.40, "rgb(199, 113,   4)"],
                [0.65, "rgb(215, 118,   3)"],
                [0.80, "rgb(231,  48,  45)"],
                [1.00, "rgb(231,  48,  45)"],
            ],
        )
    )

    month_changes = heatmap_df["Date"].dt.month.diff().fillna(0).ne(0)
    month_labels = heatmap_df.loc[month_changes, "month"].to_numpy()
    month_weeks = heatmap_df.loc[month_changes, "week"].to_numpy()
    current_week = today.isocalendar().week

    figure.update_layout(
        xaxis_tickvals=[],
        xaxis_ticktext=[],
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        autosize=True,
        height=330,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        xaxis_fixedrange=False,
        yaxis_fixedrange=True,
    )

    for week, month in zip(month_weeks, month_labels):
        x = week - (current_week + 1) if week >= current_week + 1 else 52 - (current_week + 1 - week)
        figure.add_annotation(
            x=x,
            y=6.5,
            text=month,
            showarrow=False,
            xanchor="center",
            yanchor="top",
            font={"size": 12, "color": "white"},
        )

    figure.update_yaxes(autorange="reversed", scaleanchor="x")
    return figure

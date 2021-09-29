import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from sklearn.metrics import r2_score

from asf_mission_primer_la_stats import PROJECT_DIR


def scatter_with_trendline(
    data, x_factor, y_factor, s, ylim_max, xlabel, ylabel, title, filename
):
    """Scatter plot with trendline and annotated R^2 value."""
    x = data[x_factor]
    y = data[y_factor]
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)

    fig, ax = plt.subplots()

    ax.scatter(x=x, y=y, s=s)
    ax.plot(x, p(x), "r")
    ax.set_ylim(0, ylim_max)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)

    ax.annotate(
        "$R^2 =$" + str(round(r2_score(y, p(x)), 2)),
        xy=(0.7, 0.5),
        xycoords="axes fraction",
        color="red",
        size="15",
    )

    plt.savefig(PROJECT_DIR / "outputs/figures" / filename)


def line_plot(data, ylim_max, xlabel, ylabel, title, filename, colour="blue"):
    """Single line plot."""
    fig, ax = plt.subplots()
    ax.plot(data, c=colour)
    ax.set_ylim(0, ylim_max)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    plt.tight_layout()
    plt.savefig(PROJECT_DIR / "outputs/figures" / filename)


def multi_line_plot(
    data,
    las,
    ave_data,
    ave_label,
    x_factor,
    y_factor,
    ylim_max,
    xlabel,
    ylabel,
    title,
    filename,
):
    """Multiple line plot. Average plotted in grey."""
    fig, ax = plt.subplots()

    for la in las[::-1]:
        la_data = data[data["la_name"] == la]
        x = la_data[x_factor]
        y = la_data[y_factor]
        ax.plot(x, y, label=la)

    ax.plot(ave_data, c="grey", alpha=0.3, label=ave_label)

    ax.legend()
    ax.set_ylim(0, ylim_max)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    plt.savefig(PROJECT_DIR / "outputs/figures" / filename)


def highlight_ni_scatter(
    data, x_factor, y_factor, xlim_max, ylim_max, x_label, y_label, title, filename
):
    """Scatter plot with Northern Irish LAs highlighted."""
    fig, ax = plt.subplots()

    not_ni = data[data.region != "Northern Ireland"]
    ni = data[data.region == "Northern Ireland"]

    x = not_ni[x_factor]
    y = not_ni[y_factor]
    ax.scatter(x, y, s=3, alpha=0.5)

    x = ni[x_factor]
    y = ni[y_factor]
    ax.scatter(x, y, s=3, c="red", label="Northern Irish LAs", alpha=0.5)

    ax.legend(loc="lower right")
    ax.set_xlim(0, xlim_max)
    ax.set_ylim(0, ylim_max)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)

    plt.savefig(PROJECT_DIR / "outputs/figures" / filename)


def line_region_plot(data, line1, factor, x_label, y_label, title, filename):
    """Line graph with a line for each region, with one line highlighted."""
    fig, ax = plt.subplots()

    for region in set(data.region) - set([line1]):
        regional_data = data[data.region == region]
        x = regional_data.year
        y = regional_data[factor]
        ax.plot(x, y, c="grey", linewidth=1)

    line_data = data[data.region == line1]
    x = line_data.year
    y = line_data[factor]
    ax.plot(x, y, c="red", linewidth=2, label=line1)

    ax.legend()
    ax.yaxis.set_major_formatter(
        mtick.PercentFormatter(xmax=1, decimals=None, symbol="%", is_latex=False)
    )
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    plt.tight_layout()
    plt.savefig(PROJECT_DIR / "outputs/figures" / filename)


def multi_line_region_plot(
    data,
    line_1,
    col_1,
    line_2,
    col_2,
    factor,
    ylim_max,
    x_label,
    y_label,
    title,
    filename,
):
    """Line graph with a line for each region, with two lines highlighted."""
    fig, ax = plt.subplots()

    for region in set(data.region) - set([line_1, line_2]):
        regional_data = data[data.region == region]
        x = regional_data.year
        y = regional_data[factor]
        ax.plot(x, y, c="grey", linewidth=1)

    line1_data = data[data.region == line_1]
    x = line1_data.year
    y = line1_data[factor]
    ax.plot(x, y, c=col_1, linewidth=2, label=line_1)

    line2_data = data[data.region == line_2]
    x = line2_data.year
    y = line2_data[factor]
    ax.plot(x, y, c=col_2, linewidth=2, label=line_2)

    ax.set_ylim(0, ylim_max)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.legend()
    plt.savefig(PROJECT_DIR / "outputs/figures" / filename)


def country_bar_plot(data, factor, percentages, ylim, xlabel, ylabel, title, filename):

    fig, ax = plt.subplots()

    ax.bar(data.index, data[factor])

    if percentages:
        ax.yaxis.set_major_formatter(
            mtick.PercentFormatter(xmax=1, decimals=None, symbol="%", is_latex=False)
        )
        labels = [str(round(value * 100, 2)) + "%" for value in data[factor]]
        offset = 0.03
    else:
        labels = [str(round(value, 2)) for value in data[factor]]
        offset = 0.1

    ax.set_ylim(0, ylim)

    rects = ax.patches

    for rect, label in zip(rects, labels):
        height = rect.get_height()
        ax.text(
            rect.get_x() + rect.get_width() / 2,
            height + offset,
            label,
            ha="center",
            va="bottom",
        )

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    plt.tight_layout()
    plt.savefig(PROJECT_DIR / "outputs/figures" / filename)

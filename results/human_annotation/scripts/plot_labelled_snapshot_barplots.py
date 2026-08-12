import argparse
import json
import math
from pathlib import Path


LANGUAGE_ORDER = ("en-ar_AR", "en-ru_RU", "en-zh_CN")
MODEL_A_COLOR = "#2f855a"
MODEL_B_COLOR = "#b7791f"
TIE_COLOR = "#718096"
UNCLEAR_COLOR = "#cbd5e0"
AXIS_COLOR = "#2d3748"
TEXT_COLOR = "#1a202c"
BG_COLOR = "#ffffff"
ERROR_BAR_COLOR = "#2d3748"
TEXT_ON_DARK_COLOR = "#ffffff"


def ordered_labels_and_summaries(summary_payload):
    labels = []
    summaries = []
    for language_pair in LANGUAGE_ORDER:
        language_payload = summary_payload["languages"].get(language_pair)
        if language_payload is None:
            continue
        labels.append(language_pair)
        summaries.append(language_payload["summary"])
    labels.append("overall")
    summaries.append(summary_payload["overall"])
    return labels, summaries


def svg_header(width, height):
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        'viewBox="0 0 {w} {h}">'.format(w=width, h=height)
    )


def svg_footer():
    return "</svg>"


def proportion_standard_error(numerator, denominator):
    if denominator <= 0:
        return 0.0
    proportion = float(numerator) / float(denominator)
    return math.sqrt(proportion * (1.0 - proportion) / float(denominator))


def summary_sem(summary, sem_key, count_key, denominator_key):
    if sem_key in summary:
        return float(summary[sem_key])
    counts = summary.get("counts", {})
    numerator = counts.get(count_key, 0)
    denominator = summary.get(denominator_key, 0)
    return proportion_standard_error(numerator, denominator)


def clamp(value, lower, upper):
    return max(lower, min(upper, value))


def percent_to_y(percent_value, *, top, plot_height):
    return top + plot_height - (percent_value / 100.0) * plot_height


def add_error_bar(lines, center_x, value_percent, sem_percent, *, top, plot_height):
    lower = clamp(value_percent - sem_percent, 0.0, 100.0)
    upper = clamp(value_percent + sem_percent, 0.0, 100.0)
    y1 = percent_to_y(lower, top=top, plot_height=plot_height)
    y2 = percent_to_y(upper, top=top, plot_height=plot_height)
    cap_half_width = 6.0
    lines.append(
        '<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{c}" stroke-width="1.5"/>'.format(
            x=center_x, y1=y1, y2=y2, c=ERROR_BAR_COLOR
        )
    )
    lines.append(
        '<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y1}" stroke="{c}" stroke-width="1.5"/>'.format(
            x1=center_x - cap_half_width,
            x2=center_x + cap_half_width,
            y1=y1,
            c=ERROR_BAR_COLOR,
        )
    )
    lines.append(
        '<line x1="{x1}" y1="{y2}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="1.5"/>'.format(
            x1=center_x - cap_half_width,
            x2=center_x + cap_half_width,
            y2=y2,
            c=ERROR_BAR_COLOR,
        )
    )


def format_percent_and_sem(percent_value, sem_percent):
    return "{:.0f}+/-{:.0f}".format(percent_value, sem_percent)


def make_decisive_win_rates_svg(summary_payload, output_path):
    model_a = summary_payload["model_a"]
    model_b = summary_payload["model_b"]
    labels, summaries = ordered_labels_and_summaries(summary_payload)
    model_a_rates = [summary["model_a_win_rate_decisive"] * 100.0 for summary in summaries]
    model_b_rates = [summary["model_b_win_rate_decisive"] * 100.0 for summary in summaries]
    model_a_sems = [
        summary_sem(
            summary,
            "model_a_win_rate_decisive_sem",
            "model_a_wins",
            "decisive_items",
        )
        * 100.0
        for summary in summaries
    ]
    model_b_sems = [
        summary_sem(
            summary,
            "model_b_win_rate_decisive_sem",
            "model_b_wins",
            "decisive_items",
        )
        * 100.0
        for summary in summaries
    ]

    width = 920
    height = 480
    left = 70
    right = 30
    top = 72
    bottom = 90
    plot_width = width - left - right
    plot_height = height - top - bottom
    group_width = float(plot_width) / max(len(labels), 1)
    bar_width = min(36.0, group_width * 0.32)

    lines = [svg_header(width, height)]
    lines.append('<rect width="100%" height="100%" fill="{}"/>'.format(BG_COLOR))
    lines.append(
        '<text x="{x}" y="28" font-size="20" fill="{c}" font-family="sans-serif">'
        'Human annotation decisive win rates</text>'.format(x=left, c=TEXT_COLOR)
    )
    lines.append(
        '<text x="{x}" y="44" font-size="12" fill="{c}" font-family="sans-serif">'
        '{a} vs {b}</text>'.format(x=left, c=TEXT_COLOR, a=model_a, b=model_b)
    )
    lines.append(
        '<text x="{x}" y="60" font-size="11" fill="{c}" font-family="sans-serif">'
        'Error bars show +/- 1 standard error of the mean.</text>'.format(
            x=left, c=TEXT_COLOR
        )
    )

    y0 = top + plot_height
    lines.append(
        '<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{c}" stroke-width="1.5"/>'.format(
            x1=left, x2=width - right, y=y0, c=AXIS_COLOR
        )
    )
    lines.append(
        '<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{c}" stroke-width="1.5"/>'.format(
            x=left, y1=top, y2=y0, c=AXIS_COLOR
        )
    )

    for tick in (0, 25, 50, 75, 100):
        y = top + plot_height - (tick / 100.0) * plot_height
        dash = "4 4" if tick not in (0, 100) else "none"
        lines.append(
            '<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="#e2e8f0" stroke-width="1" stroke-dasharray="{dash}"/>'.format(
                x1=left, x2=width - right, y=y, dash=dash
            )
        )
        lines.append(
            '<text x="{x}" y="{y}" font-size="11" fill="{c}" font-family="sans-serif" text-anchor="end">{label}%</text>'.format(
                x=left - 8, y=y + 4, c=TEXT_COLOR, label=tick
            )
        )

    ref_y = top + plot_height - 0.5 * plot_height
    lines.append(
        '<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{c}" stroke-width="1.5" stroke-dasharray="6 4"/>'.format(
            x1=left, x2=width - right, y=ref_y, c="#4a5568"
        )
    )

    for idx, label in enumerate(labels):
        group_center = left + group_width * (idx + 0.5)
        a_height = (model_a_rates[idx] / 100.0) * plot_height
        b_height = (model_b_rates[idx] / 100.0) * plot_height
        ax = group_center - bar_width - 4
        bx = group_center + 4
        ay = y0 - a_height
        by = y0 - b_height
        lines.append(
            '<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}"><title>{title}</title></rect>'.format(
                x=ax,
                y=ay,
                w=bar_width,
                h=max(a_height, 0.0),
                c=MODEL_A_COLOR,
                title="{}: {} decisive win rate {}% +/- {}%".format(
                    label,
                    model_a,
                    int(round(model_a_rates[idx])),
                    int(round(model_a_sems[idx])),
                ),
            )
        )
        lines.append(
            '<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}"><title>{title}</title></rect>'.format(
                x=bx,
                y=by,
                w=bar_width,
                h=max(b_height, 0.0),
                c=MODEL_B_COLOR,
                title="{}: {} decisive win rate {}% +/- {}%".format(
                    label,
                    model_b,
                    int(round(model_b_rates[idx])),
                    int(round(model_b_sems[idx])),
                ),
            )
        )
        add_error_bar(
            lines,
            ax + bar_width / 2.0,
            model_a_rates[idx],
            model_a_sems[idx],
            top=top,
            plot_height=plot_height,
        )
        add_error_bar(
            lines,
            bx + bar_width / 2.0,
            model_b_rates[idx],
            model_b_sems[idx],
            top=top,
            plot_height=plot_height,
        )
        lines.append(
            '<text x="{x}" y="{y}" font-size="11" fill="{c}" font-family="sans-serif" text-anchor="middle">{label}</text>'.format(
                x=ax + bar_width / 2.0, y=max(ay - 6, top + 12), c=TEXT_COLOR, label=int(round(model_a_rates[idx]))
            )
        )
        lines.append(
            '<text x="{x}" y="{y}" font-size="11" fill="{c}" font-family="sans-serif" text-anchor="middle">{label}</text>'.format(
                x=bx + bar_width / 2.0, y=max(by - 6, top + 12), c=TEXT_COLOR, label=int(round(model_b_rates[idx]))
            )
        )
        lines.append(
            '<text x="{x}" y="{y}" font-size="12" fill="{c}" font-family="sans-serif" text-anchor="middle">{label}</text>'.format(
                x=group_center, y=height - 45, c=TEXT_COLOR, label=label
            )
        )

    legend_y = height - 20
    lines.append('<rect x="{x}" y="{y}" width="14" height="14" fill="{c}"/>'.format(x=left, y=legend_y - 11, c=MODEL_A_COLOR))
    lines.append('<text x="{x}" y="{y}" font-size="12" fill="{c}" font-family="sans-serif">{label}</text>'.format(x=left + 20, y=legend_y, c=TEXT_COLOR, label=model_a))
    lines.append('<rect x="{x}" y="{y}" width="14" height="14" fill="{c}"/>'.format(x=left + 210, y=legend_y - 11, c=MODEL_B_COLOR))
    lines.append('<text x="{x}" y="{y}" font-size="12" fill="{c}" font-family="sans-serif">{label}</text>'.format(x=left + 230, y=legend_y, c=TEXT_COLOR, label=model_b))

    lines.append(svg_footer())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def make_label_mix_svg(summary_payload, output_path):
    model_a = summary_payload["model_a"]
    model_b = summary_payload["model_b"]
    labels, summaries = ordered_labels_and_summaries(summary_payload)

    width = 920
    height = 500
    left = 70
    right = 30
    top = 72
    bottom = 90
    plot_width = width - left - right
    plot_height = height - top - bottom
    group_width = float(plot_width) / max(len(labels), 1)
    bar_width = min(64.0, group_width * 0.5)

    lines = [svg_header(width, height)]
    lines.append('<rect width="100%" height="100%" fill="{}"/>'.format(BG_COLOR))
    lines.append(
        '<text x="{x}" y="28" font-size="20" fill="{c}" font-family="sans-serif">'
        'Human annotation label mix</text>'.format(x=left, c=TEXT_COLOR)
    )
    lines.append(
        '<text x="{x}" y="44" font-size="12" fill="{c}" font-family="sans-serif">'
        '{a} vs {b}</text>'.format(x=left, c=TEXT_COLOR, a=model_a, b=model_b)
    )
    lines.append(
        '<text x="{x}" y="60" font-size="11" fill="{c}" font-family="sans-serif">'
        'Segment labels show share +/- 1 standard error when there is room.</text>'.format(
            x=left, c=TEXT_COLOR
        )
    )

    y0 = top + plot_height
    lines.append(
        '<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{c}" stroke-width="1.5"/>'.format(
            x1=left, x2=width - right, y=y0, c=AXIS_COLOR
        )
    )
    lines.append(
        '<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{c}" stroke-width="1.5"/>'.format(
            x=left, y1=top, y2=y0, c=AXIS_COLOR
        )
    )

    for tick in (0, 25, 50, 75, 100):
        y = top + plot_height - (tick / 100.0) * plot_height
        lines.append(
            '<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="#e2e8f0" stroke-width="1"/>'.format(
                x1=left, x2=width - right, y=y
            )
        )
        lines.append(
            '<text x="{x}" y="{y}" font-size="11" fill="{c}" font-family="sans-serif" text-anchor="end">{label}%</text>'.format(
                x=left - 8, y=y + 4, c=TEXT_COLOR, label=tick
            )
        )

    for idx, label in enumerate(labels):
        summary = summaries[idx]
        a_share = summary["model_a_share_all"] * 100.0
        b_share = summary["model_b_share_all"] * 100.0
        tie_share = summary["tie_share_all"] * 100.0
        unclear_share = summary["unclear_share_all"] * 100.0
        x = left + group_width * (idx + 0.5) - bar_width / 2.0
        current_bottom = y0
        segments = (
            (
                model_a,
                a_share,
                summary_sem(
                    summary, "model_a_share_all_sem", "model_a_wins", "total_items"
                )
                * 100.0,
                MODEL_A_COLOR,
                TEXT_ON_DARK_COLOR,
            ),
            (
                model_b,
                b_share,
                summary_sem(
                    summary, "model_b_share_all_sem", "model_b_wins", "total_items"
                )
                * 100.0,
                MODEL_B_COLOR,
                TEXT_ON_DARK_COLOR,
            ),
            (
                "tie",
                tie_share,
                summary_sem(summary, "tie_share_all_sem", "tie", "total_items")
                * 100.0,
                TIE_COLOR,
                TEXT_ON_DARK_COLOR,
            ),
            (
                "unclear",
                unclear_share,
                summary_sem(
                    summary, "unclear_share_all_sem", "unclear", "total_items"
                )
                * 100.0,
                UNCLEAR_COLOR,
                TEXT_COLOR,
            ),
        )
        for segment_label, share, sem, color, text_color in segments:
            height_px = (share / 100.0) * plot_height
            y = current_bottom - height_px
            lines.append(
                '<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}"><title>{title}</title></rect>'.format(
                    x=x,
                    y=y,
                    w=bar_width,
                    h=max(height_px, 0.0),
                    c=color,
                    title="{}: {} share {}% +/- {}%".format(
                        label,
                        segment_label,
                        int(round(share)),
                        int(round(sem)),
                    ),
                )
            )
            if height_px >= 22.0:
                lines.append(
                    '<text x="{x}" y="{y}" font-size="10" fill="{c}" font-family="sans-serif" text-anchor="middle">{label}</text>'.format(
                        x=x + bar_width / 2.0,
                        y=y + height_px / 2.0 + 3,
                        c=text_color,
                        label=format_percent_and_sem(share, sem),
                    )
                )
            current_bottom = y
        lines.append(
            '<text x="{x}" y="{y}" font-size="12" fill="{c}" font-family="sans-serif" text-anchor="middle">{label}</text>'.format(
                x=x + bar_width / 2.0, y=height - 45, c=TEXT_COLOR, label=label
            )
        )

    legend_y = height - 20
    legend_items = [
        (MODEL_A_COLOR, model_a),
        (MODEL_B_COLOR, model_b),
        (TIE_COLOR, "tie"),
        (UNCLEAR_COLOR, "unclear"),
    ]
    legend_x = left
    for color, label in legend_items:
        lines.append('<rect x="{x}" y="{y}" width="14" height="14" fill="{c}"/>'.format(x=legend_x, y=legend_y - 11, c=color))
        lines.append('<text x="{x}" y="{y}" font-size="12" fill="{c}" font-family="sans-serif">{label}</text>'.format(x=legend_x + 20, y=legend_y, c=TEXT_COLOR, label=label))
        legend_x += 150

    lines.append(svg_footer())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Plot forced-choice human annotation summaries."
    )
    parser.add_argument(
        "--summary-path",
        type=Path,
        required=True,
        help="Path to manual_label_raw_statistics_all_languages.json.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Directory where plot files should be written.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    summary_payload = json.loads(args.summary_path.read_text(encoding="utf-8"))
    win_rates_path = args.output_dir / "manual_label_decisive_win_rates_all_languages.svg"
    label_mix_path = args.output_dir / "manual_label_label_mix_all_languages.svg"
    make_decisive_win_rates_svg(summary_payload, win_rates_path)
    make_label_mix_svg(summary_payload, label_mix_path)
    print("wrote: {}".format(win_rates_path))
    print("wrote: {}".format(label_mix_path))


if __name__ == "__main__":
    main()

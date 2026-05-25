from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

ACTIVITIES = ("puzzles", "drawing", "music", "bookreading")
ACTIVITY_TO_LEVEL = {name: idx + 1 for idx, name in enumerate(ACTIVITIES)}
ACTIVITY_LEVEL_SPAN = max(len(ACTIVITIES) - 1, 1)


@dataclass
class VolunteerRecord:
    name: str
    activity: str


@dataclass
class SurveyData:
    industry: str
    phd_professional_count: int
    volunteers: list[VolunteerRecord]


def _read_non_empty(prompt: str, input_func: Callable[[str], str]) -> str:
    while True:
        value = input_func(prompt).strip()
        if value:
            return value
        print("Value cannot be empty. Please try again.")


def _read_non_negative_int(prompt: str, input_func: Callable[[str], str]) -> int:
    while True:
        raw_value = input_func(prompt).strip()
        try:
            value = int(raw_value)
        except ValueError:
            print("Please enter a valid integer.")
            continue
        if value < 0:
            print("Please enter a non-negative integer.")
            continue
        return value


def _read_activity(prompt: str, input_func: Callable[[str], str]) -> str:
    allowed = ", ".join(ACTIVITIES)
    while True:
        value = input_func(f"{prompt} ({allowed}): ").strip().lower()
        if value in ACTIVITY_TO_LEVEL:
            return value
        print(f"Invalid activity. Choose one of: {allowed}.")


def collect_survey_data(input_func: Callable[[str], str] | None = None) -> SurveyData:
    if input_func is None:
        input_func = input
    industry = _read_non_empty("Enter industry: ", input_func)
    phd_count = _read_non_negative_int("Enter number of professionals with a PhD: ", input_func)
    volunteer_count = _read_non_negative_int("Enter number of volunteers: ", input_func)

    volunteers: list[VolunteerRecord] = []
    for index in range(1, volunteer_count + 1):
        name = _read_non_empty(f"Enter volunteer #{index} name: ", input_func)
        activity = _read_activity(f"Enter volunteer #{index} art activity", input_func)
        volunteers.append(VolunteerRecord(name=name, activity=activity))

    return SurveyData(industry=industry, phd_professional_count=phd_count, volunteers=volunteers)


def _svg_axes(width: int, height: int, margin: int) -> str:
    x_axis = f'<line x1="{margin}" y1="{height - margin}" x2="{width - margin}" y2="{height - margin}" stroke="black" />'
    y_axis = f'<line x1="{margin}" y1="{margin}" x2="{margin}" y2="{height - margin}" stroke="black" />'
    return f"{x_axis}\n{y_axis}"


def _activity_tick_labels(width: int, height: int, margin: int) -> Iterable[str]:
    graph_height = height - (2 * margin)
    for activity, level in ACTIVITY_TO_LEVEL.items():
        y = height - margin - ((level - 1) * graph_height / ACTIVITY_LEVEL_SPAN)
        label = f'<text x="{margin - 10}" y="{y + 4:.1f}" text-anchor="end" font-size="12">{activity}</text>'
        tick = f'<line x1="{margin - 4}" y1="{y:.1f}" x2="{margin}" y2="{y:.1f}" stroke="black" />'
        yield tick
        yield label


def generate_svg_graph(data: SurveyData, output_path: str = "volunteer_activity_graph.svg") -> str:
    width, height, margin = 900, 500, 80
    chart_width = width - (2 * margin)
    chart_height = height - (2 * margin)
    volunteer_count = max(len(data.volunteers), 1)
    x_step = chart_width / volunteer_count

    point_elements: list[str] = []
    for index, volunteer in enumerate(data.volunteers):
        x = margin + ((index + 0.5) * x_step)
        y_level = ACTIVITY_TO_LEVEL[volunteer.activity]
        y = height - margin - ((y_level - 1) * chart_height / ACTIVITY_LEVEL_SPAN)
        point_elements.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="#2b7" />')
        point_elements.append(
            f'<text x="{x:.1f}" y="{height - margin + 20}" text-anchor="middle" font-size="12">{volunteer.name}</text>'
        )

    title = (
        f'Industry: {data.industry} | PhD professionals: {data.phd_professional_count}'
    )
    svg_content = "\n".join(
        [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
            '<rect width="100%" height="100%" fill="white" />',
            f'<text x="{width / 2}" y="32" text-anchor="middle" font-size="18" font-weight="bold">Volunteer Art Activities</text>',
            f'<text x="{width / 2}" y="56" text-anchor="middle" font-size="14">{title}</text>',
            _svg_axes(width, height, margin),
            *list(_activity_tick_labels(width, height, margin)),
            f'<text x="{width / 2}" y="{height - 20}" text-anchor="middle" font-size="14">Volunteer Name (X axis)</text>',
            '<text x="24" y="250" text-anchor="middle" font-size="14" transform="rotate(-90 24 250)">Art Activity (Y axis)</text>',
            *point_elements,
            '</svg>',
        ]
    )

    with open(output_path, "w", encoding="utf-8") as svg_file:
        svg_file.write(svg_content)

    return output_path


def main() -> None:
    survey_data = collect_survey_data()
    output_file = generate_svg_graph(survey_data)
    print(f"Graph generated: {output_file}")


if __name__ == "__main__":
    main()

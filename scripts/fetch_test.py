import pytest
from datetime import date

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from fetch import fetch_holiday, get_paper_urls


def test_get_paper_urls():
    urls = get_paper_urls(2024)
    assert len(urls) > 0
    assert all(url.startswith("https://") or url.startswith("http://") for url in urls)


def test_fetch_holiday():
    data = fetch_holiday(2024)
    assert "year" in data
    assert data["year"] == 2024
    assert "papers" in data
    assert "days" in data
    assert len(data["days"]) > 0

    first_day = data["days"][0]
    assert "name" in first_day
    assert "date" in first_day
    assert "isOffDay" in first_day
    assert isinstance(first_day["date"], date) or isinstance(first_day["date"], str)

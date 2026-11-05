"""Week 1 Day 3: Capture a Cricbuzz score using Playwright."""

import re
import sys
from pathlib import Path

from playwright.sync_api import Error, TimeoutError, sync_playwright


HOME_URL = "https://www.cricbuzz.com/"
LIVE_URL = "https://www.cricbuzz.com/live-cricket-scores/real-time"
SCREENSHOT = Path(__file__).with_name("score.png")

# A score usually looks like 156/4 or 156-4, optionally with overs.
# Inspect the actual Cricbuzz score element in DevTools for your assignment.
SCORE_PATTERN = re.compile(r"\b\d{1,3}\s*[/\-]\s*\d{1,2}(?:\s*\([^)]*\))?")


def capture_cricket_score(headless=False):
    print("Cricbuzz Assignment - Day 3")
    print("Opening Cricbuzz...")

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=headless)
            try:
                page = browser.new_page(viewport={"width": 1366, "height": 900})
                page.goto(HOME_URL, wait_until="domcontentloaded", timeout=30000)
                page.goto(LIVE_URL, wait_until="domcontentloaded", timeout=30000)

                # Playwright waits for the matching score to become visible.
                score_element = page.get_by_text(SCORE_PATTERN).first
                try:
                    score_element.wait_for(state="visible", timeout=15000)
                    print("\nCricket score:")
                    print(score_element.inner_text().strip())
                except TimeoutError:
                    print("No live score found. There may be no live match, or the page layout changed.")

                page.screenshot(path=str(SCREENSHOT), full_page=True)
                print(f"Screenshot saved: {SCREENSHOT}")
            finally:
                browser.close()
    except Error as exc:
        print(f"Playwright/browser error: {exc}")
        print("Check your internet connection and run: python -m playwright install chromium")


if __name__ == "__main__":
    capture_cricket_score(headless="--headless" in sys.argv)

from pathlib import Path

from lib.driver_builder import DriverBuilder

TEMP_ROOT = Path("../data")
url = ""


def main():
    driver_builder = DriverBuilder()
    driver = driver_builder.get_driver(
        download_location=str(TEMP_ROOT.resolve()), headless=True
    )
    driver.get(url)


if __name__ == "__main__":
    main()

from typing import Iterable, Optional, Union
import holidays
import pandas as pd
import numpy as np

def get_country_holidays(country: str, years: Optional[Union[int, Iterable[int]]] = None):
    """
    Helper function to get holidays for a country, with custom holidays for the US.

    Parameters
    ----------
        country : str
            Country code to retrieve country-specific holidays
        years : int or list of int
            Year or list of years to retrieve holidays for

    Returns
    -------
        dict
            Dictionary with holiday dates as keys and names as values
    """
    substitutions = {
        "TU": "TR",  # For compatibility with Turkey as "TU" cases.
        "USA": "US"  # Ensure "USA" is recognized as "US"
    }

    country = substitutions.get(country, country)
    if not hasattr(holidays, country):
        raise AttributeError(f"Holidays in {country} are not currently supported!")

    holiday_list = getattr(holidays, country)(years=years)
    
    # Add Black Friday and Cyber Monday for the United States
    if country == "US" and years is not None:
        # Ensure `years` is a list, even if a single year is provided
        if isinstance(years, (int, float)):
            years = [int(years)]
        elif isinstance(years, np.ndarray):
            years = years.tolist()

        for year in years:
            # Calculate Thanksgiving as the fourth Thursday in November
            thanksgiving = pd.Timestamp(f"{year}-11-01") + pd.DateOffset(weeks=3) + pd.offsets.Week(weekday=3)
            
            # Black Friday is the day after Thanksgiving
            black_friday = thanksgiving + pd.Timedelta(days=1)
            holiday_list[black_friday.to_pydatetime().date()] = "Black Friday"

            # Cyber Monday is three days after Black Friday
            cyber_monday = black_friday + pd.Timedelta(days=3)
            holiday_list[cyber_monday.to_pydatetime().date()] = "Cyber Monday"

    # Convert the holiday list to a dictionary with date objects as keys and names as values
    holiday_dict = {date_: name for date_, name in holiday_list.items()}
    return holiday_dict

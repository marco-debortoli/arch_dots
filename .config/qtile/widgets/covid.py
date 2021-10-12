from datetime import datetime

from urllib.error import URLError
from urllib.request import Request, urlopen

from libqtile.widget import base


class CovidCaseCount(base.ThreadPoolText):
    """
    A widget that will fetch and display COVID case counts for a provided
    US state using the NYTimes GitHub data source
    """
    orientations = base.ORIENTATION_HORIZONTAL

    defaults = [
        ("state", "Massachusetts", "The state that the widget will render data for"),
        (
            "ignore_weekend", True,
            "Whether or not the state returns data on weekends."
            "If True, then if the case count on a weekend is zero, the previous weekday will be used"
        ),
        ("trend_lookback_days", 14, "The number of days to look back to calculate the trend"),
        ("increasing_case_colour", None, "The text colour when the trend of cases is increasing"),
        ("decreasing_case_colour", None, "The text colour when the trend of cases is descreasing"),
        ("fail_text", "?", "The text to return if the request for data fails")
    ]

    DATA_SOURCE = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/rolling-averages/us-states.csv"

    def __init__(self, **config):
        base.ThreadPoolText.__init__(self, "", **config)
        self.add_defaults(CovidCaseCount.defaults)
        self.add_callbacks({'Button1': self.poll})

    def fetch_data(self):
        """
        Fetch the data from our DATA_SOURCE URL and return the raw body of the response
        """
        req = Request(self.DATA_SOURCE, None, {'Content-Type': 'text/csv'})

        try:
            res = urlopen(req)
        except URLError:
            # We either have no network, or the data source no longer exists
            return None

        charset = res.headers.get_content_charset()

        # If the response is not a 200, then we should return None
        if res.code != 200:
            return None

        body = res.read()

        if charset:
            body = body.decode(charset)

        return body

    def parse_case_counts(self, raw_csv):
        """
        Given the raw CSV body from the request, return the data for the state sorted by date
        as a list
        """
        # Ignore the first line
        csv_lines = raw_csv.split("\n")[1:]

        parsed = list()

        # Filter by state and parse
        for csv_line in csv_lines:
            split_line = csv_line.split(",")

            state = split_line[2]

            if state.lower() == self.state.lower():
                # (date, case count, rolling average)
                parsed.append(
                    (split_line[0], int(split_line[3]), float(split_line[4]))
                )

        return parsed

    def poll(self):
        body = self.fetch_data()

        if body is None:
            return self.fail_text

        # Parse the data to return the data for our state
        state_data = self.parse_case_counts(body)

        if not state_data:
            return self.fail_text

        # Get the data from the last day
        last_day = state_data[-1]
        case_count = last_day[1]
        case_avg = last_day[2]

        if self.ignore_weekend:
            last_date = datetime.strptime(last_day[0], "%Y-%m-%d")
            weekday = last_date.weekday()
            
            if case_count == 0 and weekday in [5, 6]:
                case_count = state_data[-1 - (weekday - 4)][1]

        # Get the average X number of days before
        lookback_average = state_data[-self.trend_lookback_days][2]

        if case_avg > lookback_average:
            trend = "\uf062"

            if self.increasing_case_colour:
                self.foreground = self.increasing_case_colour
        else:
            trend = "\uf063"
            
            if self.decreasing_case_colour:
                self.foreground = self.decreasing_case_colour

        return f"\uf7df  {case_count} {trend}"
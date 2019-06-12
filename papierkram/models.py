from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class TimeBooking:
    start: datetime
    end: datetime
    billable: bool
    customer: str
    project: str
    task: str
    service: str
    comment: str

    @property
    def duration(self) -> timedelta:
        return self.end - self.start

    @classmethod
    def from_csv(cls, record):
        return cls(
            datetime.strptime(
                "{} {}".format(record["Datum"], record["Beginn"]), "%d.%m.%Y %H:%M"
            ),
            datetime.strptime(
                "{} {}".format(record["Datum"], record["Ende"]), "%d.%m.%Y %H:%M"
            ),
            record["Nicht-Abrechenbar"] == "nein",
            record["Kunde"],
            record["Projekt"],
            record["Aufgabe"],
            record["Dienstleistung"],
            record["Kommentar"],
        )

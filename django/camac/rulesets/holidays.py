from datetime import date

from holidays.countries import CH


class AargauAdministrationHolidays(CH):
    """Holiday class representing all holidays in the administration of Kt. AG."""

    def __init__(self, *args, **kwargs):
        kwargs["subdiv"] = "AG"
        kwargs["language"] = "de"

        super().__init__(*args, **kwargs)

    def _populate(self, year: int) -> None:
        super()._populate(year)

        self.remove_non_public_holidays()
        self.add_administration_holidays(year)

    def remove_non_public_holidays(self) -> None:
        """Remove non public holidays for the administration of Kt. AG.

        For more information please consult the column "Aarau" in this list:
        https://www.ag.ch/media/kanton-aargau/dvi/dokumente/awa/awa/arbeitnehmerschutz-im-betrieb/feiertage.pdf
        """

        self.pop_named("Tag der Arbeit")
        self.pop_named("Fronleichnam")
        self.pop_named("Mariä Himmelfahrt")
        self.pop_named("Allerheiligen")
        self.pop_named("Mariä Empfängnis")

    def add_administration_holidays(self, year: int) -> None:
        """Add administration holidays.

        The administration in Kt. AG has fixed holidays between Christmas Day
        (25.12) and Berchtold's Day (02.01). Since Christmas Day, New Year's Day
        and Berchtold's Day are public holidays anyways we can ignore them here.
        """
        administration_holidays = [date(year, 12, day) for day in range(27, 32)]

        for holiday in administration_holidays:
            self[holiday] = "Betriebsferien"

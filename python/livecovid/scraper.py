from requests_html import HTMLSession
import json

BASEURL = "https://covidlive.com.au/report/daily-cases"
STATES = {
    "sa": "South Australia",
    "wa": "Western Australia",
    "nsw": "New South Wales",
    "vic": "Victoria",
    "tas": "Tasmania",
    "nt": "Northern Territory",
    "act": "Australian Capital Territory",
}


class CovidScraper:
    def get_covid_numbers(self, state: str, details: bool = False):
        retval = {}
        state = state or "sa"  # default to sa
        retval["state"] = STATES[state]

        try:
            # Start HTML session and begin scraping BASEURL
            session = HTMLSession()
            STATEURL = f"{BASEURL}/{state}"

            resp = session.get(STATEURL)
            meta = {"code": resp.status_code, "reason": resp.reason}
            retval["meta"] = meta

            if resp.status_code != 200:
                return json.loads(retval)

            # Extract numbers
            retval["payload"] = self._get_payload(resp)

        except Exception as exc:
            retval["exception"] = exc

        return json.loads(retval)

    def _get_payload(self, rsp):
        payload = {}
        cases = rsp.html.find("section.DAILY-CASES.STD-3")
        dates = cases[0].find("td.COL1.DATE")
        numbers = cases[0].find("td.COL2.NEW")
        zipped = zip(dates, numbers)

        for item in zipped:
            payload[item[0].text] = item[1].text

        return payload


if __name__ == "__main__":
    cs = CovidScraper()
    print(cs.get_covid_numbers("sa"))

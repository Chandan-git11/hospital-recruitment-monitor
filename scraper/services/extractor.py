from ..parsers.apollo_parser import ApolloParser
from ..parsers.fortis_parser import FortisParser
from ..parsers.generic_parser import GenericParser
from ..parsers.max_parser import MaxParser
from ..parsers.manipal_parser import ManipalParser


class JobExtractor:

    def __init__(self) -> None:

        self.parsers = {
    "apollo": ApolloParser(),
    "fortis": FortisParser(),
    "manipal": ManipalParser(),
}
    def extract(
        self,
        html: str,
        hospital_name: str
    ) -> list[dict]:

        hospital = hospital_name.strip().lower()

        # Fortis uses API, not HTML parsing
        if hospital == "fortis":
            return FortisParser().fetch_jobs()

        parser = self.parsers.get(
            hospital,
            GenericParser()
        )

        return parser.parse(
            html,
            hospital_name
        )
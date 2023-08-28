from pprint import pformat
import yaml

from schema.model import MadeSchema


class MadeController:
    def run(self) -> None:
        with open("made-file.yaml") as made_file:
            made_config = yaml.safe_load(made_file)

        print(made_config)
        schema = MadeSchema.from_dict(made_config)
        print(f"schema: {pformat(schema)}")

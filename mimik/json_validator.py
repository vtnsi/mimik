import json
import jsonschema


class JsonValidator:
    def __init__(self):
        """
        The constructor which sets the schema for the JSON
        """
        self.schema = {
            "type": "object",
            "patternProperties": {
                "^[A-Za-z0-9 -_]+": {
                    "type": "object",
                    "patternProperties": {
                        "^[A-Za-z0-9 -_]+": {
                            "type": "object",
                            "properties": {
                                "attributes": {
                                    "type": "object",
                                    "properties": {
                                        "task": {"type": "string"},
                                        "task_arguments": {"type": "object"},
                                        "system_name": {"type": "string",}
                                    },
                                    "additionalProperties": True
                                },
                                "connected_components": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                }
                            }
                        }
                    }                   
                }
            },
            "additionalProperties": False
        }

    def validate_config(self, config_file: str, silent: bool):
        """
        Validates a JSON config file containing killweb information
        
        Parameters:
            config_file (str): The config file to validate
            silent (bool): True if MIMIK is running in silent mode
        
        Returns:
            True if the config file had valid JSON schema
        """
        with open(config_file, 'r') as file:
            data = json.load(file)
            try:
                jsonschema.validate(instance=data, schema=self.schema)
                if not silent:
                    print("JSON data is valid.")
            except jsonschema.exceptions.ValidationError as e:
                print(f"JSON data is invalid: {e.message}")
                raise e
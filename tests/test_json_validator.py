import pytest
import os
import jsonschema
from mimik.json_validator import JsonValidator


class TestJsonValidator:
    """
    Creates a test class for the JsonValidator class
    """

    @pytest.fixture
    def test_json_validator(self):
        """
        Returns a JsonValidator object

        Returns:
            JsonValidator: A JsonValidator object to test with
        """
        return JsonValidator()

    def test_validate_config(self, test_json_validator, mocker):
        """
        Tests the JsonValidator's validate_config method

        Args:
            test_json_validator (JsonValidator): The JsonValidator for test provided by the fixture
        """
        mock_print = mocker.patch("builtins.print")
        test_json_validator.validate_config(os.path.join("tests", "test_configs", "test_json.json"), False)
        mock_print.assert_called_with("JSON data is valid.")

        with pytest.raises(jsonschema.exceptions.ValidationError):
            test_json_validator.validate_config(os.path.join("tests", "test_configs", "invalid_config.json"), False)
            mock_print.assert_called_with("JSON data is invalid:")
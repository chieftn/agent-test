class Secrets:
     def __init__(self, values: dict[str], sensitive_data_fields: list[str]):
        self.values = values
        self.sensitive_data = dict[str]()

        sensitive_data_field_set = set(sensitive_data_fields)
        for key, value in self.values.items():
            if (key in sensitive_data_field_set):
                self.sensitive_data[key] = value

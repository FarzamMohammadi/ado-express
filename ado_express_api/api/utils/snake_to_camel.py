class SnakeToCamelCaseConverter:
    @staticmethod
    def _snake_to_camel(snake_str):
        components = snake_str.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])

    @staticmethod
    def convert(obj):
        # Handle custom objects by converting them to dictionaries
        if hasattr(obj, "__dict__"):
            obj = obj.__dict__

        if isinstance(obj, dict):
            camel_case_obj = {}
            for key, value in obj.items():
                camel_case_key = SnakeToCamelCaseConverter._snake_to_camel(key)
                camel_case_obj[camel_case_key] = SnakeToCamelCaseConverter.convert(value)
            return camel_case_obj
        elif isinstance(obj, list):
            return [SnakeToCamelCaseConverter.convert(item) for item in obj]
        else:
            return obj
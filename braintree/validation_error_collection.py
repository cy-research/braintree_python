from braintree.validation_error import ValidationError

class ValidationErrorCollection:
    def __init__(self, data):
        self.errors = [ValidationError(error) for error in data["errors"]]
        self.nested_errors = self.__nested_errors(data)
        self.deep_size = self.__deep_size()
        self.size = len(self.errors)

    def for_object(self, nested_key):
        return self.nested_errors[nested_key]

    def on(self, attribute):
        return [error for error in self.errors if error.attribute == attribute]

    def __deep_size(self):
        size = len(self.errors)
        for error in self.nested_errors.values():
            size += error.deep_size
        return size

    def __getitem__(self, index):
        return self.errors[index]

    def __nested_errors(self, data):
        nested_errors = {}
        for key in data.keys():
            if key == "errors": continue
            nested_errors[key] = ValidationErrorCollection(data[key])
        return nested_errors

class FileValidationError(Exception):
    def __init__(self, message="Invalid file format. Only CSV and XLSX files are allowed."):
        self.message = message
        super().__init__(self.message)

class DataProcessingError(Exception):
    def __init__(self, message="Error processing data."):
        self.message = message
        super().__init__(self.message)
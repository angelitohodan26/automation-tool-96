import json
import logging

class DataProcessor:
    def __init__(self, data):
        self.data = data
        self.logger = logging.getLogger(__name__)

    def validate_data(self):
        if not isinstance(self.data, dict):
            self.logger.error('Data must be a dictionary')
            return False
        if 'timestamp' not in self.data:
            self.logger.error('Missing timestamp in data')
            return False
        return True

    def process_data(self):
        if not self.validate_data():
            return {'error': 'Invalid data'}
        try:
            # Simulate processing
            result = {'status': 'processed', 'original_data': self.data}
            return result
        except Exception as e:
            self.logger.exception('Error processing data')
            return {'error': str(e)}

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    sample_data = {'timestamp': '2023-10-01T12:00:00'}
    processor = DataProcessor(sample_data)
    response = processor.process_data()
    print(json.dumps(response, indent=2))
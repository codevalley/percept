import time

class Snowflake53:
    def __init__(self, datacenter_id, worker_id):
        self.datacenter_id = datacenter_id
        self.worker_id = worker_id
        self.sequence = 0
        self.last_timestamp = -1

    def generate(self):
        timestamp = int(time.time() * 1000)  # Current time in milliseconds

        if timestamp < self.last_timestamp:
            raise ValueError("Clock moved backwards")

        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & 0xFF  # 8 bits for sequence
            if self.sequence == 0:
                timestamp = self.wait_next_millis(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        # Reduce from 64 bits to 53 bits
        id = ((timestamp & 0x1FFFFFFFFFF) << 12) | \
             ((self.datacenter_id & 0x1F) << 7) | \
             ((self.worker_id & 0x1F) << 2) | \
             (self.sequence & 0x3)

        return id

    def wait_next_millis(self, last_timestamp):
        timestamp = int(time.time() * 1000)
        while timestamp <= last_timestamp:
            timestamp = int(time.time() * 1000)
        return timestamp

# Usage
#generator = Snowflake53(datacenter_id=1, worker_id=1)
#id = generator.generate()
#print(id)  # This will print a number that fits within JavaScript's safe integer range
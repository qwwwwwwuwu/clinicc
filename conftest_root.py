# clinic/conftest_root.py

import sys
import io

class ProtectedStderr(io.StringIO):
    def close(self):
        pass

    def write(self, msg):
        try:
            return super().write(msg)
        except ValueError:
            return 0

    def flush(self):
        pass

# Защита еще до всего
sys.stderr = ProtectedStderr()

# run_pytest.py

import sys
import io
import pytest

# Глобально защищаем sys.stderr от закрытия
class ProtectedStderr(io.StringIO):
    def close(self):
        pass

    def write(self, msg):
        try:
            return super().write(msg)
        except Exception:
            return 0

    def flush(self):
        pass

sys.stderr = ProtectedStderr()

# Запуск pytest
sys.exit(pytest.main())

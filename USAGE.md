# 📖 دليل الاستخدام السريع

## التثبيت

```bash
# استنساخ المستودع
git clone https://github.com/nlkm8850-collab/Moon-carag.git
cd Moon-carag

# تثبيت المتطلبات
pip install -r requirements.txt
```

## أمثلة الاستخدام

### 1. TokenManager
```python
from tools.token_manager import TokenManager

manager = TokenManager(model="gpt-3.5-turbo")
token_count = manager.count_tokens("Hello World")
print(f"Tokens: {token_count}")
```

### 2. RateLimiter
```python
from tools.rate_limiter import RateLimiter

limiter = RateLimiter(requests_per_minute=60)
if limiter.is_allowed():
    make_api_call()
```

### 3. RetryHandler
```python
from tools.retry_handler import RetryHandler

handler = RetryHandler(max_retries=3)
result = handler.execute(risky_function)
```

### 4. APICache
```python
from tools.api_cache import APICache

cache = APICache(ttl=3600)
data = cache.get_or_fetch("key", api_function, arg1, arg2)
```

### 5. ErrorHandler
```python
from tools.error_handler import ErrorHandler

handler = ErrorHandler()
try:
    risky_operation()
except Exception as e:
    handler.handle(e)
```

### 6. Logger
```python
from tools.logger_system import LoggerSetup

logger = LoggerSetup.setup("my_app")
logger.info("تطبيقي بدأ")
logger.error("حدث خطأ", exc_info=True)
```

### 7. Monitor
```python
from tools.monitor import PerformanceMonitor

monitor = PerformanceMonitor()
monitor.record_operation("api_call", 0.5)
stats = monitor.get_stats()
```

### 8. Validator
```python
from tools.validator import Validator

validator = Validator()
valid, error = validator.validate(data)
```

### 9. BatchProcessor
```python
from tools.batch_processor import BatchProcessor

processor = BatchProcessor(batch_size=10)
results = processor.process(items, processor_func)
```

### 10. HealthChecker
```python
from tools.health_check import HealthChecker

checker = HealthChecker()
health = checker.run_checks()
```

### 11. ConfigManager
```python
from tools.config_manager import ConfigManager

config = ConfigManager("config.json")
api_key = config.get("api.key")
```

### 12. DataSanitizer
```python
from tools.data_sanitizer import DataSanitizer

sanitizer = DataSanitizer()
clean_text = sanitizer.sanitize_text(sensitive_text)
```

## أفضل الممارسات

1. **استخدم TokenManager** لجميع عمليات API
2. **طبق RateLimiter** لتجنب حد المعدل
3. **استخدم RetryHandler** للأخطاء المؤقتة
4. **فعّل APICache** لتوفير الموارد
5. **طبق ErrorHandler** لمعالجة موحدة
6. **استخدم Logger** بدل print()
7. **راقب الأداء** مع Monitor
8. **تحقق من البيانات** مع Validator
9. **عالج الدفعات** مع BatchProcessor
10. **راقب الصحة** مع HealthCheck
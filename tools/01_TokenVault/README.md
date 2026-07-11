# 🔐 TokenVault - Smart Token Management

إدارة التوكنز في APIs الذكاء الاصطناعي بذكاء وأمان

## المشكلة
تجاوز حد التوكنز = فشل الطلبات وتكاليف إضافية

## الحل
- ✅ حساب دقيق للتوكنز
- ✅ تقسيم تلقائي للنصوص الطويلة
- ✅ مراقبة الاستهلاك
- ✅ دعم نماذج متعددة

## الاستخدام
```python
from token_manager import TokenManager
manager = TokenManager(model="gpt-4")
count = manager.count_tokens("مرحبا")
```
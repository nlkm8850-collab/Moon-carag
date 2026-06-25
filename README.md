# Moon-carag
تطوير برمجيات ومنها برمجة بوتات الية

## Pemini - مساعد الذكاء الاصطناعي

### نبذة عن Pemini
Pemini هو تطبيق ذكاء اصطناعي متقدم مصمم لمساعدة المطورين والمبرمجين في كتابة وتحسين أكوادهم البرمجية.

### المميزات الرئيسية:
- ✨ **كتابة الأكواد البرمجية**: يمكن لـ Pemini كتابة أكواد احترافية بلغات برمجة مختلفة
- 🐛 **تصحيح الأخطاء**: اكتشاف وإصلاح الأخطاء البرمجية
- 📚 **شرح الأكواد**: فهم وشرح الأكواد المعقدة
- ⚡ **تحسين الأداء**: اقتراحات لتحسين كفاءة البرامج
- 🔧 **دعم لغات متعددة**: Python, JavaScript, Java, C++, C#, وغيرها

### طرق التحميل:

#### 1. نسخة الويب
الوصول المباشر عبر المتصفح للاستخدام الفوري بدون تثبيت

#### 2. نسخة التطبيق للهواتف (.APK)
تحميل التطبيق على أجهزة الهاتف الذكية بنظام Android

**خطوات التحميل:**
1. قم بتحميل ملف APK من القسم المخصص
2. انتقل إلى إعدادات الهاتف > الأمان > السماح بتثبيت من مصادر غير معروفة
3. افتح ملف APK وانقر على تثبيت
4. افتح التطبيق واستمتع بمميزات Pemini

### المتطلبات:
- **للنسخة الويب**: متصفح حديث متصل بالإنترنت
- **للنسخة .APK**: أجهزة Android 8.0 أو أحدث

### البدء السريع:
```
1. اختر اللغة البرمجية المطلوبة
2. اكتب طلبك بالعربية أو الإنجليزية
3. اترك المجال لـ Pemini ليقوم بالعمل
4. انسخ الكود وكن مطوراً احترافياً
```

---

## 🛠️ أداة Pemini

### Pemini 0.7 - أداة التحليل والتطوير المتقدمة

**Pemini 0.7** هي أداة قوية وخفيفة الوزن مصممة خصيصاً للعمل على **Termux** وأي بيئة سطر أوامر Linux. توفر تجربة برمجية متكاملة.

### المميزات الأساسية:
- 🔍 **تحقق شامل من الأكواد** - فحص الأخطاء النحوية والمنطقية
- 💻 **دعم جميع لغات البرمجة**:
  - Python 🐍
  - JavaScript/Node.js 📜
  - Java ☕
  - C/C++ 🔧
  - C# 🟦
  - PHP 🐘
  - Ruby 💎
  - Go 🐹
  - Rust 🦀
  - TypeScript 📘
  - وغيرها...
- 🎯 **تحليل الأخطاء** - تشخيص دقيق للمشاكل مع اقتراحات للحل
- ⚡ **أداء سريع** - معالجة فورية للأكواد
- 📊 **تقارير تفصيلية** - عرض شامل للنتائج والإحصائيات
- 🔐 **آمن وموثوق** - لا يحتاج لاتصال بالإنترنت للعمل الأساسي
- 🎨 **واجهة ملونة** - عرض احترافي للنتائج

### التثبيت على Termux:

#### الخطوة 1: تحديث النظام
```bash
apt update && apt upgrade -y
```

#### الخطوة 2: تثبيت المتطلبات
```bash
apt install git python python-pip nodejs -y
```

#### الخطوة 3: استنساخ المشروع من GitHub
```bash
git clone https://github.com/nlkm8850-collab/Moon-carag.git
cd Moon-carag/pemini-0.7
```

#### الخطوة 4: تثبيت المتطلبات الخاصة
```bash
pip install -r requirements.txt
```

#### الخطوة 5: منح صلاحيات التنفيذ
```bash
chmod +x pemini.py
chmod +x pemini
```

### طرق الاستخدام:

#### 1. التحقق من ملف Python
```bash
./pemini check file.py
# أو
python pemini.py check file.py
```

#### 2. التحقق من ملف JavaScript
```bash
./pemini check script.js
```

#### 3. التحقق من جميع الملفات في المجلد
```bash
./pemini check --recursive .
```

#### 4. تقرير تفصيلي
```bash
./pemini check file.js --verbose
```

#### 5. عرض الاقتراحات والحلول
```bash
./pemini suggest file.py
```

#### 6. إصلاح تلقائي للأكواد
```bash
./pemini fix file.py --auto
```

### أمثلة على الاستخدام:

**مثال 1: فحص ملف Python**
```bash
$ ./pemini check app.py
┌─────────────────────────────────────┐
│     تقرير التحليل - Pemini 0.7      │
└─────────────────────────────────────┘
ملف: app.py
الحالة: ✓ نظيف (مع تحذيرات)
الأخطاء: 0
التحذيرات: 2
```

**مثال 2: فحص ملف JavaScript مع اقتراحات**
```bash
$ ./pemini suggest index.js
الاقتراحات:
✓ استخدم const بدلاً من var
✓ أضف معالجة للأخطاء في الدالة
```

### المميزات المتقدمة:

- 📈 **تحليل الأداء** - معلومات عن تعقيد الخوارزمية
- 🔗 **كشف التبعيات** - عرض جميع المكتبات المستخدمة
- 🐛 **تتبع الأخطاء** - معرفة موقع الخطأ بدقة
- 🎓 **شرح الأخطاء** - توضيح لماذا حدث الخطأ

### الملفات المتضمنة:

```
pemini-0.7/
├── pemini              (ملف تنفيذي رئيسي)
├── pemini.py           (كود Python الرئيسي)
├── requirements.txt    (المكتبات المطلوبة)
├── config.json         (إعدادات التكوين)
├── analyzers/          (أدوات التحليل)
│   ├── python_analyzer.py
│   ├── js_analyzer.py
│   ├── java_analyzer.py
│   └── cpp_analyzer.py
├── reporters/          (أدوات التقرير)
│   ├── console_reporter.py
│   └── json_reporter.py
└── README.md           (التوثيق الكامل)
```

### المتطلبات الأساسية:

```
Python 3.8+
Node.js 12+
Git
RAM: 512 MB (الحد الأدنى)
مساحة تخزين: 100 MB
```

### رابط التحميل من GitHub:

🔗 **[Pemini 0.7 على GitHub](https://github.com/nlkm8850-collab/Moon-carag/releases/download/pemini-0.7/pemini-0.7.tar.gz)**

أو باستخدام الأمر:
```bash
wget https://github.com/nlkm8850-collab/Moon-carag/releases/download/pemini-0.7/pemini-0.7.tar.gz
tar -xzf pemini-0.7.tar.gz
cd pemini-0.7
pip install -r requirements.txt
```

### الدعم والمساعدة:

إذا واجهت أي مشاكل:
- 📖 اقرأ [التوثيق الكامل](https://github.com/nlkm8850-collab/Moon-carag/wiki/Pemini-0.7)
- 💬 [افتح issue جديد](https://github.com/nlkm8850-collab/Moon-carag/issues)
- 🤝 ساهم في تطوير المشروع

### الإصدارات السابقة:

- **Pemini 0.5** - الإصدار الأول
- **Pemini 0.6** - إضافة دعم لغات جديدة
- **Pemini 0.7** - الإصدار الحالي (محسّن وأسرع) ⭐

---

## 📚 برمجة 0.1 - أداة تعليم البرمجة التفاعلية

### نبذة عن برمجة 0.1
**برمجة 0.1** هي أداة تعليمية متخصصة لتعلم البرمجة بطريقة تفاعلية وممتعة. مصممة للعمل على **Termux** و**Linux** بسهولة، توفر دروساً عملية وتطبيقية لجميع مستويات المبتدئين.

### المميزات الرئيسية:
- 🎓 **دروس تفاعلية** - شروحات مفصلة لأساسيات البرمجة
- 💡 **أمثلة عملية** - أمثلة حقيقية قابلة للتنفيذ
- 🏆 **تحديات برمجية** - مشاكل وتحديات لتطبيق ما تعلمته
- 🐍 **دعم لغات متعددة**:
  - Python 🐍 (مبتدئ إلى متقدم)
  - JavaScript 📜 (من الأساسيات إلى DOM)
  - Java ☕ (البرمجة كائنية التوجه)
  - C/C++ 🔧 (الخوارزميات والبنى)
  - SQL 🗄️ (قواعد البيانات)
- 📊 **تتبع التقدم** - معرفة مستواك والدروس المتبقية
- 🔍 **تصحيح فوري** - تعليقات فورية على إجاباتك
- 🌍 **محتوى عربي وإنجليزي** - تعلم بلغتك المفضلة

### التثبيت على Termux:

#### الخطوة 1: تحديث النظام
```bash
apt update && apt upgrade -y
```

#### الخطوة 2: تثبيت المتطلبات الأساسية
```bash
apt install git python python-pip curl wget -y
```

#### الخطوة 3: استنساخ المشروع
```bash
git clone https://github.com/nlkm8850-collab/Moon-carag.git
cd Moon-carag/programming-0.1
```

#### الخطوة 4: تثبيت متطلبات Python
```bash
pip install -r requirements.txt
```

#### الخطوة 5: منح صلاحيات التنفيذ
```bash
chmod +x programming-0.1
chmod +x main.py
```

### التثبيت على Linux:

#### الخطوة 1: تحديث النظام
```bash
sudo apt update && sudo apt upgrade -y
```

#### الخطوة 2: تثبيت المتطلبات
```bash
sudo apt install git python3 python3-pip curl -y
```

#### الخطوة 3: استنساخ المشروع
```bash
git clone https://github.com/nlkm8850-collab/Moon-carag.git
cd Moon-carag/programming-0.1
```

#### الخطوة 4: تثبيت المكتبات
```bash
sudo pip3 install -r requirements.txt
```

#### الخطوة 5: منح الصلاحيات
```bash
sudo chmod +x programming-0.1
sudo chmod +x main.py
```

### طرق الاستخدام:

#### 1. عرض الدروس المتاحة
```bash
./programming-0.1 --list
# أو
python main.py --list
```

#### 2. بدء درس معين
```bash
./programming-0.1 --lesson python-basics
```

#### 3. حل تحدي برمجي
```bash
./programming-0.1 --challenge challenge-01
```

#### 4. عرض إحصائياتك
```bash
./programming-0.1 --stats
```

#### 5. اختبر معلوماتك
```bash
./programming-0.1 --quiz python
```

#### 6. اطلب شرحاً لموضوع معين
```bash
./programming-0.1 --explain "loops in python"
```

### أمثلة على الاستخدام:

**مثال 1: بدء درس Python للمبتدئين**
```bash
$ ./programming-0.1 --lesson python-basics
╔═══════════════════════════════════════╗
║      برمجة 0.1 - أداة التعليم         ║
╚═══════════════════════════════════════╝

📚 الدرس: أساسيات Python
⏱️ المدة: 15 دقيقة

📖 المحتوى:
1. مقدمة عن Python
2. المتغيرات والأنواع
3. العمليات الحسابية
4. الطباعة على الشاشة

💡 مثال عملي:
print("مرحباً بك في عالم البرمجة!")
```

**مثال 2: حل تحدي برمجي**
```bash
$ ./programming-0.1 --challenge sum-array
🎯 التحدي: أوجد مجموع عناصر المصفوفة

المشكلة:
اكتب برنامج يجمع جميع الأرقام في قائمة

📝 الحل المقترح:
numbers = [1, 2, 3, 4, 5]
total = sum(numbers)
print(total)

✅ تم التحقق: الحل صحيح!
🏆 +10 نقاط
```

### المحتوى التعليمي:

```
Lessons/
├── Python/
│   ├── 01-basics.md
│   ├── 02-variables.md
│   ├── 03-conditionals.md
│   ├── 04-loops.md
│   ├── 05-functions.md
│   └── 06-projects.md
├── JavaScript/
│   ├── 01-introduction.md
│   ├── 02-variables.md
│   └── 03-dom.md
├── Java/
│   ├── 01-oop-basics.md
│   └── 02-classes.md
└── Challenges/
    ├── beginner/
    ├── intermediate/
    └── advanced/
```

### الملفات المتضمنة:

```
programming-0.1/
├── main.py              (البرنامج الرئيسي)
├── programming-0.1      (ملف تنفيذي)
├── requirements.txt     (المكتبات المطلوبة)
├── config.json          (الإعدادات)
├── lessons/             (الدروس التعليمية)
├── challenges/          (التحديات البرمجية)
├── database/            (قاعدة بيانات التقدم)
└── templates/           (النماذج والقوائم)
```

### المتطلبات:

```
Python 3.7+
Git
نظام التشغيل: Termux أو Linux
مساحة التخزين: 50 MB
RAM: 256 MB (الحد الأدنى)
```

### الوصول السريع:

🔗 **[برمجة 0.1 على GitHub](https://github.com/nlkm8850-collab/Moon-carag/releases/download/programming-0.1/programming-0.1.tar.gz)**

أو عبر:
```bash
wget https://github.com/nlkm8850-collab/Moon-carag/releases/download/programming-0.1/programming-0.1.tar.gz
tar -xzf programming-0.1.tar.gz
cd programming-0.1
pip install -r requirements.txt
./programming-0.1 --help
```

### مستويات التعلم:

- 🟢 **مبتدئ** - من الصفر إلى الدوال الأساسية
- 🟡 **متوسط** - البرمجة كائنية التوجه والمكتبات
- 🔴 **متقدم** - الخوارزميات والبنى المعقدة

### نصائح للاستفادة القصوى:

1. 📖 ابدأ بالدروس الأساسية قبل التحديات
2. ✍️ اكتب الكود بنفسك لا تنسخها
3. 🔄 كرر الأمثلة عدة مرات حتى تتقنها
4. 🎯 انتقل للتحديات بعد فهم كل درس
5. 📊 راقب تقدمك من خلال الإحصائيات

### الدعم والمساعدة:

- 📚 [التوثيق الكامل](https://github.com/nlkm8850-collab/Moon-carag/wiki/Programming-0.1)
- 💬 [افتح issue جديد](https://github.com/nlkm8850-collab/Moon-carag/issues)
- 🤝 ساهم بدرس أو تحدي جديد

---

*Moon-carag: منصتك الموثوقة لتطوير البرمجيات والتعليم الذاتي*

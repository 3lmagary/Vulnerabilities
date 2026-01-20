# شرح: Access Control (التحكم في الوصول) و Privilege Escalation

> هدف الملف: شرح مركز، عملي، ومنظّم يساعدك تحل الـ labs المتعلقة بـ Access Control and Privilege Escalation بدون تفاصيلٍ تضيّعك.

---
#### <mark style="background: #D2B3FFA6;">البدايه يوم 15-10-2025</mark>

## 1. تعريف سريع
- **Authentication**: إثبات هوية المستخدم (login).
- **Session management**: متابعة الطلبات لنفس المستخدم (كوكي، توكن).
- **Access control**: تحديد ما إذا كان هذا المستخدم مخوّلًا لعمل فعل أو الوصول لمورد.

**Broken access control** = أي حالة يقدر فيها مستخدم يقوم بإجراء أو يحصل على بيانات ليس من المفترض أن يستطيعها.

---

## 2. أنواع التحكم (بإيجاز)
- **عمودي (Vertical)**: ترقية إلى صلاحيات أعلى (user → admin).
- **أفقي (Horizontal)**: الوصول لبيانات مستخدم آخر (user A → بيانات user B).
- **سياقي (Context-dependent)**: يعتمد على حالة التطبيق أو ترتيب الخطوات.

---

## 3. أمثلة شائعة للمشاكل (مع طريقة الاختبار السريعة)
- **Unprotected functionality**: رابط /admin متاح بدون تحقق.
  - اختبار: افتح المسار مباشرة كـ user عادي.
- **Security-by-obscurity (unpredictable URL)**: مسار مُخفي لكن ظاهر في جافاسكربت أو robots.txt.
  - اختبار: افحص HTML، JS، robots.txt، sitemap.
- **Parameter-based access control (role in param/cookie/hidden field)**
  - اختبار: عدّل param `role=true` أو cookie وقم بطلب.
- **IDOR (Insecure Direct Object Reference)**
  - اختبار: غيّر `id=123` إلى قيمة مستخدم آخر أو جرب GUIDs موجودة في التطبيق.
- **Method/URL mismatch or platform headers**
  - اختبار: أرسِل `X-Original-URL` أو جرّب GET vs POST vs PUT لكل endpoint.
- **Referer-based control**
  - اختبار: أرسل الطلب مع Referer مختلف أو احذفه.
- **Multi-step missing checks**
  - اختبار: تخطى الخطوات وأرسل مباشرة المرحلة النهائية.
- **URL-matching discrepancies (trail slash, case, suffix)**
  - اختبار: جرّب `/admin/`, `/ADMIN/deleteUser`, `/admin/deleteUser.any`.

---

## 4. منهجية عملية لحل الـ labs (خطوة بخطوة)
1. **جمع المعلومات السريعة (5–10 دقائق)**
   - استخرج روابط من UI, JS, robots.txt, sitemap, responses.
   - سجّل جميع endpoints وباراميترز مهمة.
2. **تحديد أماكن التحكم**
   - أين يقرّر السيرفر الصلاحيات؟ (session, token, param, cookie)
3. **تحكم في الطلبات (tampering)**
   - عِدّل: path, method, headers (Referer, X-Original-URL), params، body، cookies.
4. **جرّب الفرضيات البسيطة أولاً**
   - تغيير id, تعديل role=true، حذف referer، تغيير method.
5. **تحويل هجوم أفقي إلى عمودي**
   - استهدف مستخدم ذو صلاحية أعلى إذا أمكن (ابحث عن رسائل أو مراجعات تكشف GUIDs أو IDs).
6. **فحص ردود السيرفر**
   - 200 مع محتوى حساس = نجاح؛ 302/redirect مع بيانات = نجاح جزئي؛ 403/401 = مرّ.
7. **سجل خطواتك بدقة**
   - كل طلب/رد، القيم التي غيّرتها، ولماذا اعتقدت أنها مهمة.

---

## 5. قائمة طلبات اختبار (snippets قابلة للنسخ — استخدم curl/Postman)
> **ملاحظة**: غيّر القيم (`HOST`, `SESSION_COOKIE`, `id`, الخ.) حسب اللاب.

```bash
# 1) فحص رابط إدارة مخفي
curl -i -b "session=SESSION_COOKIE" https://HOST/administrator-panel-yb556

# 2) تغيير role عبر Query
curl -i -b "session=SESSION_COOKIE" "https://HOST/login/home.jsp?role=1"

# 3) IDOR: تغيير id
curl -i -b "session=SESSION_COOKIE" "https://HOST/myaccount?id=456"

# 4) تجاوز Referer
curl -i -b "session=SESSION_COOKIE" -H "Referer: https://HOST/admin" https://HOST/admin/deleteUser

# 5) تجاوز URL عبر Header (X-Original-URL)
curl -i -b "session=SESSION_COOKIE" -H "X-Original-URL: /admin/deleteUser" -X POST https://HOST/

# 6) جرّب GET بدل POST
curl -i -b "session=SESSION_COOKIE" -X GET https://HOST/admin/deleteUser
```

---

## 6. علامات نجاح وقراءة الاستجابة
- **200 OK + محتوى الهدف** = نجاح مباشر.
- **302 Redirect إلى صفحة login لكن مع بيانات في Location/Body** = نجاح جزئي (data leak).
- **403 Forbidden أو 401 Unauthorized** = لم تنجح — جرّب طرق أخرى (headers, method, path variations).
- **نص خطأ يحتوي معلومات** = مفيد للغاية (debug info، مسارات، IDs).

---

## 7. نصائح عملية سريعة للـ labs
- ابدأ دائمًا من UI → ثم فحص JS (لو فيه role/URLs مبنية فيه).
- فكّ الحماية على مستوى العميل أولاً (المتصفح/JS/hidden fields) ثم جرّب السيرفر.
- لا تعتمد على التخمين: جرّب append `/`, case variations، وإبدال الامتدادات.
- إذا كان المعرف GUID، ابحث عنه في رسائل المستخدمين أو التعليقات أو HTML.
- دوّن كل شيء: طلبات، رؤوس، أجوبة — لأن التقارير تطلب الأدلة.

---

## 8. كيف تصلّح هذه الثغرات (مختصر للمطوِّرين)
- **اعمل deny-by-default**: افترض أن أي مورد خاص ما لم يُصرّح خلاف ذلك.
- **لا تعتمد على القيم القابلة للتعديل بالعميل** (hidden fields, query params, cookies) لقرارات الصلاحية.
- **وحّد نقطة تطبيق التحكم**: كل الموارد تعتمد على نفس طبقة التحقق في السيرفر.
- **تحقق على كل خطوة** في العمليات متعددة الخطوات.
- **سجل ومراجعة**: احتفظ بسجلات محايدة للكشف عن محاولات الوصول غير المصرّح.

---

## 9. Checklist سريع قبل تحضير التقرير (لـ labs)
- [ ] وثّق endpoint المستهدف وتفاصيل الطلب (method, headers, body).
- [ ] ضمّن الطلب الأصلي والطلب بعد التلاعب (raw requests).
- [ ] سجّل ردود السيرفر (status, body snippets).
- [ ] حدِّد نوع الاستغلال (IDOR, parameter tampering, referer bypass...).
- [ ] اقترح توصية قصيرة واحدة قابلة للتنفيذ للمطور.

---

## Appendix (English — quick commands & hints)

**Quick curl examples (replace placeholders):**

```bash
# Access admin path directly
curl -i -b "session=abc" https://example.com/admin

# Modify role cookie
curl -i -b "session=abc; role=admin" https://example.com/dashboard

# Use X-Original-URL to bypass front-end routing
curl -i -b "session=abc" -H "X-Original-URL: /admin/delete" -X POST https://example.com/
```

---

### نهاية
الملف ده مُصمّم يكون مرجع عملي وانت ممكن تستخدمه كقالب لكل lab: اتبع المنهجية، سجّل كل طلب، وجرّب التلاعبات البسيطة أولًا. لو عايز أعمل لك **نسخة جاهزة للـ Obsidian** (بـ frontmatter أو قالب ملاحظات لكل lab) أقدّمها لك فورًا.



---

## مصطلحات — جدول عربي / إنجليزي

| English | العربية |
|---|---|
| Authentication | المصادقة |
| Authorization | التفويض |
| Access Control | التحكم في الوصول |
| Privilege Escalation | تصعيد الصلاحيات |
| Vertical Privilege Escalation | تصعيد صلاحيات عمودي |
| Horizontal Privilege Escalation | تصعيد صلاحيات أفقي |
| Context-dependent Access Control | التحكم في الوصول المعتمد على السياق |
| Insecure Direct Object Reference (IDOR) | مراجع كائن مباشر غير آمن (IDOR) |
| Parameter Tampering | التلاعب بالمعاملات / المعاملات |
| Session Management | إدارة الجلسات |
| Role-based Access Control (RBAC) | التحكم في الوصول بناءً على الأدوار |
| Least Privilege | مبدأ أقل صلاحية |
| Deny-by-default | الرفض افتراضيًا |
| Obfuscated / Unpredictable URL | رابط مخفي / غير متوقع |
| robots.txt | ملف robots.txt |
| Referer Header | هيدر المرجع (Referer) |
| X-Original-URL / X-Rewrite-URL | هيدر X-Original-URL / X-Rewrite-URL |
| HTTP Method (GET/POST/PUT/DELETE) | طريقة HTTP (GET/POST/PUT/DELETE) |
| Method-based Access Control | التحكم في الوصول بناءً على الطريقة |
| URL-matching Discrepancy | تفاوت مطابقة المسارات |
| GUID (Globally Unique Identifier) | معرف عالمي فريد (GUID) |
| ID (identifier) | معرف (ID) |
| 200 OK | 200 موافق (نجاح) |
| 302 Redirect | 302 إعادة توجيه |
| 401 Unauthorized | 401 غير مخوّل |
| 403 Forbidden | 403 ممنوع |
| Multi-step Process | عملية متعددة الخطوات |
| Data Leakage | تسريب بيانات |
| Security by Obscurity | الأمان عن طريق الإخفاء (غير كافٍ) |


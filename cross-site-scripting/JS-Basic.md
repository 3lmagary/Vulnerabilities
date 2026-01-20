
## 1. المتغيرات (Variables)

```js
a = 10;
let x = 20;
const y = 30;
```

**فايدته في XSS:** تتبع بيانات المستخدم اللي ممكن تُحقن في الصفحة.

---

## 2. الأنواع (Types)

- String
    
- Number
    
- Boolean
    
- Array
    
- Object
    

```js
let user = {name: "admin"};
let arr = [1,2,3];
```

**فايدته:** تعرف تتعامل مع بيانات الصفحة.

---

## 3. DOM (أهم جزء)

```js
document.getElementById("id")
document.querySelector("div")
element.innerHTML
element.textContent
element.value
```

**ليه مهم؟** لأن `innerHTML` سبب معظم ثغرات XSS.

---

## 4. Event Handlers

```html
<img src=x onerror=alert(1)>
```

أهم events: `onerror`, `onload`, `onclick`.

---

## 5. fetch()

```js
fetch("/api", { method: "POST" })
```

**أهميته:** تفهم كيف الموقع يسحب البيانات وينفذها.

---

## 6. Cookies & LocalStorage

```js
document.cookie
localStorage.getItem("token")
```

**أهمية:** سرقة الجلسات عبر XSS.

---

## 7. location

```js
location.href
location.search
location.hash
```

**أهمية:** XSS عبر URL.

---

## 8. Encoding

```js
decodeURIComponent()
atob() // Base64 decode
```

**أهمية:** عمل bypass للفلاتر.

---

## 9. Control Flow

```js
if(x == 1){}
for(let i=0;i<5;i++){}
```

**أهمية:** قراءة الكود.

---

## 10. Prototype

```js
Object.prototype.hack = "x";
```

**أهمية:** معرفة Prototype Pollution.

---

## 11. Regular Expressions

```js
/test/i.test("TEST")
```

**أهمية:** معرفة لماذا فلتر معين ضعيف.

---

## 12. Node.js أساسيات مفيدة

- require()
    
- module.exports
    
- express basics
    

**أهمية:** لو فيه تحديات backend تعتمد على JavaScript.
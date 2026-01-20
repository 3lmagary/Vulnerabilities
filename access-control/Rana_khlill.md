
# Broken Access Control — التحكم المكسور في الوصول
---

## 1. Quick overview (نظرة سريعة)
**Broken Access Control** يعني أن المستخدمين قادرون على تنفيذ أفعال أو الوصول إلى معلومات خارج صلاحياتهم المقصودة. ينتج عن ذلك تسريبات معلوماتية (Confidentiality)، تغيير بيانات (Integrity)، أو منع وصول (Availability).
> الثغره بكل بساطه هي انك تتخطي صلاحيات زي تشوف صفحه الادمين أو تغير اي حاجه في حساب مش بتاعك أو تغير امر الموقع فرضه عليك بس يعم 


---

## 2. Key concepts you must not mix up (مفاهيم أساسية - لا تخلط بينها)
-  **Authentication (التحقق من الهوية):** التحقق من "من أنت" (e.g., username/password, MFA).
- **Session management (إدارة الجلسات):** المحافظة على هوية المستخدِم عبر طلبات متعددة (session tokens/cookies).
- **Access Control / Authorization (التحكم في الوصول / التفويض):** تحديد ما يمكنك فعله أو رؤيته بعد التحقق من الهوية.
     - يعني اياللي تقدر تعمله جو الموقع  و دي بتبقي بعد authentication يعني بعد متسجل دخولك تمام

> Note: Broken Access Control is an *authorization* issue — not an authentication/session issue — but these functionalities interact.

---

## 3. Types of Access Control (أنواع التحكم في الوصول)
- **Vertical Access Control (التحكم العمودي):** يمنع المستخدمين ذوي صلاحية أقل من تنفيذ وظائف إدارة (regular → admin).
 - يتحكم في الصفحات و المعلومات اللي بتظهر يعني صفحات الادمين مفيش غيره اللييشوفها صفحات المستخدم مفيش غيره اللي يشوفها وهكذا
- **Horizontal Access Control (التحكم الأفقي):** يمنع المستخدمين المتساوين في الصلاحية من الوصول إلى موارد بعضهم البعض (user A ↔ user B).
- ده بقي بينك وبين اللي بيستخدموا الموقع يعني مينفعش حد ييجي من حسابه يغير ليا صوره حساب وهكذا 
- **Context-dependent / Workflow Access Control (التحكم السياقي/التسلسلي):** يفرض ترتيب خطوات أو حالات (multi-step processes).
- ده بقي مش ثوابت دي بتبقي حجات الموقع الليعملها زي فوري مثلا لما بتطلع كود بيقولك بعد كام ساعه هيتلغي وهكذا 

---

## 4. Broken Access Control categories (أنواع الاختراقات)
1. **Horizontal privilege escalation** — مثال: تغيير user_id في الـURL أو POST ليغطي حساب مستخدم آخر.
2. **Vertical privilege escalation** — مثال: تبديل parameter admin=false → true أو تجاوز صفحة الـadmin.
3. **Missing checks in multi-step process** — مثال: إزالة خطوة التأكيد والنداء المباشر لـ`/delete` بدون تحقق.
4. **Partial enforcement / method-specific gaps** — تحقق على GET ولكن نسيان التحقق على POST/DELETE.
5. **Client-side enforcement only** — الاعتماد على قيم من العميل (hidden field, JS) لاتخاذ قرارات.
6. **Metadata tampering** — تعديل JWT, cookies, or other tokens when server trusts client metadata.
7. **CORS misconfiguration / API origin issues** — خروقات عبر موارد أصلية غير موثوقة.
8. **Forceful browsing / path enumeration** — الوصول لصفحات/endpoints غير موثوقة عبر brute-force.

---

## 5. Real-world examples (أمثلة واقعية)
- `GET /profile?id=123` → attacker changes `id=123` to `id=124` → views other user profile (horizontal).
- Hidden form field `is_admin=false` → attacker sets `is_admin=true` → accesses admin panel (vertical).
- `POST /orders/{id}/delete` accepts request without checking owner → attacker deletes others' orders (multi-step / missing check).

---

## 6. How vulnerabilities are introduced (كيف تُوضع الثغرات في الكود)
- Missing server-side checks (developer assumes client side or workflow enforces order).
- Decentralized, inconsistent authorization logic (no central gate).
- Default-allow configuration (not deny-by-default).
- Overtrusting client-supplied identifiers (IDs, roles, flags).

---

## 7. Impact mapping to CIA triad (الأثر على السرية، السلامة، التوفر)
- **Confidentiality:** data exposure (view other users' PII).
- **Integrity:** perform actions as others (modify, spoof transactions).
- **Availability:** delete/lock resources (DoS on app-level resources).

---

## 8. Testing methodology (منهجية الاختبار)
### 8.1 Black / Gray box (الميدان / شبه المصدر)
1. **Map the app**: crawl pages, endpoints, input vectors (URL params, hidden fields, headers, cookies, JSON bodies).  
2. **Collect accounts**: request accounts for multiple roles and multiple accounts per role (to test horizontal & vertical).  
3. **Intercept and observe**: use Burp to capture requests and note ID/role tokens and patterns.  
4. **Tamper inputs**: change IDs, roles, flags; replay requests.  
5. **Automate** parts with Burp Authorize (or custom scripts) to speed horizontal/vertical checks.

### 8.2 White box / Code review (مصدر كامل)
- Locate the global authorization gate (is there one?).  
- Check adherence to deny-by-default and least-privilege.  
- Search for missing checks on API methods (GET vs POST vs DELETE).  
- Look for trusted client inputs (hidden fields, client-side role setting).  
- Validate config (CORS, webserver filters, directory access control).

---

## 9. Exploitation patterns (أنماط الاستغلال)
- Modify URL/POST parameters (IDOR) — Insecure Direct Object Reference.  
- Swap session token or reuse low-privileged cookie against high-privileged requests (session swapping).  
- Replay / tamper JWT (if algorithm confusion or no signature validation).  
- Forceful browsing: enumerate common admin paths and API endpoints.  
- Exploit missing checks on alternate HTTP methods.

---

## 10. Tools & commands (أدوات وأوامر عملية)
- **Burp Suite** (Proxy, repeater, intruder, extensions).  
  - Extension: **Autorize** (automates session swapping checks).  
- **curl** — quick API tests: `curl -i -X DELETE 'https://app/orders/123' -H 'Cookie: session=...'`  
- **httpie** — friendlier CLI: `http DELETE https://app/orders/123 Cookie:"session=..."`  
- **feroxbuster / gobuster** — forceful browsing: `feroxbuster -u https://example.com -w common-words.txt`  
- **jwt_tool / jose/jwt-cli** — test JWT manipulation and validation.  
- **Postman** — manual API testing.  

---

## 11. Fixes & secure patterns (كيفية الإصلاح وطرق آمنة)
- **Server-side enforcement only:** never rely on client to enforce rules.  
- **Centralized authorization layer:** single place to enforce policies.  
- **Deny by default** + explicit allow rules.  
- **Least privilege**: grant only necessary rights.  
- **Validate ownership**: check `resource.owner_id == current_user_id` before CRUD.  
- **Consistent checks across HTTP methods** (GET/POST/PUT/DELETE).  
- **Use non-guessable identifiers** (UUIDs, random tokens) or layered checking (IDs + owner checks).  
- **Harden tokens:** sign JWTs properly, rotate, use short expiry, bind to client context if needed.

---

## 12. Vulnerable code example + fix (مثال كود معرض للخطر مع التصحيح)
### Vulnerable (pseudo-Python)
```python
def delete_order(order_id):
    order = db.get_order(order_id)
    if order is None:
        return "Not found", 404
    db.delete(order)   # MISSING ownership check!
    log(f"deleted order {order_id} by user {current_user.id}")
    return "Deleted", 200
```

### Fix
```python
def delete_order(order_id):
    order = db.get_order(order_id)
    if order is None:
        return "Not found", 404
    if order.owner_id != current_user.id and not current_user.is_admin:
        return "Forbidden", 403
    db.delete(order)
    log(...)
    return "Deleted", 200
```

---

## 13. 13 Labs (Suggested hands-on exercises list)
Use these as the lab plan — each lab teaches one class of broken access control:
1. Simple IDOR in URL (view other profile).  
2. Hidden form field privilege escalation.  
3. Insecure direct object access on APIs (GET exposed, DELETE unprotected).  
4. Session swapping via cookies (Autorize).  
5. JWT tampering (alg=none / key confusion).  
6. Forceful browsing to admin pages.  
7. Multi-step workflow bypass (delete without confirmation).  
8. CORS misconfiguration to access API from another origin.  
9. Metadata tampering causing mis-authorisation.  
10. ID brute-force to enumerate resources.  
11. Broken RBAC vs attribute-based flaws.  
12. Access control inconsistent across microservices / endpoints.  
13. Chained attack: privilege escalation + file upload -> RCE.

---

## 14. Checklists (قوائم الفحص العملية)
### Pre-engagement checklist (قبل البدء)
- [ ] Obtain accounts for each role (2 accounts per role if possible).  
- [ ] Define scope and endpoints.  
- [ ] Configure Burp + Autorize extension.  

### Runtime testing checklist (أثناء الاختبار)
- [ ] Map app: pages, forms, endpoints.  
- [ ] Intercept all requests; identify user-id / role tokens.  
- [ ] Tamper IDs, roles, flags in URL/body/headers/cookies.  
- [ ] Test alternate methods (POST/DELETE) for missing checks.  
- [ ] Force-browse hidden paths.  
- [ ] Use Autorize to automate role swap tests.  
- [ ] Validate findings with multiple accounts & sessions.  

### Reporting checklist (التوثيق)
- [ ] Reproduce steps (step-by-step).  
- [ ] Impact assessment (CIA triad).  
- [ ] Recommend specific code/config fixes.  
- [ ] Suggest detection (logging / alerting) & monitoring steps.

---

## 15. Resources & further reading (مصادر)
- OWASP Broken Access Control cheat sheet.  
- PortSwigger Web Security Academy: Broken Access Control labs.  
- JWT best practices; RFC7519.  

---

## 16. FAQ (أسئلة متكررة)
**Q:** Can client-side validation be used for access control?  
**A:** No. Client-side can help UX but must never be trusted for authorization.

**Q:** Are UUIDs enough to prevent IDOR?  
**A:** Not on their own. Use UUIDs plus server-side ownership checks; obscurity is not authorization.

---

## 17. TL;DR (ملخص سريع جدا)
- Broken Access Control = users do things outside their permissions.  
- Test both horizontal and vertical escalation, and multi-step flows.  
- Use server-side centralized checks, deny-by-default, least-privilege.  
- Automate with Burp + Autorize, but always manually verify.

---

*Prepared and formatted for Obsidian — ready for study and labs.*
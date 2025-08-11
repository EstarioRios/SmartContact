# 📌 Contacts Management API – README

## Overview

This API provides user authentication (signup/login) and contact management features.  
It uses **JWT authentication** for secured endpoints and supports manual login with an optional `remember` flag to receive JWT tokens.

This backend is built with **Django** and **Django REST Framework (DRF)** and uses **Redis** for caching/session management or token blacklisting (depending on implementation).  
The system manages contacts with tagging and categorization features to organize contacts efficiently.

---

## 🔐 Authentication Endpoints (`/api/auth/`)

### 1️⃣ Signup – Create New User

**POST** `/api/auth/signup/`

**Body (JSON):**

```json
{
  "user_name": "john_doe",
  "password": "your_password",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Auth:** None (AllowAny)
**Success Response:** `201 Created`

```json
{
  "msg": "user created",
  "user": { ... },
  "tokens": {
    "access": "ACCESS_TOKEN",
    "refresh": "REFRESH_TOKEN"
  }
}
```

**Error Responses:**

* `400 Bad Request` → Missing required fields
* `403 Forbidden` → Username already taken

---

### 2️⃣ Manual Login – Username + Password

**POST** `/api/auth/manual-login/`

**Body (JSON):**

```json
{
  "user_name": "john_doe",
  "password": "your_password",
  "remember": true
}
```

**Auth:** None (AllowAny)
**Behavior:**

* If `remember` is `true` → Returns **JWT access & refresh tokens**
* If `remember` is `false` → Returns user data only

**Success Response (remember = true):**

```json
{
  "success": "Login successful",
  "tokens": {
    "access": "ACCESS_TOKEN",
    "refresh": "REFRESH_TOKEN"
  },
  "user": { ... }
}
```

**Error Response:**
`404 Not Found` → Invalid credentials

---

### 3️⃣ Login via JWT – Preferred Method

**POST** `/api/auth/login/`

**Headers:**

```
Authorization: Bearer ACCESS_TOKEN
```

**Auth:** None (JWT checked manually)
**Success Response:**

```json
{
  "success": "Login successful",
  "user": { ... }
}
```

**Error Response:**
`400 Bad Request` → Invalid or expired JWT

---

## 📇 Contact Endpoints (`/api/contact/`)

### 1️⃣ Create Contact

**POST** `/api/contact/create/`

**Headers:**

```
Authorization: Bearer ACCESS_TOKEN
```

**Body (JSON):**

```json
{
  "name": "Alice",
  "phone_number": "123456789",
  "tags": "family-friends"
}
```

**Success Response:**

```json
{
  "msg": "Contact created",
  "contact": { ... }
}
```

---

### 2️⃣ List All Contacts

**GET** `/api/contact/all/`

**Headers:**

```
Authorization: Bearer ACCESS_TOKEN
```

**Success Response:**

```json
[
  { "id": 1, "name": "Alice", "tags": "family-friends" },
  { "id": 2, "name": "Bob", "tags": "work" }
]
```

---

### 3️⃣ Filter Contacts by Tag

**GET** `/api/contact/by-tag/?tag=family`

**Headers:**

```
Authorization: Bearer ACCESS_TOKEN
```

**Behavior:**

* Tags in DB are stored as a single string separated by `-` (e.g., `"family-friends"`)
* Returns contacts whose `tags` contain the given tag

**Success Response:**

```json
[
  { "id": 1, "name": "Alice", "tags": "family-friends" }
]
```

---

### 4️⃣ Delete Contact

**DELETE** `/api/contact/delete/?contact_id=1`

**Headers:**

```
Authorization: Bearer ACCESS_TOKEN
```

**Success Response:**

```json
{ "msg": "Contact deleted" }
```

---

### 5️⃣ Edit Contact

**PUT** `/api/contact/edit/`

**Headers:**

```
Authorization: Bearer ACCESS_TOKEN
```

**Body (JSON):**

```json
{
  "contact_id": 1,
  "new_name": "Alice Updated",
  "new_phone_number": "987654321",
  "new_tags": "family"
}
```

**Success Response:**

```json
{
  "msg": "Contact updated",
  "contact": { ... }
}
```

---

## ⚙️ Authentication Rules Summary

| Endpoint                  | Auth Required | Method | Notes               |
| ------------------------- | ------------- | ------ | ------------------- |
| `/api/auth/signup/`       | ❌             | POST   | Create account      |
| `/api/auth/manual-login/` | ❌             | POST   | Username + password |
| `/api/auth/login/`        | ✅             | POST   | JWT authentication  |
| `/api/contact/create/`    | ✅             | POST   | Create contact      |
| `/api/contact/all/`       | ✅             | GET    | List all contacts   |
| `/api/contact/by-tag/`    | ✅             | GET    | Filter by tag       |
| `/api/contact/delete/`    | ✅             | DELETE | Delete contact      |
| `/api/contact/edit/`      | ✅             | PUT    | Edit contact        |

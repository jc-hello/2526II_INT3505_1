# 1. JWT vs OAuth 2.0 and the Meaning of Bearer Token

In Web API development, strong authentication is required because HTTP is stateless by default. A **Bearer Token** is the most common key that helps the server identify a client without checking username/password in the database for every request.

## 1.1 What Is a Bearer Token?

A **Bearer Token** means the token is valid for whoever carries it.
Think of a movie ticket: the staff does not need your name; they only need a valid ticket in your hand.

In an HTTP request, a bearer token is sent in the header:
```http
Authorization: Bearer <token_string_here>
```

> [!WARNING]
> Because this model treats the holder as the owner, leaked tokens can be abused for impersonation. Therefore, bearer tokens must always be sent over **HTTPS**.

---

## 1.2 JSON Web Token (JWT)

**JWT (JSON Web Token)** is a specific token format, serialized as a compact string (often used as a bearer token).

**Key property:** It is self-contained. It carries user information (for example ID and role). When the server receives a JWT, it can decode and validate it without hitting the database for every request.

### JWT Structure (3 Parts)
A JWT has three dot-separated parts: `Header.Payload.Signature`.

1. **Header:** Defines the signing algorithm (for example `HS256`).
2. **Payload:** Contains claims (for example `user_id`, `role`, `nbf`, `exp`).
3. **Signature:** A digital signature that prevents tampering. If payload data is modified, signature validation fails.

> [!CAUTION]
> JWT payloads can be Base64-decoded and read. Never store sensitive data (passwords, card numbers) in the payload.

---

## 1.3 What Is OAuth 2.0?

Many people think JWT and OAuth 2.0 are alternatives, but they are different layers.
- **JWT** is a token format.
- **OAuth 2.0** is an authorization framework/protocol for safely issuing and delegating token-based access to third parties.

**Library example:**
You (`User`) use website A.
Website A wants to access your borrowed-book list from the library app (`Server`).
- If website A asks for your library password directly, that is unsafe.
- **OAuth 2.0 solution:** You authenticate on the library's own login page, and the library issues an **access token** (often a JWT) to website A. Website A then uses that token on your behalf.

---

## 1.4 Practical Comparison Table

| Criteria | JWT | OAuth 2.0 |
| :--- | :--- | :--- |
| **Nature** | A token data format. | An authorization protocol/framework. |
| **Role** | The "ticket" carrying claims. | The process to request/issue/delegate that ticket. |
| **Goal** | Carry authenticated claims securely between parties. | Grant third-party apps controlled access to resources. |
| **Complexity** | Simple flow: client login -> server issues JWT. | More complex: auth server, client ID/secret, redirect callbacks, etc. |
| **Typical use** | Often used as an access token format inside OAuth 2.0 flows. | Enables features like "Login with Google" / "Login with Facebook". |

---

## 1.5 Conclusion

In our API server, endpoints such as `/loans/` do not require third-party delegation. So basic JWT-based authentication is sufficient and full OAuth 2.0 flows are unnecessary. In FastAPI, token extraction from login flows is commonly wired through `OAuth2PasswordBearer`.

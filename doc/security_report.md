# API Security Report

## 1. Introduction to API Security

Application Programming Interfaces (APIs) allow different software systems to communicate and exchange data. Because APIs often provide access to sensitive information and critical functionality, securing them is essential. Authentication ensures that only authorized users or applications can access API resources.

Without proper authentication, attackers could access confidential data, modify information, impersonate legitimate users, or disrupt services. API security helps protect data integrity, confidentiality, and availability by ensuring that requests come from trusted sources.

## 2. Basic Authentication in this API

This API uses Basic Authentication to verify the identity of clients making requests. Basic Authentication works by requiring the client to send an `Authorization` header containing a username and password encoded using Base64.

When a request is sent, the credentials are formatted as:

```
Authorization: Basic <base64-encoded-credentials>
```

The server decodes the credentials and compares them with the expected username and password. If the credentials match, the request is allowed to proceed; otherwise, access is denied.

In this implementation, every protected endpoint passes through the `is_authenticated()` function, which performs the authentication check before any API operation is executed. When authentication fails, the API returns an HTTP 401 Unauthorized response with a JSON error body, signaling to the client that valid credentials are required.

## 3. Limitations of Basic Authentication

Although Basic Authentication is simple to implement and useful for learning purposes, it has several important security limitations:

### Base64 Is Not Encryption

Basic Authentication uses Base64 encoding, which is not a form of encryption. Anyone who intercepts the encoded credentials can easily decode them and recover the original username and password.

### Credentials Sent on Every Request

The username and password are transmitted with every API request. This increases the risk of credential exposure because the same sensitive information is repeatedly sent across the network.

### No Expiration or Revocation

Basic Authentication does not provide built-in mechanisms for token expiration, session management, or credential revocation. Once credentials are known, they remain valid until manually changed.

### Hardcoded Credentials

For this assignment, the credentials are stored directly in the source code. While acceptable in a learning environment, hardcoded credentials are considered poor security practice because anyone with access to the code can view them. In production systems, credentials would be stored as salted hashes in a database, with the plain password never appearing in source code or version control.

### Vulnerable Over HTTP

If Basic Authentication is used over plain HTTP instead of HTTPS, credentials can be captured by attackers monitoring network traffic. Because the credentials are only encoded, not encrypted, they are easily exposed.

## 4. Stronger Alternatives

### JWT (JSON Web Tokens)

JSON Web Tokens (JWTs) provide a more secure and flexible authentication mechanism.

With JWT authentication:

1. A user logs in with valid credentials.
2. The server generates and signs a token.
3. The client stores the token and includes it in future requests.
4. The server verifies the token's signature before granting access.

JWTs are signed using a secret key (HMAC) or a public/private key pair (RSA), so any tampering invalidates the token. They can also include expiration times, reducing the risk associated with stolen credentials. Since the server only needs to verify the token signature, it can remain stateless and avoid storing session data.

### OAuth 2.0

OAuth 2.0 is an industry-standard framework for authorization that allows users to grant limited access to applications without sharing their passwords.

Key benefits include:

* Delegated authorization through access tokens.
* Fine-grained permission scopes.
* No need to share user credentials with third-party applications.
* Support for secure authentication flows used by major platforms.

OAuth 2.0 is commonly used by services such as Google, Microsoft, GitHub, and many enterprise applications.

## 5. Conclusion

Basic Authentication is useful for educational projects because it is straightforward to understand and implement. However, it has significant security weaknesses, including the repeated transmission of credentials, lack of expiration mechanisms, and vulnerability when used without HTTPS.

In a real MoMo deployment handling actual customer financial data, Basic Authentication would not be acceptable. JWT or OAuth 2.0 over HTTPS, combined with input validation, rate limiting, and audit logging, would form the minimum baseline for protecting users and their transactions.
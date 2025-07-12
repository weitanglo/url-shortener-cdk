# 🏗️ URL Shortener Service - ASCII Architecture

> **🤖 Built with Amazon Q Developer**

## 📊 System Architecture (ASCII)

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          URL Shortener Service                                 │
│                      🤖 Built with Amazon Q Developer                          │
└─────────────────────────────────────────────────────────────────────────────────┘

                                    👤 Users
                                      │
                                      ▼
                            ┌─────────────────┐
                            │   🌍 Route53    │
                            │  DNS Management │
                            └─────────┬───────┘
                                      │
                                      ▼
                            ┌─────────────────┐
                            │ 🔗 Custom Domain│
                            │url.loweitang.com│
                            └─────────┬───────┘
                                      │
                                      ▼
                            ┌─────────────────┐      ┌─────────────────┐
                            │  🚪 API Gateway │◄────►│  🔒 ACM Cert    │
                            │    HTTP API     │      │   SSL/TLS       │
                            └─────────┬───────┘      └─────────────────┘
                                      │
                    ┌─────────────────┼─────────────────┐
                    │                 │                 │
                    ▼                 ▼                 ▼
          ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
          │  🔐 Cognito     │ │  🎫 JWT Auth    │ │  🛡️ IAM Roles   │
          │   User Pool     │ │   Authorizer    │ │   & Policies    │
          └─────────────────┘ └─────────────────┘ └─────────────────┘
                                      │
                    ┌─────────────────┼─────────────────┐
                    │                 │                 │
                    ▼                 ▼                 ▼
    ┌─────────────────────────────────────────────────────────────────┐
    │                    🔧 Lambda Functions                          │
    ├─────────────┬─────────────┬─────────────┬─────────────────────┤
    │ 📝 Create   │ 📋 Get      │ 🗑️ Delete   │ ↩️ Redirect         │
    │    URL      │    URLs     │    URL      │                     │
    ├─────────────┼─────────────┼─────────────┼─────────────────────┤
    │ 👥 Signup   │ 🔑 Login    │ 📦 Layer    │                     │
    │             │             │ (Shared)    │                     │
    └─────────────┴─────────────┴─────────────┴─────────────────────┘
                                      │
                    ┌─────────────────┼─────────────────┐
                    │                 │                 │
                    ▼                 ▼                 ▼
          ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
          │  🗄️ DynamoDB    │ │  🗄️ DynamoDB    │ │  📊 CloudWatch  │
          │   URL Table     │ │   User Table    │ │  Logs & Metrics │
          │   + GSI         │ │                 │ │                 │
          └─────────────────┘ └─────────────────┘ └─────────────────┘
                                                           │
                                                           ▼
                                                  ┌─────────────────┐
                                                  │  🔍 X-Ray       │
                                                  │   Tracing       │
                                                  └─────────────────┘
```

## 🔄 Request Flow Diagram

```
User Request Flow:
┌─────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│User │───►│Route53  │───►│API GW   │───►│Lambda   │───►│DynamoDB │
└─────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘
                                │
                                ▼
                          ┌─────────┐
                          │Cognito  │
                          │JWT Auth │
                          └─────────┘

Authentication Flow:
┌─────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│User │───►│/login   │───►│Cognito  │───►│JWT Token│
└─────┘    └─────────┘    └─────────┘    └─────────┘

URL Creation Flow:
┌─────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│User │───►│/createurl│───►│JWT Check│───►│Lambda   │───►│DynamoDB │
└─────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘

Redirect Flow:
┌─────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│User │───►│/{code}  │───►│Lambda   │───►│Redirect │
└─────┘    └─────────┘    └─────────┘    └─────────┘
```

## 🏗️ CDK Stack Dependencies

```
Deployment Order:
┌─────────────────┐
│  Database Stack │
│                 │
│ ┌─────────────┐ │
│ │ URL Table   │ │
│ │ User Table  │ │
│ │ GSI Indexes │ │
│ └─────────────┘ │
└─────────┬───────┘
          │ depends on
          ▼
┌─────────────────┐
│ Security Stack  │
│                 │
│ ┌─────────────┐ │
│ │ Cognito     │ │
│ │ IAM Roles   │ │
│ │ Policies    │ │
│ └─────────────┘ │
└─────────┬───────┘
          │ depends on
          ▼
┌─────────────────┐
│   API Stack     │
│                 │
│ ┌─────────────┐ │
│ │ API Gateway │ │
│ │ 6x Lambda   │ │
│ │ Custom DNS  │ │
│ │ SSL Cert    │ │
│ └─────────────┘ │
└─────────────────┘
```

## 🌍 Multi-Environment Layout

```
┌─────────────────────────────────────────────────────────────────┐
│                    Environment Separation                       │
└─────────────────────────────────────────────────────────────────┘

Development:                 Staging:                 Production:
┌─────────────────┐         ┌─────────────────┐      ┌─────────────────┐
│url-dev.         │         │url-staging.     │      │url.             │
│loweitang.com    │         │loweitang.com    │      │loweitang.com    │
├─────────────────┤         ├─────────────────┤      ├─────────────────┤
│UrlShortener-    │         │UrlShortener-    │      │UrlShortener-    │
│Database-dev     │         │Database-staging │      │Database-prod    │
│Security-dev     │         │Security-staging │      │Security-prod    │
│Api-dev          │         │Api-staging      │      │Api-prod         │
└─────────────────┘         └─────────────────┘      └─────────────────┘
         │                           │                         │
         └───────────────────────────┼─────────────────────────┘
                                     │
                            ┌─────────────────┐
                            │  Shared Route53 │
                            │ loweitang.com   │
                            └─────────────────┘
```

## 📊 API Endpoints Map

```
API Gateway Routes:
┌─────────────────────────────────────────────────────────────────┐
│                    HTTP API Endpoints                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Public Endpoints (No Auth):                                   │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ POST /signup    │  │ POST /login     │  │ GET /{code}     │ │
│  │ User Registration│  │ Authentication  │  │ URL Redirect    │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│                                                                 │
│  Protected Endpoints (JWT Required):                            │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │ POST /createurl │  │ GET /geturls    │  │ DELETE /delete  │ │
│  │ Create Short URL│  │ List User URLs  │  │ Delete URL      │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🔒 Security Layers

```
Security Architecture:
┌─────────────────────────────────────────────────────────────────┐
│                      Security Layers                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Layer 1: Network Security                                      │
│  ┌─────────────────┐  ┌─────────────────┐                      │
│  │ HTTPS Only      │  │ CORS Policy     │                      │
│  │ ACM Certificate │  │ Origin Control  │                      │
│  └─────────────────┘  └─────────────────┘                      │
│                                                                 │
│  Layer 2: Authentication                                        │
│  ┌─────────────────┐  ┌─────────────────┐                      │
│  │ Cognito User    │  │ JWT Tokens      │                      │
│  │ Pool            │  │ Validation      │                      │
│  └─────────────────┘  └─────────────────┘                      │
│                                                                 │
│  Layer 3: Authorization                                         │
│  ┌─────────────────┐  ┌─────────────────┐                      │
│  │ IAM Roles       │  │ Resource        │                      │
│  │ & Policies      │  │ Permissions     │                      │
│  └─────────────────┘  └─────────────────┘                      │
│                                                                 │
│  Layer 4: Data Security                                         │
│  ┌─────────────────┐  ┌─────────────────┐                      │
│  │ DynamoDB        │  │ Lambda          │                      │
│  │ Encryption      │  │ Environment     │                      │
│  └─────────────────┘  └─────────────────┘                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🤖 Amazon Q Developer Generated Architecture

**Key Metrics:**
- 📊 **Total AWS Services**: 15+
- 🔧 **Lambda Functions**: 6
- 🗄️ **Database Tables**: 2 (with GSI)
- 🌍 **Environments**: 3 (dev/staging/prod)
- 🔒 **Security Layers**: 4
- 📈 **Scalability**: Auto-scaling serverless
- 💰 **Cost Model**: Pay-per-use

**Architecture Highlights:**
✅ Fully Serverless  
✅ Multi-Environment Ready  
✅ Security Best Practices  
✅ Auto-Scaling  
✅ Monitoring & Observability  
✅ Cost Optimized  

**🎯 100% Generated by Amazon Q Developer AI Assistant**

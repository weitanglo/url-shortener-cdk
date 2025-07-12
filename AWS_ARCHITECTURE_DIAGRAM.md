# 🏗️ AWS Architecture Diagram - URL Shortener Service

> **🤖 Built with Amazon Q Developer**  
> draw.io style AWS architecture diagram

## 📊 AWS Infrastructure Overview

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                          🌐 Internet Users                                                      │
└─────────────────────────────────────────────────────┬───────────────────────────────────────────────────────────┘
                                                      │
                                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                         🌍 Amazon Route 53                                                      │
│                                      DNS Management Service                                                     │
│                                                                                                                 │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐                                    │
│  │ url-dev.loweitang   │  │ url-staging.        │  │ url.loweitang.com   │                                    │
│  │ .com                │  │ loweitang.com       │  │                     │                                    │
│  └─────────────────────┘  └─────────────────────┘  └─────────────────────┘                                    │
└─────────────────────────────────────┬───────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    🔒 AWS Certificate Manager (ACM)                                            │
│                                         SSL/TLS Certificates                                                   │
│                                                                                                                 │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐                                    │
│  │ *.loweitang.com     │  │ Auto Validation     │  │ Auto Renewal        │                                    │
│  │ Wildcard Cert       │  │ DNS Challenge       │  │ 90 Days             │                                    │
│  └─────────────────────┘  └─────────────────────┘  └─────────────────────┘                                    │
└─────────────────────────────────────┬───────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    🚪 Amazon API Gateway                                                       │
│                                      HTTP API (v2)                                                             │
│                                                                                                                 │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐                                    │
│  │ Custom Domain       │  │ CORS Enabled        │  │ JWT Authorizer      │                                    │
│  │ Integration         │  │ Multiple Methods    │  │ Cognito Integration │                                    │
│  └─────────────────────┘  └─────────────────────┘  └─────────────────────┘                                    │
│                                                                                                                 │
│  API Endpoints:                                                                                                 │
│  ├── POST /signup          (No Auth)                                                                           │
│  ├── POST /login           (No Auth)                                                                           │
│  ├── POST /createurl       (JWT Auth) ✨ Enhanced                                                              │
│  ├── GET  /geturls         (JWT Auth) ✨ Enhanced                                                              │
│  ├── DELETE /deleteurl/{id} (JWT Auth)                                                                         │
│  ├── POST /url-info        (JWT Auth) 🆕 New                                                                   │
│  └── GET  /{shortCode}     (No Auth)                                                                           │
└─────────────────────────────────────┬───────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   🔐 Amazon Cognito                                                            │
│                                    User Pool Service                                                           │
│                                                                                                                 │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐                                    │
│  │ User Pool           │  │ User Pool Client    │  │ JWT Token           │                                    │
│  │ Email Verification  │  │ No Secret           │  │ Validation          │                                    │
│  └─────────────────────┘  └─────────────────────┘  └─────────────────────┘                                    │
└─────────────────────────────────────┬───────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    🔧 AWS Lambda Functions                                                     │
│                                   Python 3.10 Runtime                                                         │
│                                                                                                                 │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐            │
│  │ 📝 createurl        │  │ 📋 geturls          │  │ 🗑️ deleteurl        │  │ ↩️ redirect          │            │
│  │ Enhanced with       │  │ Enhanced with       │  │ Standard function   │  │ Standard function   │            │
│  │ URL Info Scraping   │  │ Rich URL Info       │  │                     │  │                     │            │
│  └─────────────────────┘  └─────────────────────┘  └─────────────────────┘  └─────────────────────┘            │
│                                                                                                                 │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐                                    │
│  │ 👥 signup           │  │ 🔑 login            │  │ 🆕 url-info         │                                    │
│  │ Cognito Integration │  │ Cognito Integration │  │ URL Preview         │                                    │
│  │                     │  │                     │  │ Web Scraping        │                                    │
│  └─────────────────────┘  └─────────────────────┘  └─────────────────────┘                                    │
│                                                                                                                 │
│  📦 Shared Lambda Layer:                                                                                       │
│  ├── boto3, botocore                                                                                           │
│  ├── requests ✨                                                                                               │
│  ├── beautifulsoup4 ✨                                                                                         │
│  └── lxml ✨                                                                                                   │
└─────────────────────────────────────┬───────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   🗄️ Amazon DynamoDB                                                          │
│                                  NoSQL Database Service                                                        │
│                                                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │                              📊 URL Shortener Table                                                    │  │
│  │  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐                          │  │
│  │  │ Primary Key: id     │  │ GSI: shortCode      │  │ GSI: createdBy      │                          │  │
│  │  │ UUID                │  │ Unique Index        │  │ User URLs           │                          │  │
│  │  └─────────────────────┘  └─────────────────────┘  └─────────────────────┘                          │  │
│  │                                                                                                       │  │
│  │  Enhanced Fields: ✨                                                                                  │  │
│  │  ├── title (Site Title)                                                                              │  │
│  │  ├── description (Meta Description)                                                                  │  │
│  │  ├── favicon (Favicon URL)                                                                           │  │
│  │  ├── image (OG Image URL)                                                                            │  │
│  │  ├── site_name (Site Name)                                                                           │  │
│  │  └── domain (Domain Name)                                                                            │  │
│  └─────────────────────────────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │                                👤 User Table                                                          │  │
│  │  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐                          │  │
│  │  │ Primary Key: id     │  │ User Data           │  │ Cognito Integration │                          │  │
│  │  │ User ID             │  │ Profile Info        │  │ JWT Claims          │                          │  │
│  │  └─────────────────────┘  └─────────────────────┘  └─────────────────────┘                          │  │
│  └─────────────────────────────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │                          🆕 URL Info Cache Table                                                      │  │
│  │  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐                          │  │
│  │  │ Primary Key: url    │  │ GSI: domain         │  │ TTL: 7 days ✨      │                          │  │
│  │  │ Original URL        │  │ Domain Index        │  │ Auto Deletion       │                          │  │
│  │  └─────────────────────┘  └─────────────────────┘  └─────────────────────┘                          │  │
│  │                                                                                                       │  │
│  │  Cached Fields: ✨                                                                                    │  │
│  │  ├── title, description, favicon, image                                                              │  │
│  │  ├── site_name, retrieved_at                                                                         │  │
│  │  ├── status_code, content_type                                                                       │  │
│  │  └── ttl (Unix Timestamp)                                                                            │  │
│  └─────────────────────────────────────────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   🛡️ AWS IAM (Identity & Access Management)                                   │
│                                      Security & Permissions                                                    │
│                                                                                                                 │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐                                    │
│  │ Lambda Execution    │  │ DynamoDB Access     │  │ Cognito Access      │                                    │
│  │ Role                │  │ Policy              │  │ Policy              │                                    │
│  └─────────────────────┘  └─────────────────────┘  └─────────────────────┘                                    │
│                                                                                                                 │
│  Enhanced Permissions: ✨                                                                                      │
│  ├── All 3 DynamoDB Tables Access                                                                              │
│  ├── CloudWatch Logs Write                                                                                     │
│  ├── X-Ray Tracing                                                                                             │
│  └── SES Email Sending                                                                                         │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   📊 Amazon CloudWatch                                                         │
│                                  Monitoring & Logging                                                          │
│                                                                                                                 │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐                                    │
│  │ Lambda Logs         │  │ API Gateway Logs    │  │ DynamoDB Metrics    │                                    │
│  │ Function Metrics    │  │ Request Metrics     │  │ Read/Write Units    │                                    │
│  └─────────────────────┘  └─────────────────────┘  └─────────────────────┘                                    │
│                                                                                                                 │
│  Enhanced Monitoring: ✨                                                                                       │
│  ├── URL Scraping Performance                                                                                  │
│  ├── Cache Hit/Miss Ratio                                                                                      │
│  ├── Error Rate Tracking                                                                                       │
│  └── Response Time Analysis                                                                                    │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   🔍 AWS X-Ray                                                                 │
│                                 Distributed Tracing                                                            │
│                                                                                                                 │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐                                    │
│  │ Request Tracing     │  │ Performance         │  │ Error Analysis      │                                    │
│  │ End-to-End          │  │ Bottleneck Detection│  │ Root Cause          │                                    │
│  └─────────────────────┘  └─────────────────────┘  └─────────────────────┘                                    │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## 🌐 External Integrations

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                  🌍 External Web Sites                                                         │
│                                   URL Scraping Targets                                                         │
│                                                                                                                 │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐            │
│  │ 🐙 GitHub           │  │ 📰 News Sites       │  │ 🛒 E-commerce       │  │ 📱 Social Media    │            │
│  │ github.com          │  │ Various domains     │  │ Shopping sites      │  │ Twitter, Facebook   │            │
│  └─────────────────────┘  └─────────────────────┘  └─────────────────────┘  └─────────────────────┘            │
│                                      │                                                                          │
│                                      ▼                                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │                              🕷️ Web Scraping Process                                                  │  │
│  │                                                                                                       │  │
│  │  1. HTTP Request with User-Agent                                                                     │  │
│  │  2. HTML Content Parsing (BeautifulSoup4)                                                            │  │
│  │  3. Metadata Extraction:                                                                             │  │
│  │     ├── Open Graph Tags (og:title, og:description, og:image)                                         │  │
│  │     ├── Twitter Cards (twitter:title, twitter:description)                                           │  │
│  │     ├── HTML Meta Tags (title, description)                                                          │  │
│  │     └── Favicon Detection (4 patterns)                                                               │  │
│  │  4. Error Handling (Timeout, Connection, HTTP errors)                                                │  │
│  │  5. Cache Storage (DynamoDB with TTL)                                                                │  │
│  └─────────────────────────────────────────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## 🔄 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    📊 URL Creation Flow                                                        │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

User Input → API Gateway → JWT Validation → Lambda (createurl) → Web Scraping → Cache Check → DynamoDB Storage
     │              │              │                │                    │             │              │
     │              │              │                │                    │             │              ▼
     │              │              │                │                    │             │        ┌─────────────┐
     │              │              │                │                    │             │        │ URL Table   │
     │              │              │                │                    │             │        │ + URL Info  │
     │              │              │                │                    │             │        └─────────────┘
     │              │              │                │                    │             │
     │              │              │                │                    │             ▼
     │              │              │                │                    │        ┌─────────────┐
     │              │              │                │                    │        │ Cache Table │
     │              │              │                │                    │        │ (TTL 7days) │
     │              │              │                │                    │        └─────────────┘
     │              │              │                │                    │
     │              │              │                │                    ▼
     │              │              │                │              ┌─────────────┐
     │              │              │                │              │ External    │
     │              │              │                │              │ Website     │
     │              │              │                │              │ Scraping    │
     │              │              │                │              └─────────────┘
     │              │              │                │
     │              │              │                ▼
     │              │              │          ┌─────────────┐
     │              │              │          │ Lambda      │
     │              │              │          │ Function    │
     │              │              │          │ Processing  │
     │              │              │          └─────────────┘
     │              │              │
     │              │              ▼
     │              │        ┌─────────────┐
     │              │        │ Cognito     │
     │              │        │ JWT Token   │
     │              │        │ Validation  │
     │              │        └─────────────┘
     │              │
     │              ▼
     │        ┌─────────────┐
     │        │ API Gateway │
     │        │ HTTP API    │
     │        │ Routing     │
     │        └─────────────┘
     │
     ▼
┌─────────────┐
│ User        │
│ Interface   │
│ (Frontend)  │
└─────────────┘
```

## 🏷️ AWS Resource Tags

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                    🏷️ Resource Tagging Strategy                                                │
│                                                                                                                 │
│  All AWS Resources are tagged with:                                                                            │
│                                                                                                                 │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐                                    │
│  │ Project             │  │ Environment         │  │ BuiltWith           │                                    │
│  │ UrlShortener        │  │ dev/staging/prod    │  │ Amazon-Q-Developer  │                                    │
│  └─────────────────────┘  └─────────────────────┘  └─────────────────────┘                                    │
│                                                                                                                 │
│  ┌─────────────────────┐  ┌─────────────────────┐                                                              │
│  │ CreatedBy           │  │ Feature             │                                                              │
│  │ Amazon-Q-Developer  │  │ URL-Info-Enhanced   │                                                              │
│  │ -AI-Assistant       │  │                     │                                                              │
│  └─────────────────────┘  └─────────────────────┘                                                              │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## 🌟 Phase 2 Enhanced Features

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                  ✨ URL Information Enhancement                                                 │
│                                                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │                              🕷️ Web Scraping Engine                                                   │  │
│  │                                                                                                       │  │
│  │  Input: URL → HTTP Request → HTML Parsing → Metadata Extraction → Cache Storage                     │  │
│  │                                                                                                       │  │
│  │  Extracted Data:                                                                                     │  │
│  │  ├── 📝 Title (Open Graph → Twitter → HTML)                                                          │  │
│  │  ├── 📄 Description (Meta tags priority)                                                             │  │
│  │  ├── 🎨 Favicon (4 detection patterns)                                                               │  │
│  │  ├── 🖼️ Image (OG Image → Twitter Image)                                                             │  │
│  │  ├── 🏢 Site Name (Open Graph)                                                                       │  │
│  │  └── 🌐 Domain (URL parsing)                                                                         │  │
│  └─────────────────────────────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │                              🧠 Smart Caching System                                                  │  │
│  │                                                                                                       │  │
│  │  Cache Strategy:                                                                                     │  │
│  │  ├── 🔍 Check Cache First (DynamoDB Query)                                                           │  │
│  │  ├── ⏰ TTL Validation (7 days)                                                                      │  │
│  │  ├── 🔄 Auto Refresh (Expired data)                                                                  │  │
│  │  ├── 💾 Store New Data (TTL timestamp)                                                               │  │
│  │  └── 📊 Performance Tracking (Hit/Miss ratio)                                                        │  │
│  └─────────────────────────────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │                              🛡️ Error Handling System                                                │  │
│  │                                                                                                       │  │
│  │  Error Types:                                                                                        │  │
│  │  ├── ⏱️ Timeout (15 seconds limit)                                                                   │  │
│  │  ├── 🔌 Connection Error (Network issues)                                                            │  │
│  │  ├── 🚫 HTTP Error (4xx, 5xx responses)                                                              │  │
│  │  ├── 📄 Content Type (Non-HTML filtering)                                                            │  │
│  │  └── 🔄 Fallback Data (Domain-based info)                                                            │  │
│  └─────────────────────────────────────────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

**🤖 Generated by Amazon Q Developer AI Assistant**  
*Complete AWS Architecture with Enhanced URL Information Features*

**📊 Architecture Summary:**
- **3 CDK Stacks**: Database, Security, API
- **7 Lambda Functions**: Enhanced with web scraping
- **3 DynamoDB Tables**: Optimized with GSI + TTL
- **1 API Gateway**: 7 endpoints with JWT auth
- **1 Cognito User Pool**: Complete authentication
- **Route53 + ACM**: Custom domain with SSL
- **CloudWatch + X-Ray**: Full observability

**🌟 Phase 2 Enhanced Features:**
- Smart URL information extraction
- 7-day TTL caching system
- Production-grade error handling
- Multi-pattern metadata detection
- Performance optimization

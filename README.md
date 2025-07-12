# URL Shortener Service

> **🤖 Built with Amazon Q Developer**  
> このプロジェクトは完全にAmazon Q Developer AI Assistantによって作成されました。

[![Built with Amazon Q Developer](https://img.shields.io/badge/Built%20with-Amazon%20Q%20Developer-FF9900?style=flat-square&logo=amazon-aws)](https://aws.amazon.com/q/developer/)
[![AWS CDK](https://img.shields.io/badge/AWS-CDK-FF9900?style=flat-square&logo=amazon-aws)](https://aws.amazon.com/cdk/)
[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=flat-square&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Serverless](https://img.shields.io/badge/Serverless-FD5750?style=flat-square&logo=serverless&logoColor=white)](https://www.serverless.com/)

AWS CDK (TypeScript) で構築されたサーバーレスURL短縮サービスです。**URL情報自動取得機能**付きで、リッチなプレビュー表示が可能です。

## 🏗️ アーキテクチャ

📊 **[詳細なアーキテクチャ図を見る](./ARCHITECTURE.md)**  
🎨 **[ASCII版アーキテクチャ図を見る](./ARCHITECTURE_ASCII.md)**  
🔧 **[AWS構成図 (draw.io形式)](./AWS_ARCHITECTURE_DIAGRAM.md)**  
📈 **[Mermaid構成図](./AWS_MERMAID_DIAGRAM.md)**

### 技術スタック
- **フレームワーク**: AWS CDK (TypeScript)
- **認証**: Amazon Cognito User Pool
- **API**: API Gateway HTTP API
- **コンピュート**: AWS Lambda (Python 3.10)
- **データベース**: Amazon DynamoDB (3テーブル)
- **ドメイン**: Route53 + ACM
- **Web Scraping**: BeautifulSoup4 + Requests
- **開発**: Amazon Q Developer AI Assistant

### システム概要図
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Database   │    │  Security   │    │     API     │
│    Stack    │    │    Stack    │    │    Stack    │
├─────────────┤    ├─────────────┤    ├─────────────┤
│ DynamoDB    │    │ Cognito     │    │ API Gateway │
│ - URLs      │    │ User Pool   │    │ HTTP API    │
│ - Users     │    │ IAM Roles   │    │ 7x Lambda   │
│ - URL Info  │    │ JWT Auth    │    │ Custom DNS  │
│ - GSI + TTL │    │             │    │ URL Scraper │
└─────────────┘    └─────────────┘    └─────────────┘
```

### 🆕 主要機能 (Phase 2 Enhanced)
- **URL短縮・管理** - カスタムコード対応
- **ユーザー認証・認可** - Cognito JWT
- **カスタムドメイン対応** - 環境別サブドメイン
- **リアルタイムリダイレクト** - 高速レスポンス
- **🌟 URL情報自動取得** - タイトル、説明、ファビコン、画像
- **🌟 スマートキャッシュ** - 7日間TTL付きキャッシュ
- **🌟 エラーハンドリング** - 堅牢なWeb scraping
- **環境別デプロイ** - dev/staging/prod

## 🚀 Amazon Q Developer による開発

このプロジェクトの特徴：
- **100% AI生成**: 全てのコード、設定、ドキュメントがAmazon Q Developerによって生成
- **ベストプラクティス**: AWS CDKとサーバーレスアーキテクチャのベストプラクティスを適用
- **モダンな技術スタック**: TypeScript、Python、AWS最新サービスを活用
- **プロダクション品質**: エンタープライズレベルの機能と信頼性

## プロジェクト構成

```
url-shortener-cdk/
├── bin/
│   └── url-shortener-cdk.ts     # CDK アプリエントリーポイント
├── lib/
│   ├── stacks/
│   │   ├── database-stack.ts    # DynamoDB テーブル (3テーブル)
│   │   ├── security-stack.ts    # Cognito + IAM
│   │   └── api-stack.ts         # API Gateway + Lambda
│   └── constructs/
│       └── lambda-function.ts   # Lambda関数 Construct
├── lambda/                      # Lambda関数ソースコード
│   ├── createurl/              # URL作成 (URL情報取得付き)
│   ├── geturls/                # URL一覧取得 (情報付き)
│   ├── deleteurl/              # URL削除
│   ├── redirect/               # リダイレクト
│   ├── signup/                 # ユーザー登録
│   ├── login/                  # ログイン
│   ├── url-info/               # 🆕 URL情報取得専用
│   └── Layer/                  # 共有ライブラリ (Web scraping)
├── config/
│   └── config.ts               # 環境別設定
├── ARCHITECTURE.md             # 詳細アーキテクチャ図
├── ARCHITECTURE_ASCII.md       # ASCII版アーキテクチャ図
├── AWS_ARCHITECTURE_DIAGRAM.md # 🆕 AWS構成図 (draw.io形式)
├── AWS_MERMAID_DIAGRAM.md      # 🆕 Mermaid構成図
├── AMAZON_Q_DEVELOPER.md       # AI生成詳細
└── test/                       # テストファイル
```

## 🚀 クイックスタート

### 前提条件
- Node.js 18+
- AWS CLI 設定済み
- AWS CDK CLI インストール済み

### インストール
```bash
git clone https://github.com/weitanglo/url-shortener-cdk.git
cd url-shortener-cdk
npm install
```

### ビルド
```bash
npm run build
```

### デプロイ
```bash
# 開発環境
npm run deploy:dev

# 本番環境
npm run deploy:prod
```

## デプロイ

### 環境別デプロイ
```bash
# 開発環境 (url-dev.loweitang.com)
npx cdk deploy --all --context stage=dev

# ステージング環境 (url-staging.loweitang.com)
npx cdk deploy --all --context stage=staging

# 本番環境 (url.loweitang.com)
npx cdk deploy --all --context stage=prod
```

### 個別スタックデプロイ
```bash
# データベースのみ (3テーブル)
npx cdk deploy UrlShortener-Database-dev

# セキュリティのみ (Cognito)
npx cdk deploy UrlShortener-Security-dev

# APIのみ (7つのLambda関数)
npx cdk deploy UrlShortener-Api-dev
```

## 📋 API エンドポイント

| メソッド | パス | 説明 | 認証 | 🆕 機能 |
|---------|------|------|------|--------|
| POST | `/signup` | ユーザー登録 (Cognito) | なし | |
| POST | `/login` | ログイン (Cognito) | なし | |
| POST | `/createurl` | URL短縮 | 必要 | ✨ URL情報自動取得 |
| GET | `/geturls` | URL一覧取得 | 必要 | ✨ リッチ情報表示 |
| DELETE | `/deleteurl/{id}` | URL削除 | 必要 | |
| GET | `/{shortCode}` | リダイレクト | なし | |
| POST | `/url-info` | 🆕 URL情報プレビュー | 必要 | ✨ 事前プレビュー |

### 🆕 拡張されたAPIレスポンス

#### URL作成時のレスポンス
```json
{
  "id": "uuid-here",
  "shortUrl": "https://url.loweitang.com/abc123",
  "shortCode": "abc123",
  "originalUrl": "https://github.com",
  "urlInfo": {
    "title": "GitHub: Let's build from here",
    "description": "GitHub is where over 100 million developers shape the future of software, together.",
    "favicon": "https://github.com/favicon.ico",
    "image": "https://github.com/images/og-image.png",
    "site_name": "GitHub",
    "domain": "github.com"
  },
  "createdAt": "2025-07-12T06:00:00.000Z",
  "cached": false
}
```

#### URL一覧取得時のレスポンス
```json
{
  "urls": [
    {
      "id": "uuid-here",
      "shortCode": "abc123",
      "originalUrl": "https://github.com",
      "shortUrl": "https://url.loweitang.com/abc123",
      "createdAt": "2025-07-12T06:00:00.000Z",
      "clickCount": 5,
      "isActive": true,
      "urlInfo": {
        "title": "GitHub: Let's build from here",
        "description": "GitHub is where over 100 million developers...",
        "favicon": "https://github.com/favicon.ico",
        "image": "https://github.com/images/og-image.png",
        "site_name": "GitHub",
        "domain": "github.com"
      }
    }
  ],
  "count": 1
}
```

## 🗄️ データベース設計

### DynamoDBテーブル (3テーブル)

#### 1. URL短縮テーブル (拡張版)
```
urlshortnertable-{stage}
├── id (PK)
├── shortCode + GSI
├── createdBy + GSI
├── originalUrl
├── title ✨
├── description ✨
├── favicon ✨
├── image ✨
├── site_name ✨
├── domain ✨
└── clickCount, isActive, createdAt
```

#### 2. ユーザーテーブル
```
usertable-{stage}
├── id (PK)
└── user data
```

#### 3. 🆕 URL情報キャッシュテーブル
```
urlinfotable-{stage}
├── url (PK)
├── domain + GSI
├── title, description, favicon, image
├── site_name, retrieved_at
├── ttl (7日間自動削除) ✨
└── status_code, content_type
```

## 環境設定

環境別設定は `config/config.ts` で管理：

- **dev**: `url-dev.loweitang.com`
- **staging**: `url-staging.loweitang.com`
- **prod**: `url.loweitang.com`

## 開発

### 開発コマンド
```bash
npm run build      # TypeScriptビルド
npm run watch      # ウォッチモード
npm test           # テスト実行
npx cdk synth      # テンプレート生成
npx cdk diff       # 差分確認
```

### CDK コマンド
```bash
# テンプレート生成
npx cdk synth

# 差分確認
npx cdk diff

# スタック削除
npx cdk destroy --all
```

## 🔒 セキュリティ

- Amazon Cognito User Pool による認証
- JWT トークンベースの認可
- IAM ロールベースのアクセス制御
- HTTPS 強制 (ACM証明書)
- 環境別リソース分離
- **🆕 Web scraping セキュリティ**: User-Agent設定、タイムアウト制御

## 📊 モニタリング

- CloudWatch Logs (Lambda)
- X-Ray トレーシング
- DynamoDB メトリクス
- API Gateway メトリクス
- **🆕 URL取得パフォーマンス**: キャッシュヒット率、レスポンス時間

## 🌟 URL情報取得機能 (Phase 2)

### 取得される情報
- **タイトル**: Open Graph → Twitter → HTML title
- **説明文**: Open Graph → Twitter → meta description  
- **ファビコン**: 4種類のパターンに対応
- **画像**: Open Graph → Twitter image
- **サイト名**: Open Graph site_name
- **ドメイン**: URLのドメイン部分

### スマートキャッシュシステム
- **7日間TTL**: DynamoDB自動削除機能
- **キャッシュ優先**: 既存データを優先使用
- **自動更新**: 期限切れ時の自動再取得
- **パフォーマンス**: 2回目以降の高速レスポンス

### エラーハンドリング
- **タイムアウト対応**: 15秒制限
- **接続エラー**: フォールバック情報
- **HTTPエラー**: ステータスコード別処理
- **コンテンツ検証**: HTML以外の除外

## 🤖 Amazon Q Developer の活用

このプロジェクトでAmazon Q Developerが生成した要素：

### 🏗️ インフラストラクチャ
- AWS CDK スタック設計 (3スタック)
- DynamoDB テーブル設計 (3テーブル + GSI + TTL)
- Cognito User Pool設定
- API Gateway HTTP API設定
- Lambda関数設定 (7関数)

### 💻 コード生成
- TypeScript CDK コード
- Python Lambda関数 (Web scraping付き)
- 環境設定管理
- デプロイスクリプト
- エラーハンドリング

### 📚 ドキュメント
- README.md (完全版)
- アーキテクチャ図 (4種類)
  - Mermaid形式
  - ASCII形式
  - draw.io形式
  - テキスト形式
- API仕様書
- デプロイ手順

### 🔧 設定ファイル
- package.json
- tsconfig.json
- cdk.json
- .gitignore
- requirements.txt (複数)

## 🏷️ タグ情報

全てのAWSリソースに以下のタグが自動付与されます：
- `Project`: UrlShortener
- `Environment`: dev/staging/prod
- `BuiltWith`: Amazon-Q-Developer
- `CreatedBy`: Amazon-Q-Developer-AI-Assistant
- `Feature`: URL-Info-Enhanced

## 🚀 パフォーマンス

### レスポンス時間
- **キャッシュヒット**: ~100ms
- **新規取得**: ~2-5秒 (外部サイト依存)
- **リダイレクト**: ~50ms

### スケーラビリティ
- **Lambda**: 自動スケーリング
- **DynamoDB**: オンデマンド課金
- **API Gateway**: 無制限リクエスト

## 🤝 コントリビューション

このプロジェクトはAmazon Q Developerによって生成されましたが、改善提案やバグ報告は歓迎します。

1. このリポジトリをフォーク
2. フィーチャーブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add some amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は [LICENSE](LICENSE) ファイルを参照してください。

## 📞 サポート

質問や問題がある場合は、[Issues](https://github.com/weitanglo/url-shortener-cdk/issues) を作成してください。

## 🎯 ロードマップ

### Phase 3: UI/UX強化 (計画中)
- [ ] React/Vue.js フロントエンド
- [ ] リアルタイムプレビュー
- [ ] 画像最適化・リサイズ
- [ ] 統計ダッシュボード
- [ ] バルクURL処理

### Phase 4: エンタープライズ機能 (将来)
- [ ] チーム管理機能
- [ ] API レート制限
- [ ] 高度な分析
- [ ] カスタムブランディング

---

**🤖 Powered by Amazon Q Developer**  
*AI-Generated Serverless Application with Enhanced URL Information Features*

[![Amazon Q Developer](https://img.shields.io/badge/Generated%20by-Amazon%20Q%20Developer-FF9900?style=for-the-badge&logo=amazon-aws)](https://aws.amazon.com/q/developer/)

**🌟 Phase 2 Enhanced - URL情報自動取得機能付き**

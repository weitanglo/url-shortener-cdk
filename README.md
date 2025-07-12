# URL Shortener Service

> **🤖 Built with Amazon Q Developer**  
> このプロジェクトは完全にAmazon Q Developer AI Assistantによって作成されました。

[![Built with Amazon Q Developer](https://img.shields.io/badge/Built%20with-Amazon%20Q%20Developer-FF9900?style=flat-square&logo=amazon-aws)](https://aws.amazon.com/q/developer/)
[![AWS CDK](https://img.shields.io/badge/AWS-CDK-FF9900?style=flat-square&logo=amazon-aws)](https://aws.amazon.com/cdk/)
[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=flat-square&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Serverless](https://img.shields.io/badge/Serverless-FD5750?style=flat-square&logo=serverless&logoColor=white)](https://www.serverless.com/)

AWS CDK (TypeScript) で構築されたサーバーレスURL短縮サービスです。

## 🏗️ アーキテクチャ

📊 **[詳細なアーキテクチャ図を見る](./ARCHITECTURE.md)**  
🎨 **[ASCII版アーキテクチャ図を見る](./ARCHITECTURE_ASCII.md)**

### 技術スタック
- **フレームワーク**: AWS CDK (TypeScript)
- **認証**: Amazon Cognito User Pool
- **API**: API Gateway HTTP API
- **コンピュート**: AWS Lambda (Python 3.10)
- **データベース**: Amazon DynamoDB
- **ドメイン**: Route53 + ACM
- **開発**: Amazon Q Developer AI Assistant

### システム概要図
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Database   │    │  Security   │    │     API     │
│    Stack    │    │    Stack    │    │    Stack    │
├─────────────┤    ├─────────────┤    ├─────────────┤
│ DynamoDB    │    │ Cognito     │    │ API Gateway │
│ - URLs      │    │ User Pool   │    │ HTTP API    │
│ - Users     │    │ IAM Roles   │    │ 6x Lambda   │
│ - GSI       │    │ JWT Auth    │    │ Custom DNS  │
└─────────────┘    └─────────────┘    └─────────────┘
```

### 主要機能
- URL短縮・管理
- ユーザー認証・認可 (Cognito)
- カスタムドメイン対応
- リアルタイムリダイレクト
- 環境別デプロイ (dev/staging/prod)

## 🚀 Amazon Q Developer による開発

このプロジェクトの特徴：
- **100% AI生成**: 全てのコード、設定、ドキュメントがAmazon Q Developerによって生成
- **ベストプラクティス**: AWS CDKとサーバーレスアーキテクチャのベストプラクティスを適用
- **モダンな技術スタック**: TypeScript、Python、AWS最新サービスを活用

## プロジェクト構成

```
url-shortener-cdk/
├── bin/
│   └── url-shortener-cdk.ts     # CDK アプリエントリーポイント
├── lib/
│   ├── stacks/
│   │   ├── database-stack.ts    # DynamoDB テーブル
│   │   ├── security-stack.ts    # Cognito + IAM
│   │   └── api-stack.ts         # API Gateway + Lambda
│   └── constructs/
│       └── lambda-function.ts   # Lambda関数 Construct
├── lambda/                      # Lambda関数ソースコード
│   ├── createurl/              # URL作成
│   ├── geturls/                # URL一覧取得
│   ├── deleteurl/              # URL削除
│   ├── redirect/               # リダイレクト
│   ├── signup/                 # ユーザー登録
│   ├── login/                  # ログイン
│   └── Layer/                  # 共有ライブラリ
├── config/
│   └── config.ts               # 環境別設定
├── ARCHITECTURE.md             # 詳細アーキテクチャ図
├── ARCHITECTURE_ASCII.md       # ASCII版アーキテクチャ図
└── test/                       # テストファイル
```

## 🚀 クイックスタート

### 前提条件
- Node.js 18+
- AWS CLI 設定済み
- AWS CDK CLI インストール済み

### インストール
```bash
git clone https://github.com/your-username/url-shortener-cdk.git
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
# データベースのみ
npx cdk deploy UrlShortener-Database-dev

# セキュリティのみ (Cognito)
npx cdk deploy UrlShortener-Security-dev

# APIのみ
npx cdk deploy UrlShortener-Api-dev
```

## API エンドポイント

| メソッド | パス | 説明 | 認証 |
|---------|------|------|------|
| POST | `/signup` | ユーザー登録 (Cognito) | なし |
| POST | `/login` | ログイン (Cognito) | なし |
| POST | `/createurl` | URL短縮 | 必要 |
| GET | `/geturls` | URL一覧取得 | 必要 |
| DELETE | `/deleteurl/{id}` | URL削除 | 必要 |
| GET | `/{shortCode}` | リダイレクト | なし |

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

## セキュリティ

- Amazon Cognito User Pool による認証
- JWT トークンベースの認可
- IAM ロールベースのアクセス制御
- HTTPS 強制 (ACM証明書)
- 環境別リソース分離

## モニタリング

- CloudWatch Logs (Lambda)
- X-Ray トレーシング
- DynamoDB メトリクス
- API Gateway メトリクス

## 🤖 Amazon Q Developer の活用

このプロジェクトでAmazon Q Developerが生成した要素：

### 🏗️ インフラストラクチャ
- AWS CDK スタック設計
- DynamoDB テーブル設計 (GSI含む)
- Cognito User Pool設定
- API Gateway HTTP API設定
- Lambda関数設定

### 💻 コード生成
- TypeScript CDK コード
- Lambda関数構成
- 環境設定管理
- デプロイスクリプト

### 📚 ドキュメント
- README.md
- アーキテクチャ図 (Mermaid + ASCII)
- API仕様書
- デプロイ手順

### 🔧 設定ファイル
- package.json
- tsconfig.json
- cdk.json
- .gitignore

## 🏷️ タグ情報

全てのAWSリソースに以下のタグが自動付与されます：
- `Project`: UrlShortener
- `Environment`: dev/staging/prod
- `BuiltWith`: Amazon-Q-Developer
- `CreatedBy`: Amazon-Q-Developer-AI-Assistant

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

質問や問題がある場合は、[Issues](https://github.com/your-username/url-shortener-cdk/issues) を作成してください。

---

**🤖 Powered by Amazon Q Developer**  
*AI-Generated Serverless Application*

[![Amazon Q Developer](https://img.shields.io/badge/Generated%20by-Amazon%20Q%20Developer-FF9900?style=for-the-badge&logo=amazon-aws)](https://aws.amazon.com/q/developer/)

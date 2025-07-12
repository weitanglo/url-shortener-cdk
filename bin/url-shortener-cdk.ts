#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { DatabaseStack } from '../lib/stacks/database-stack';
import { SecurityStack } from '../lib/stacks/security-stack';
import { ApiStack } from '../lib/stacks/api-stack';
import { getConfig } from '../config/config';

const app = new cdk.App();

// Get stage from context or default to 'dev'
const stage = app.node.tryGetContext('stage') || 'dev';
const config = getConfig(stage);

const env = {
  account: process.env.CDK_DEFAULT_ACCOUNT,
  region: config.region,
};

// Database Stack (拡張版)
const databaseStack = new DatabaseStack(app, `UrlShortener-Database-${config.stageName}`, {
  env,
  stageName: config.stageName,
});

// Security Stack
const securityStack = new SecurityStack(app, `UrlShortener-Security-${config.stageName}`, {
  env,
  stageName: config.stageName,
  senderEmail: config.senderEmail,
  urlShortnerTableArn: databaseStack.urlShortnerTable.tableArn,
  userTableArn: databaseStack.userTable.tableArn,
});

// API Stack (includes Lambda functions + URL Info features)
const apiStack = new ApiStack(app, `UrlShortener-Api-${config.stageName}`, {
  env,
  stageName: config.stageName,
  subDomain: config.subDomain,
  hostedZoneId: config.hostedZoneId,
  domainName: config.domainName,
  senderEmail: config.senderEmail,
  emailRegion: config.region,
  userPool: securityStack.userPool,
  userPoolClient: securityStack.userPoolClient,
  lambdaRole: securityStack.lambdaRole,
  urlShortnerTable: databaseStack.urlShortnerTable,
  userTable: databaseStack.userTable,
  urlInfoTable: databaseStack.urlInfoTable, // 新規追加
});

// Stack dependencies
securityStack.addDependency(databaseStack);
apiStack.addDependency(securityStack);

// Tags - Built with Amazon Q Developer
cdk.Tags.of(app).add('Project', 'UrlShortener');
cdk.Tags.of(app).add('Environment', config.stageName);
cdk.Tags.of(app).add('BuiltWith', 'Amazon-Q-Developer');
cdk.Tags.of(app).add('CreatedBy', 'Amazon-Q-Developer-AI-Assistant');
cdk.Tags.of(app).add('Feature', 'URL-Info-Enhanced'); // 新機能タグ

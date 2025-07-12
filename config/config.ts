export interface AppConfig {
  stageName: string;
  region: string;
  subDomain: string;
  hostedZoneId: string;
  domainName: string;
  senderEmail: string;
}

export const getConfig = (stage: string = 'dev'): AppConfig => {
  const configs: { [key: string]: AppConfig } = {
    dev: {
      stageName: 'dev',
      region: 'ap-northeast-1',
      subDomain: 'url-dev.loweitang.com', // 開発環境用サブドメイン
      hostedZoneId: 'Z06146261K6JRFZIWWUX1',
      domainName: 'loweitang.com',
      senderEmail: 'low.texeg@gmail.com',
    },
    staging: {
      stageName: 'staging',
      region: 'ap-northeast-1',
      subDomain: 'url-staging.loweitang.com',
      hostedZoneId: 'Z06146261K6JRFZIWWUX1',
      domainName: 'loweitang.com',
      senderEmail: 'low.texeg@gmail.com',
    },
    prod: {
      stageName: 'prod',
      region: 'ap-northeast-1',
      subDomain: 'url.loweitang.com',
      hostedZoneId: 'Z06146261K6JRFZIWWUX1',
      domainName: 'loweitang.com',
      senderEmail: 'low.texeg@gmail.com',
    },
  };

  return configs[stage] || configs.dev;
};

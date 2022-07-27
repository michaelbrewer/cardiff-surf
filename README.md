# Cardiff Twitter Bot

Create a simple serverless bot that publishes news for the Cardiff area. 

Read [CDK Guide](cdk/README.md) on how to deploy to your own account.

## TODO

- [x] Create a new twitter account for the bot and add mobile phone to it
- [x] Create a new developer account and get the api key, api key secret and bearer token
- [x] Create oauth 1.0a with write accesss
- [x] Generate access token and access token secret
- [x] Store credentials in AWS SSM Parameter Store
- [x] Initial test code
- [x] Create basic CDK app that builds and deploys the lambda with lambda layer
- [x] Test initial version via console
- [x] Add logic to fetch credentials from parameter store
- [x] Add logic to scrape news and tweet
- [x] Add basic docs
- [x] Add tracing, logs and metrics
- [ ] Setup CI/CD
- [ ] Add some unit testing
- [ ] Add architecture docs (highlights IAC, Security, Patching, Cost, Reliabilty, Observability)
- [ ] Final polish (add linting, formatters and security scans)

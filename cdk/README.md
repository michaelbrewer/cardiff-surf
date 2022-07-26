
# Welcome to your CDK Python project!

You should explore the contents of this project. It demonstrates a CDK app with an instance of a stack (`cdk_stack`)
which contains an Amazon SQS queue that is subscribed to an Amazon SNS topic.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

```shell
$ make dev
```

At this point you can now synthesize the CloudFormation template for this code.

```shell
$ cdk synth
```

You can now begin exploring the source code, contained in the hello directory.
There is also a very trivial test included that can be run like this:

```shell
$ make test
```

To add additional dependencies, for example other CDK libraries, just add via `poetry add name` or for development dependencies
`poetry add -D name`.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!

## Setting up the Twitter credentials

* [How to get started with the Twitter API in 2022
](https://medium.com/@yassinetahri/how-to-get-started-with-the-twitter-api-in-2022-34b8f1d0d73a)
* Create a new SSM parameter called `/projects/cardiff/twitter`
* Select `SecureString` as the type
* Use the default KMS key (`alias/aws/ssm`)
* Value should be a json string like

```json
{
   "api_key":"TWITTER_API_KEY",
   "api_key_secret":"TWITTER_API_KEY_SECRET",
   "bearer_token":"TWITTER_BEARER_TOKEN",
   "access_token":"TWITTER_ACCESS_TOKEN",
   "access_token_secret":"TWITTER_ACCESS_TOKEN_SECRET"
}
```

* Get the key id for `alias/aws/ssm`

```shell
aws kms describe-key --key-id=alias/aws/ssm | jq ".KeyMetadata.KeyId"
```

* Set the KMS Key as a CDK context value

```shell
cdk synth -c ssm_kms_key_id=KMS_KEY_ID
```

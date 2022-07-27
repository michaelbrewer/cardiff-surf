from inspect import stack
from constructs import Construct
from aws_cdk import (
    BundlingOptions,
    Duration,
    Stack,
    aws_lambda,
    aws_iam,
    aws_kms,
    aws_events,
    aws_events_targets,
)


class CdkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        function = aws_lambda.Function(
            self,
            id="cardiffBot",
            description="Twitter bot that published Cardiff related updates",
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            handler="app.handler",
            timeout=Duration.seconds(25),
            memory_size=512,
            architecture=aws_lambda.Architecture.ARM_64,
            tracing=aws_lambda.Tracing.ACTIVE,
            code=aws_lambda.Code.from_asset(
                path="../src/",
                bundling=BundlingOptions(
                    image=aws_lambda.Runtime.PYTHON_3_9.bundling_image,
                    command=[
                        "bash",
                        "-c",
                        "pip install -r requirements.txt -t /asset-output && cp -au . /asset-output",
                    ],
                ),
            ),
            environment={
                "LOG_LEVEL": "DEBUG",
                "POWERTOOLS_SERVICE_NAME": "cardiff-bot",
                "POWERTOOLS_METRICS_NAMESPACE": "cardiff",
                "POWERTOOLS_TRACE_MIDDLEWARES": "true",
                "POWERTOOLS_TRACER_CAPTURE_RESPONSE": "true",
                "POWERTOOLS_TRACER_CAPTURE_ERROR": "true",
                "POWERTOOLS_LOGGER_LOG_EVENT": "true",
            },
        )

        ssm_kms_arn = self.format_arn(
            service="kms",
            resource="key",
            resource_name=self.node.try_get_context("ssm_kms_key_id"),
        )
        key = aws_kms.Key.from_key_arn(self, "ssmKmsKey", ssm_kms_arn)
        key.grant_decrypt(function)

        # Grant lambda access to twitter and stormglass credentials
        credentials_path_arn = self.format_arn(
            service="ssm",
            resource="parameter",
            resource_name="projects/cardiff/*",
        )
        function.role.add_to_principal_policy(
            aws_iam.PolicyStatement(
                actions=["ssm:GetParameter"],
                resources=[credentials_path_arn],
            )
        )

        aws_events.Rule(
            self,
            "ScheduleBot",
            description="Run the Cardiff bot on an hourly basis",
            schedule=aws_events.Schedule.cron(hour="14,16,18,20,23,0,2", minute="0"),
            targets=[aws_events_targets.LambdaFunction(function)],
        )

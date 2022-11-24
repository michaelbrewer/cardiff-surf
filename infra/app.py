import aws_cdk as cdk
from stacks.cdk_stack import CdkStack

app = cdk.App()
CdkStack(app, "cardiff")
cdk.Tags.of(app).add("project", "cardiff-bot")
cdk.Tags.of(app).add("environment", "production")
app.synth()

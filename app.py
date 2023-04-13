from aws_cdk import (
    aws_s3 as s3,
    lambda as _lambda,
    App, Stack
)

from my_custom_resource import MyCustomResource

class OpStack(Stack):
    def __init__(self, scope: App, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        bucket = s3.Bucket(self, "CustomResourceBucket",
                           encryption=s3.BucketEncryption.S3_MANAGED, block_public_access=s3.BlockPublicAccess.BLOCK_ALL)
        
        resource = MyCustomResource(
            self, "MyCustomResource",
            bucket_name=bucket.bucket_name
        )

app = App()
OpStack(app, "CustomrResourceOpstack")
app.synth()
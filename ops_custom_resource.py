from aws_cdk import (
    aws_logs as logs,
)

from aws_cdk.custom_resources import (
    AwsCustomResource,
    AwsCustomResourcePolicy,
    PhysicalResourceId,
    AwsSdkCall
)

from constructs import Construct

class MyCustomResource(Construct):

    def __init__(self, scope: Construct, id: str, bucket_name):
        super().__init__(scope, id)

        res = AwsCustomResource(
            scope=self,
            id='AWSCustomResource',
            policy=AwsCustomResourcePolicy.from_sdk_calls(resources=[f'arn:aws:s3:::{bucket_name}/*']),
            log_retention=logs.RetentionDays.INFINITE,
            on_create=self.create(bucket_name),
            on_delete=self.delete(bucket_name),
            resource_type='Custom::MyCustomResource'
        )
    
    def create(self, bucket_name):

        create_params = {
            "Body": "Ops world", # This is the content of the file
            "Bucket": bucket_name,
            "Key": "OpsWorld.txt"
        }

        return AwsSdkCall(
            action='putObject',
            service='S3',
            parameters=create_params,
            physical_resource_id=PhysicalResourceId.of('myAutomationExecution')

        )

    def delete(self, bucket_name):

        delete_params = {
           "Bucket": bucket_name,
           "Key": "OpsWorld.txt"
        }
        return AwsSdkCall(
            action='deleteObject',
            service='S3',
            parameters=delete_params,
            physical_resource_id=PhysicalResourceId.of('myAutomationExecution')
        )
    

    # the benfit of a custom resource is that you can use the same code to create and delete the resource
    # in this case, the resource is a file in an S3 bucket
    # why it is create as a custom resource is because the CDK does not have a construct for S3 objects
    # so we have to create it ourselves
    # the custom resource is a wrapper around the AWS SDK
    
    # 
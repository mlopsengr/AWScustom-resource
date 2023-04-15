use aws_cdk::{
    aws_logs::logs,
};

use aws_cdk::custom_resources::{
    AwsCustomResource,
    AwsCustomResourcePolicy,
    PhysicalResourceId,
    AwsSdkCall
};

use constructs::Construct;

struct MyCustomResource<'a> {
    scope: Construct,
    id: str,
    bucket_name: str,
}

impl<'a> MyCustomResource<'a> {
    fn new<'a>(scope: Construct, id: str, bucket_name: str) -> Self {
        super::new(scope, id)
        self.bucket_name = bucket_name
    }

    fn create<'a>(self, bucket_name: str) {

        let create_params = {
            "Body": "Ops world", // This is the content of the file
            "Bucket": bucket_name,
            "Key": "OpsWorld.txt"
        };

        return AwsSdkCall::new(
            action='putObject',
            service='S3',
            parameters=create_params,
            physical_resource_id=PhysicalResourceId.of('myAutomationExecution')

        );

    }

    fn delete<'a>(self, bucket_name: str) {

        let delete_params = {
           "Bucket": bucket_name,
           "Key": "OpsWorld.txt"
        };
        return AwsSdkCall::new(
            action='deleteObject',
            service='S3',
            parameters=delete_params,
            physical_resource_id=PhysicalResourceId.of('myAutomationExecution')
        );
    }
}

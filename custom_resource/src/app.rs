use aws_cdk::core::Stack;
use aws_cdk::aws_s3::{Bucket, BlockPublicAccess, BucketEncryption};
use main::MyCustomResource;

struct OpStack<'a> {
    scope: &'a App<'a>,
    id: &'a str,
    props: Option<StackProps<'a>>,
}

impl<'a> Stack for OpStack<'a> {
    fn new(scope: &'a App<'a>, id: &'a str, props: Option<StackProps<'a>>) -> Self {
        let bucket = Bucket::new(scope, "CustomResourceBucket",
            BucketProps {
                encryption: BucketEncryption::S3Managed,
                block_public_access: BlockPublicAccess::BlockAll,
                ..Default::default()
            }
        );

        let resource = MyCustomResource::new(scope, "MyCustomResource",
            MyCustomResourceProps {
                bucket_name: bucket.bucket_name,
                ..Default::default()
            }
        );

        OpStack {
            scope,
            id,
            props,
        }
    }
}

fn main() {
    let app = App::new();
    OpStack::new(app, "CustomResourceOpstack", None);
    app.synth();
}
provider "aws" {
  region = "ap-south-1"
}

data "aws_availability_zones" "available" {}

data "aws_eks_cluster" "cluster" {
  name = module.eks.cluster_id
}

data "aws_eks_cluster_auth" "cluster" {
  name = module.eks.cluster_id
}

locals {
  cluster_name = "assimilatek8s"
}

provider "kubernetes" {
  host                   = data.aws_eks_cluster.cluster.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.cluster.certificate_authority.0.data)
  token = data.aws_eks_cluster_auth.cluster.token
}

module "eks-kubeconfig" {
    source = "hyperbadger/eks-kubeconfig/aws"
    version = "1.0.0"

    depends_on = [ module.ks]
    cluster_id = moduel.eks.cluster_id
  
}
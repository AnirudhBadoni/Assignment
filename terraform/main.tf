provider "aws" {
  region = "us-east-1"
}

# Get the default VPC
data "aws_vpc" "default" {
  default = true
}

# Get all existing subnets in the default VPC
data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# Create a new subnet if necessary
resource "aws_subnet" "default" {
  vpc_id     = data.aws_vpc.default.id
  cidr_block = cidrsubnet(data.aws_vpc.default.cidr_block, 8, length(data.aws_subnets.default.ids))
  map_public_ip_on_launch = true

  tags = {
    Name = "Default-Subnet"
  }
}

# Create a security group for PostgreSQL communication
resource "aws_security_group" "postgres_sg" {
  name        = "postgres_sg"
  description = "Allow PostgreSQL communication between instances"
  vpc_id      = data.aws_vpc.default.id
  
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Allow SSH from anywhere (update as needed)
  }
  
  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/8"] # Adjust to your needs
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "tls_private_key" "ssh_key" {
  algorithm = "RSA"
  rsa_bits  = 2048
}

resource "local_file" "private_key" {
  content  = tls_private_key.ssh_key.private_key_pem
  filename = "${path.module}/private_key.pem"  # Save in the current working directory
}

output "private_key_path" {
  value     = local_file.private_key.filename
  sensitive = true
}


# Primary instance
resource "aws_instance" "primary" {
  ami           = "ami-0c94855ba95c71c99"  # Amazon Linux 2 AMI
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.default.id  # Use dynamically created subnet
  vpc_security_group_ids = [aws_security_group.postgres_sg.id] # Use vpc_security_group_ids
  tags = {
    Name = "PostgreSQL-Primary"
  }

  user_data = <<-EOF
              #!/bin/bash
              echo "Configuring primary instance"
              yum update -y
              yum install -y postgresql
              # Configure PostgreSQL for replication on the primary
              EOF
}

# Replica instances

resource "aws_instance" "replica_1" {
  ami           = "ami-0c94855ba95c71c99"  # Amazon Linux 2 AMI
  instance_type = "t2.micro"
  subnet_id     = aws_subnet.default.id
  vpc_security_group_ids = [aws_security_group.postgres_sg.id] # Use vpc_security_group_ids
  tags = {
    Name = "PostgreSQL-Replica-1"
  }

  user_data = <<-EOF
              #!/bin/bash
              echo "Configuring replica instance 1"
              yum update -y
              yum install -y postgresql
              # Configure PostgreSQL for replication on the replica
              EOF
}

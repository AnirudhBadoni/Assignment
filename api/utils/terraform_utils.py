import subprocess
from jinja2 import Template

def generate_terraform(params):
    """
    Generate Terraform configuration file dynamically using Jinja2.
    """
    template_file = "api/templates/terraform.j2"
    output_file = "terraform/main.tf"

    # Read and render the Jinja2 template
    with open(template_file, "r") as f:
        template = Template(f.read())

    terraform_code = template.render(
        instance_type=params["instance_type"],
        num_replicas=params["num_replicas"]
    )

    # Save the rendered Terraform code
    with open(output_file, "w") as f:
        f.write(terraform_code)

    return terraform_code


def run_terraform():
    """
    Execute Terraform commands to provision infrastructure.
    """
    try:
        # Initialize Terraform
        subprocess.run(["terraform", "init"], cwd="terraform", check=True)

        # Plan Terraform changes
        subprocess.run(["terraform", "plan"], cwd="terraform", check=True)

        # Apply Terraform changes
        subprocess.run(["terraform", "apply", "-auto-approve"], cwd="terraform", check=True)
        return True, "Terraform applied successfully"
    except subprocess.CalledProcessError as e:
        return False, str(e)

    private_key_path = "../../terraform/private_key.pem"
    if os.path.exists(private_key_path):
        os.chmod(private_key_path, 0o400)  # Restrict permissions
        print(f"Updated permissions for {private_key_path}")
    else:
        print(f"Key file not found at {private_key_path}")
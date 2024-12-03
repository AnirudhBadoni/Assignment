import subprocess
from jinja2 import Template

def generate_ansible_inventory(instances):
    """
    Generate an Ansible inventory file based on EC2 instance information.
    """
    inventory_file = "ansible/inventory.ini"
    with open(inventory_file, "w") as f:
        f.write("[primary]\n")
        f.write(f"{instances['primary']}\n\n")
        f.write("[replicas]\n")
        for replica in instances["replicas"]:
            f.write(f"{replica}\n")
    return inventory_file

def run_ansible():
    """
    Execute Ansible playbook to configure PostgreSQL on instances.
    """
    try:
        # Run the Ansible playbook
        subprocess.run(
            [
                "ansible-playbook",
                "-i",
                "ansible/inventory.ini",
                "ansible/playbooks/install_postgres.yml",
            ],
            check=True,
        )
        return True, "Ansible playbook executed successfully"
    except subprocess.CalledProcessError as e:
        return False, str(e)

import pulumi
import pulumi_aws as aws

# 1. VPC Soberana (O Bunker)
vpc = aws.ec2.Vpc("ghost-vpc",
    cidr_block="10.0.0.0/16",
    enable_dns_hostnames=True,
    tags={
        "Name": "ghost-protocol-vpc", 
        "Methodology": "Hardened-by-Design"
    })

# Subnet Privada (Onde o Monge medita)
subnet = aws.ec2.Subnet("ghost-private-subnet",
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/24",
    tags={"Name": "ghost-private-subnet"})

# 2. Security Group (Muralha Zero-Trust)
sg = aws.ec2.SecurityGroup("ghost-ollama-sg",
    vpc_id=vpc.id,
    description="Acesso interno para Ollama",
    ingress=[aws.ec2.SecurityGroupIngressArgs(
        protocol="tcp", 
        from_port=11434, 
        to_port=11434, 
        cidr_blocks=[vpc.cidr_block] # Apenas interno!
    )],
    egress=[aws.ec2.SecurityGroupEgressArgs(
        protocol="-1", 
        from_port=0, 
        to_port=0, 
        cidr_blocks=["0.0.0.0/0"]
    )])

# 3. Spot Instance (FinOps: 70-80% de economia)
ami = aws.ec2.get_ami(most_recent=True, owners=["137112412989"],
    filters=[aws.ec2.GetAmiFilterArgs(name="name", values=["amzn2-ami-hvm-*-x86_64-gp2"])])

launch_template = aws.ec2.LaunchTemplate("ghost-template",
    image_id=ami.id,
    instance_type="t3.small", # Econômica para teste
    instance_market_options=aws.ec2.LaunchTemplateInstanceMarketOptionsArgs(
        market_type="spot"
    ),
    network_interfaces=[aws.ec2.LaunchTemplateNetworkInterfaceArgs(
        device_index=0, 
        security_groups=[sg.id], 
        subnet_id=subnet.id
    )])

# 4. Auto Scaling Group com Automação de Custo
asg = aws.autoscaling.Group("ghost-asg",
    max_size=1, 
    min_size=1, 
    desired_capacity=1,
    vpc_zone_identifiers=[subnet.id],
    launch_template=aws.autoscaling.GroupLaunchTemplateArgs(
        id=launch_template.id, 
        version="$Latest"
    ))

# Automação: Desligar Sexta às 22h (Hoje!)
aws.autoscaling.Schedule("stop-weekend",
    scheduled_action_name="StopForWeekend",
    min_size=0, 
    max_size=0, 
    desired_capacity=0,
    recurrence="0 22 * * 5", 
    autoscaling_group_name=asg.name)

# Exportando para o seu relatório de auditoria
pulumi.export("vpc_id", vpc.id)
pulumi.export("asg_name", asg.name)
resource "openstack_compute_keypair_v2" "my-key" {
  name       = "team-key"
  public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC1DF41tHVYH4KQ0vCKgswMp19ynVoZ9E0PJZ2NF2/vtXY5pD/BVQ0fZuz1S27rsm5wJrdpxtzUj8UKrHlWaQcITK7yEpP9+cNQf5guHqOPlzZj4tgRR+O7poYJ4eCShsp2B0zE4l++9ELpN3DJdtJ0DDctk38a9WM2xoIFYW4w+Ovdsv5ghncaCHuVZ7u3PutcKVRobiBpXvOK8qmj0lS0UzXwrxNi1SLBRnCSjMT7urZmTzJhQSVVuWphJ2n+mdr+t8QYOC+ZDB+kvZqBI1PkXQ6acyMbMydkPib9M/uIevZc3RzWiHCrJdw4Bdt9sB07Wvzf6jCYVEZzhHisg9Dxd9I7kf2MTCup2+PhJGybav2KSAfNsRYhABNKc/P4+XnyX6d6SAe0U7iHoUFypgov" 
}

resource "openstack_compute_instance_v2" "VM_1" {
  name            = "vm1"
  image_name      = "Ubuntu-20.04"
  flavor_name     = "standard.small"
  key_pair        = "${openstack_compute_keypair_v2.my-key.name}"
  security_groups = [openstack_compute_secgroup_v2.secgroup_1.name]

  network {
    name = "project_200"
  }
}

resource "openstack_compute_instance_v2" "VM_2" {
  name            = "vm2"
  image_name      = "Ubuntu-20.04"
  flavor_name     = "standard.small"
  key_pair        = "${openstack_compute_keypair_v2.my-key.name}"
  security_groups = [openstack_compute_secgroup_v2.secgroup_2.name]

  network {
    name = "project_200"
  }
}

resource "openstack_networking_floatingip_v2" "fip_1" {
  pool = "public"
}

resource "openstack_compute_floatingip_associate_v2" "fip_1" {
  floating_ip = openstack_networking_floatingip_v2.fip_1.address
  instance_id = openstack_compute_instance_v2.VM_1.id
}

resource "openstack_compute_secgroup_v2" "secgroup_1" {
  name        = "SecGroup_1"
  description = "Security group for VM_1"

  rule {
    from_port   = 22
    to_port     = 22
    ip_protocol = "tcp"
    cidr        = "0.0.0.0/0"
  }

  rule {
    from_port   = 80
    to_port     = 80
    ip_protocol = "tcp"
    cidr        = "0.0.0.0/0"
  }

  rule {
    from_port   = 443
    to_port     = 443
    ip_protocol = "tcp"
    cidr        = "0.0.0.0/0"
  }

  rule {
    from_port   = 1
    to_port     = 65535
    ip_protocol = "tcp"
    cidr        = "192.168.1.0/24"
  }
}

resource "openstack_compute_secgroup_v2" "secgroup_2" {
  name        = "SecGroup_2"
  description = "Security group for VM_2"



  rule {
    from_port   = 1
    to_port     = 65535
    ip_protocol = "tcp"
    cidr        = "192.168.1.0/24"
  }
}  

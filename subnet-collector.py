from nornir import InitNornir
from nornir_netmiko import netmiko_send_command


def subnet_collect(task):
    """ Firstly, Creates a dictionary of all interfaces with IPs (interface_ip).
        Then uses that dictionary to obtain per interface IP subnet and mask information """
    interface_ip = {}
    host = task.host
    r1 = task.run(task=netmiko_send_command, command_string=f"show interface", use_genie=True)
    task.host["facts"] = r1.result
    for intf in task.host['facts']:
        if 'ipv4' in task.host['facts'][intf].keys():
            for ip_address in task.host['facts'][intf]['ipv4']:
                interface_ip.update({intf: ip_address})

    for interface in interface_ip:
        r2 = task.run(task=netmiko_send_command, command_string=f"show ip interface {interface} vrf all",
                      use_genie=True)
        task.host["facts"] = r2.result
        for intf in task.host['facts']:
            ip_subnet = task.host['facts'][intf]['ipv4'][interface_ip[intf]]['ip_subnet']
            prefix_length = task.host['facts'][intf]['ipv4'][interface_ip[intf]]['prefix_length']
            interface_state = task.host['facts'][intf]['interface_status']
            vrf = task.host['facts'][intf]['vrf']
            print(f'{host}, {intf}, {interface_state}, {vrf[:-3]}, {interface_ip[intf]}, {ip_subnet}/{prefix_length}')


nr = InitNornir(config_file='config.yaml')
nr.inventory.defaults.username = input("Enter your Username: ")
nr.inventory.defaults.password = input("Enter your Password: ")
print("Host, Interface, Int_State, VRF, IP, subnet")
nr.run(task=subnet_collect)

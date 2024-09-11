import argparse
import ipaddress
import psutil
import subprocess

def install_dependencies():
    """
    \brief  Install package dependencies
    \param  None
    \return None
    """
    
    # Dependencies
    required_packages = ["iptables"]

    command = ['sudo', 'apt', 'install'] + required_packages

    try:
        print(f"Installing packages: {', '.join(required_packages)}...")
        subprocess.check_call(command)
        print("Packages installed successfully.")
    
    except subprocess.CalledProcessError as e:
        print(f"Failed to install packages: {e}")

def enable_packet_forwarding():
    """
    \brief  Enable packet forward for client or clients
    \param  None
    \return None
    """

    command = ['sudo', 'sysctl', '-w', 'net.ipv4.ip_forward=1']
    
    # Execute the command
    try:
        print("Enabling packet forwarding...")
        subprocess.check_call(command)
        print("Packet forwarding enabled successfully...")

    except subprocess.CalledProcessError as e:
        print("Failed to enabling packet forwarding")
        exit(1)

def route_whole_network(net_interface, ip_addr):
    """
    \brief  The main routing function
    \param  The network interface that network packages routing to it
    \param  The ip address that network packages comes from
    \return None
    """
    
    # eg: sudo iptables -t nat -A POSTROUTING -o wlp4s0 -s 10.10.10.11 -j MASQUERADE
    ## -t (table)
    ## -A (rule to the chain)
    ## -o (network interface that whole network is going out)
    ## -s (ip address that whole network is coming in)
    ## -j (target)
    command = ['sudo', 'iptables', '-t', 'nat', '-A', 'POSTROUTING', '-o', net_interface, '-s', ip_addr, '-j', 'MASQUERADE']

    # Execute the command
    try:
        print(f"Routing whole network from {ip_addr} to {net_interface}...")
        subprocess.check_call(command)
        print("Routing network done successfully...")

    except subprocess.CalledProcessError as e:
        print("Failed to routing network")
        exit(1)

def get_args():
    """
    \brief  Get arguments and validate them
    \param  None
    \return The ip address
    \return The network interface
    """

    parser = argparse.ArgumentParser(description="A simple CLI for routing network packages")

    # Adding arguments
    parser.add_argument(
        '-n', '--net_interface', type=validate_net_interface, help='The network interface that is going out whole network', required=True)
    parser.add_argument(
        '-i', '--ip_address', type=validate_ip, help='The ip address that is going in whole network', required=True)

    # Parse the arguments
    args = parser.parse_args()

    ip_addr = args.ip_address
    net_interface = args.net_interface

    return ip_addr, net_interface

def validate_ip(ip_addr):
    """
    \brief  Validate ip address is available for IPv4 format
    \param  The ip address.
    \return The ip address
    """

    try:
        # Validate IPv4 address
        ipaddress.ip_address(ip_addr)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid IP address: {ip_addr}")
    
    return ip_addr

def validate_net_interface(net_interface):
    """
    \brief  Validate network interface that is correctly in system
    \param  The network interface name
    \return The network interface name
    """

    # Get a list of all network interface names
    interfaces = psutil.net_if_addrs().keys()

    if net_interface not in interfaces:
        raise argparse.ArgumentTypeError(f"Invalid network interface name: {net_interface}")
    
    return net_interface


def main():
    """
    \brief  The main function
    \param  None
    \return None
    """

    ip_addr, net_interface = get_args()
    install_dependencies()
    enable_packet_forwarding()
    route_whole_network(net_interface, ip_addr)

if __name__ == "__main__":
    main()
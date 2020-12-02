# dev-nornir-subnet-collector

Uses Nornir and Cisco Genie parser to do 2 things:
1. Creates a dictionary 'interface_ip' with all interfaces and IPs of all IPv4 enabled interfaces
2. Uses that dictionary to parse all IPv4 interfaces and obtain:
    * Interface State
    * VRF
    * Base Subnet and Mask
    
 Primarily to be used as a crude IPv4 auditing tool.
 
 TODO: Integrate with IPAM to maintain IPAM DB accuracy.
"""This profile sets up a simple LAN with selected node types.

Instructions:
Choose the nodes you desire and a small lan is created with them. """

# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg
# Import the Emulab specific extensions.
import geni.rspec.emulab as emulab

# Create a portal context.
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

# Client image list
imageList = [
    ('urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD', 'UBUNTU 22.04'),
    ('urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU20-64-STD', 'UBUNTU 20.04'),
]

# Do not change these unless you change the setup scripts too.
nfsServerName = "nfs"
nfsLanName    = "nfsLan"

# NFS Server Type (Source Server)
pc.defineParameter("serverType", "Source Server Type",
                   portal.ParameterType.STRING, "d710")

# NFS Client Type (Target Server)
pc.defineParameter("clientTypes", "Other Client Types",
                   portal.ParameterType.STRING, "xl170")

pc.defineParameter("osImage", "Select OS image for servers",
                   portal.ParameterType.IMAGE,
                   imageList[0], imageList)

# Always need this when using parameters
params = pc.bindParameters()

# The NFS server.
nfsServer = request.RawPC("snode")
nfsServer.disk_image = params.osImage
nfsServer.hardware_type = params.serverType
nfsServer.routable_control_ip = True

clientTypes = params.clientTypes.split(',')

ip_count = 2
ifaces = []

for c_type in clientTypes:
    nfsClient = request.RawPC("tnode-"+str(ip_count))
    nfsClient.disk_image = params.osImage
    nfsClient.hardware_type = c_type
    nfsClient.routable_control_ip = True
    ip_count = ip_count + 1

# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)

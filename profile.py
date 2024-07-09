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
nfsDirectory  = "/nfs"

# NFS Server Type (Source Server)
pc.defineParameter("serverType", "Source Server Type",
                   portal.ParameterType.STRING, "d710")

# NFS Client Type (Target Server)
pc.defineParameter("clientTypes", "Other Client Types",
                   portal.ParameterType.STRING, "xl170")

pc.defineParameter("osImage", "Select OS image for servers",
                   portal.ParameterType.IMAGE,
                   imageList[0], imageList)

pc.defineParameter("nfsSize", "Size of NFS Storage",
                   portal.ParameterType.STRING, "200GB",
                   longDescription="Size of disk partition to allocate on NFS server")

# Always need this when using parameters
params = pc.bindParameters()

# The NFS server.
nfsServer = request.RawPC("snode")
nfsServer.disk_image = params.osImage
nfsServer.hardware_type = params.serverType
nfsServer.routable_control_ip = True
# Attach server to lan.
iface0 = nfsServer.addInterface('interface-0', pg.IPv4Address('192.168.6.2','255.255.255.0'))
# Storage file system goes into a local (ephemeral) blockstore.
nfsBS = nfsServer.Blockstore("nfsBS", nfsDirectory)
nfsBS.size = params.nfsSize

clientTypes = params.clientTypes.split(',')

ip_count = 3
ifaces = []

for c_type in clientTypes:
    nfsClient = request.RawPC("tnode-"+str(ip_count))
    nfsClient.disk_image = params.osImage
    nfsClient.hardware_type = c_type
    nfsClient.routable_control_ip = True
    c_iface = nfsClient.addInterface('interface-'+str(ip_count), pg.IPv4Address('192.168.6.'+str(ip_count),'255.255.255.0'))
    ifaces.append(c_iface)
    ip_count = ip_count + 1


# The NFS network. All these options are required.
nfsLan = request.LAN(nfsLanName)
# Must provide a bandwidth. BW is in Kbps
nfsLan.bandwidth         = 100000
nfsLan.best_effort       = True
nfsLan.vlan_tagging      = True
nfsLan.link_multiplexing = True
nfsLan.addInterface(iface0)
for iface in ifaces:
    nfsLan.addInterface(iface)

# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)

from src.application.vpn.handlers import VPNHandlers
from src.config.config import settings
from src.infrastructure.openvpn.monitoring import TelnetMonitoringService
from src.infrastructure.openvpn.provisioning import ShellProvisioningService


def get_vpn_handlers() -> VPNHandlers:
    provisioning = ShellProvisioningService(base_dir="/opt/openvpn-scripts")
    monitoring = TelnetMonitoringService(
        host=settings.mgmt_address, port=settings.mgmt_port
    )
    return VPNHandlers(provisioning, monitoring)

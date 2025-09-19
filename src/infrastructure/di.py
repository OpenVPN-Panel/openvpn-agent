from src.application.vpn.handlers import VPNHandlers
from src.config.settings import settings
from src.infrastructure.openvpn.monitoring import TelnetMonitoringService
from src.infrastructure.openvpn.provisioning import ShellProvisioningService


def get_vpn_handlers() -> VPNHandlers:
    provisioning = ShellProvisioningService(
        base_dir=settings.scripts_dir,
        client_config_dir=settings.client_config_dir
    )
    monitoring = TelnetMonitoringService(
        host=settings.mgmt_address, port=settings.mgmt_port
    )
    return VPNHandlers(provisioning, monitoring)

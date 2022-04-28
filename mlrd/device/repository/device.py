from abc import ABC
from typing import List, Optional

from mlrd.device.domain import Device


class BaseDeviceRepository(ABC):
    pass


class DeviceRepository(BaseDeviceRepository):
    def __init__(self):
        super(DeviceRepository, self).__init__()

    def find(self, **kwargs) -> Optional[Device]:
        pass

    def find_all(self, **kwargs) -> List[Device]:
        pass

    def create(self, device: Device) -> Device:
        pass

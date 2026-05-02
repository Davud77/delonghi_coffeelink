"""Button platform for DeLonghi Coffee Link - one button per beverage."""
from __future__ import annotations

import logging

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import BEVERAGES, DOMAIN, MANUFACTURER
from .coordinator import DelonghiCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinators: list[DelonghiCoordinator] = hass.data[DOMAIN][entry.entry_id]
    entities: list[ButtonEntity] = []
    for coord in coordinators:
        entities.append(DelonghiWakeButton(coord))
        for bev_id, key, friendly, icon in BEVERAGES:
            entities.append(DelonghiStartBeverageButton(coord, bev_id, key, friendly, icon))
        entities.append(DelonghiStopButton(coord))
    async_add_entities(entities)


class _Base(CoordinatorEntity[DelonghiCoordinator], ButtonEntity):
    _attr_has_entity_name = True

    @property
    def device_info(self) -> DeviceInfo:
        d = self.coordinator.device
        return DeviceInfo(
            identifiers={(DOMAIN, d.dsn)},
            name=d.name or f"DeLonghi {d.dsn}",
            manufacturer=MANUFACTURER,
            model=d.oem_model or d.model,
            sw_version=d.sw_version,
            configuration_url=f"http://{d.lan_ip}" if d.lan_ip else None,
        )


class DelonghiStartBeverageButton(_Base):
    """Press to START a specific beverage."""

    def __init__(
        self,
        coord: DelonghiCoordinator,
        bev_id: int,
        key: str,
        friendly: str,
        icon: str,
    ) -> None:
        super().__init__(coord)
        self._bev_id = bev_id
        self._attr_unique_id = f"{coord.device.dsn}_start_{key}"
        # Ключ для файла переводов ru.json
        self._attr_translation_key = key 
        self._attr_icon = icon

    async def async_press(self) -> None:
        _LOGGER.info("Start beverage 0x%02x", self._bev_id)
        await self.coordinator.async_send_beverage(self._bev_id, 0x01)


class DelonghiWakeButton(_Base):
    """Wake the machine from standby."""

    def __init__(self, coord: DelonghiCoordinator) -> None:
        super().__init__(coord)
        self._attr_unique_id = f"{coord.device.dsn}_wake"
        self._attr_translation_key = "wake" # Связь с ru.json
        self._attr_icon = "mdi:power"

    async def async_press(self) -> None:
        _LOGGER.info("Sending WAKE to machine")
        await self.coordinator.async_send_wake()


class DelonghiStopButton(_Base):
    """Press to STOP currently-running beverage."""

    def __init__(self, coord: DelonghiCoordinator) -> None:
        super().__init__(coord)
        self._attr_unique_id = f"{coord.device.dsn}_stop"
        self._attr_translation_key = "stop" # Связь с ru.json
        self._attr_icon = "mdi:stop"

    async def async_press(self) -> None:
        _LOGGER.info("Generic stop command")
        await self.coordinator.async_send_beverage(0x10, 0x02)
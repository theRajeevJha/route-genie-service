from app.services.distance_provider import DistanceProvider
from app.services.ors_distance_provider import OpenRouteServiceDistanceProvider
from loguru import logger

class DistanceProviderFactory:
     _providers: dict[str, DistanceProvider] = {
        "ors": OpenRouteServiceDistanceProvider(),
        # Add other providers here as needed
    }
     
     @classmethod
     def get_providers(cls, name: str) -> DistanceProvider:
        if cls._providers.__contains__(name.lower()):
            logger.debug(f"DistanceProviderFactory will use `{name.lower()}` provider")
            return cls._providers.get(name.lower())
        else:
            logger.info(f"DistanceProviderFactory: No provider found for `{name}`. Defaulting to `ors` provider.")
            return cls._providers.get("ors")  # Default to ORS if not found
        
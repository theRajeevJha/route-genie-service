from app.services.SingleRouteGrouper import SingleRouteGrouper
from app.services.route_grouper import RouteGrouper
from loguru import logger

class RouteGrouperFactory:
    _providers: dict[str, RouteGrouper] = {
        "default": SingleRouteGrouper()
    }

    @classmethod
    def get_grouper(cls, name: str) -> RouteGrouper:
        if cls._providers.__contains__(name.lower()):
            logger.debug(f"RouteGrouperFactory will use `{name.lower()}` provider")
            return cls._providers.get(name.lower())
        else:
            logger.info(
                f"RouteGrouperFactory: No provider found for `{name}`. Defaulting to `SingleRouteGrouper` provider.")
            return cls._providers.get("default")
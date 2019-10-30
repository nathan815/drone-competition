from ..core.flight_control import FlightConfig
from .cli_main import start

if __name__ == '__main__':
    start(FlightConfig(db_write_data=False))

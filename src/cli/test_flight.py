from ..core.flight_config import FlightConfig
from .cli_main import run

if __name__ == '__main__':
    run(FlightConfig(db_write_data=False))

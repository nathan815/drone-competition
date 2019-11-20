from dataclasses import dataclass


@dataclass
class FlightConfig:
    continue_last_flight: bool = True
    show_video_window: bool = True
    db_write_data: bool = True
    print_positional_data: bool = True
    print_pilot_data: bool = True
    print_flight_data: bool = False
    print_unknown_events: bool = False
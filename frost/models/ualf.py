from typing import Any, Dict


class Ualf:
    def __init__(self, ualf_coordinates: str):
        self.read_ualf(ualf_coordinates)

    def read_ualf(self, ualf_coordinates: str) -> None:
        tokens = ualf_coordinates.strip().split()

        if len(tokens) < 25:
            raise ValueError(
                f"Incomplete UALF line: expected at least 25 fields, got {len(tokens)}"
            )

        try:
            self.version = int(tokens[0])
            self.year = int(tokens[1])
            self.month = int(tokens[2])
            self.day = int(tokens[3])
            self.hour = int(tokens[4])
            self.minutes = int(tokens[5])
            self.seconds = int(tokens[6])
            self.nanoseconds = int(tokens[7])
            self.latitude = float(tokens[8])
            self.longitude = float(tokens[9])
            self.peak_current = int(tokens[10])
            self.multiplicity = int(tokens[11])
            self.number_of_sensors = int(tokens[12])
            self.degrees_of_freedom = int(tokens[13])
            self.ellipse_angle = float(tokens[14])
            self.semi_major_axis = float(tokens[15])
            self.semi_minor_axis = float(tokens[16])
            self.chi_square_value = float(tokens[17])
            self.rise_time = float(tokens[18])
            self.peak_to_zero_time = float(tokens[19])
            self.max_rate_of_rise = float(tokens[20])
            self.cloud_indicator = int(tokens[21])
            self.angle_indicator = int(tokens[22])
            self.signal_indicator = int(tokens[23])
            self.timing_indicator = int(tokens[24])
            self.ualf_dict = self.make_ualf_dict()
        except (ValueError, IndexError) as e:
            raise ValueError(
                f"Error parsing UALF line: {ualf_coordinates}, Error: {e}"
            ) from e

    def make_ualf_dict(self) -> Dict[str, Any]:
        # Construct Epoch as ISO-8601 string with nanosecond precision
        epoch = f"{self.year:04}-{self.month:02}-{self.day:02}T{self.hour:02}:{self.minutes:02}:{self.seconds:02}.{self.nanoseconds:09}Z"  # noqa: E501
        point = [self.latitude, self.longitude]
        return {
            "Epoch": epoch,
            "Point": point,
            "CloudIndicator": self.cloud_indicator,
            "peak_current": self.peak_current,
            "Multiplicity": self.multiplicity,
            "number_of_sensors": self.number_of_sensors,
            "degrees_of_freedom": self.degrees_of_freedom,
            "ellipse_angle": self.ellipse_angle,
            "semi_major_axis": self.semi_major_axis,
            "semi_minor_axis": self.semi_minor_axis,
            "chi_square_value": self.chi_square_value,
            "rise_time": self.rise_time,
            "peak_to_zero_time": self.peak_to_zero_time,
            "max_rate_of_rise": self.max_rate_of_rise,
            "angle_indicator": self.angle_indicator,
            "signal_indicator": self.signal_indicator,
            "timing_indicator": self.timing_indicator,
        }

    def parse(self) -> Dict[str, Any]:
        return self.ualf_dict

    def print_ualf(self) -> None:
        print(self.ualf_dict)

from typing import TYPE_CHECKING, Any, List

import pandas as pd

if TYPE_CHECKING:
    from frost.entities import (
        ReportDut,
        ReportHumidityConstants,
        ReportIdf,
        ReportNormals,
        ReportStationRecords,
        ReportTemperatureConstants,
        ReportWindrose,
    )

from frost.entities import BaseEntity
from frost.models import ReportsAvailableResponse


class ReportsAvailable(BaseEntity[ReportsAvailableResponse]):
    def normalize_json(self) -> pd.DataFrame:
        """
        Normalizes the JSON data into a single DataFrame by combining data for all
        report types.

        :return pd.DataFrame: Combined DataFrame for all reports.
        """
        if self.data is None:
            return pd.DataFrame()

        normalized_data = {}

        # DUT
        if self.data.dut:
            dut = ReportDut(data=self._convert_to_report_response(self.data.dut))
            normalized_data["DUT"] = dut.normalize_json()

        # Humidity Constants
        if self.data.humidity_constants:
            humidity_constants = ReportHumidityConstants(
                data=self._convert_to_report_response(self.data.humidity_constants)
            )
            normalized_data["HumidityConstants"] = humidity_constants.normalize_json()

        # IDF
        if self.data.idf:
            idf = ReportIdf(data=self._convert_to_report_response(self.data.idf))
            normalized_data["IDF"] = idf.normalize_json()

        # Normals
        if self.data.normals:
            normals = ReportNormals(
                data=self._convert_to_report_response(self.data.normals)
            )
            normalized_data["Normals"] = normals.normalize_json()

        # Station Records
        if self.data.station_records:
            station_records = ReportStationRecords(
                data=self._convert_to_report_response(self.data.station_records)
            )
            normalized_data["StationRecords"] = station_records.normalize_json()

        # Temperature Constants
        if self.data.temperature_constants:
            temperature_constants = ReportTemperatureConstants(
                data=self._convert_to_report_response(self.data.temperature_constants)
            )
            normalized_data[
                "TemperatureConstants"
            ] = temperature_constants.normalize_json()

        # Wind Rose
        if self.data.wind_rose:
            wind_rose = ReportWindrose(
                data=self._convert_to_report_response(self.data.wind_rose)
            )
            normalized_data["WindRose"] = wind_rose.normalize_json()

        # Combine all normalized data
        return pd.concat(normalized_data.values(), keys=normalized_data.keys())

    def to_list(self) -> List[Any]:
        """
        Converts the JSON data into a single list by combining lists for
        all report types.

        :return List[Any]: Combined list for all reports.
        """
        if self.data is None:
            return []

        data_list = []

        # DUT
        if self.data.dut:
            dut = ReportDut(data=self._convert_to_report_response(self.data.dut))
            data_list.extend(dut.to_list())

        # Humidity Constants
        if self.data.humidity_constants:
            humidity_constants = ReportHumidityConstants(
                data=self._convert_to_report_response(self.data.humidity_constants)
            )
            data_list.extend(humidity_constants.to_list())

        # IDF
        if self.data.idf:
            idf = ReportIdf(data=self._convert_to_report_response(self.data.idf))
            data_list.extend(idf.to_list())

        # Normals
        if self.data.normals:
            normals = ReportNormals(
                data=self._convert_to_report_response(self.data.normals)
            )
            data_list.extend(normals.to_list())

        # Station Records
        if self.data.station_records:
            station_records = ReportStationRecords(
                data=self._convert_to_report_response(self.data.station_records)
            )
            data_list.extend(station_records.to_list())

        # Temperature Constants
        if self.data.temperature_constants:
            temperature_constants = ReportTemperatureConstants(
                data=self._convert_to_report_response(self.data.temperature_constants)
            )
            data_list.extend(temperature_constants.to_list())

        # Wind Rose
        if self.data.wind_rose:
            wind_rose = ReportWindrose(
                data=self._convert_to_report_response(self.data.wind_rose)
            )
            data_list.extend(wind_rose.to_list())

        return data_list

    @staticmethod
    def _convert_to_report_response(data: Any) -> Any:
        """
        Converts nested model instances into the expected report response types.

        :param data: Nested model instance.
        :return: Converted report response type.
        """
        # Assuming that the nested models implement `dict()` and match the structure
        # of the expected response types.
        return (
            data.dict()
        )  # Adjust this as needed if additional transformations are required.

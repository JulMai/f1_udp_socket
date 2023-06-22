"""
File created by: https://github.com/JulMai/f1_udp_socket_spec

Code for
	to_json,
    PacketMixin,
    Packet
is from f1_22_telemetry
"""


"""
The hard work for this file was taken from here:
https://forums.codemasters.com/topic/
80231-f1-2021-udp-specification/?do=findComment&comment=624274


Event                | Code   | Description
Session Started      | "SSTA" | Sent when the session starts
Session Ended        | "SEND" | Sent when the session ends
Fastest Lap          | "FTLP" | When a driver achieves the fastest lap
Retirement           | "RTMT" | When a driver retires
DRS enabled          | "DRSE" | Race control have enabled DRS
DRS disabled         | "DRSD" | Race control have disabled DRS
Team mate in pits    | "TMPT" | Your team mate has entered the pits
Chequered flag       | "CHQF" | The chequered flag has been waved
Race Winner          | "RCWN" | The race winner is announced
Penalty Issued       | "PENA" | A penalty has been issued – details in event
Speed Trap Triggered | "SPTP" | Speed trap has been triggered by fastest speed
Start lights         | "STLG" | Start lights – number shown
Lights out           | "LGOT" | Lights out
Drive through served | "DTSV" | Drive through penalty served
Stop go served       | "SGSV" | Stop go penalty served

"""

import ctypes
import json

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


def to_json(*args, **kwargs):
    kwargs.setdefault("indent", 2)

    kwargs["sort_keys"] = True
    kwargs["ensure_ascii"] = False
    kwargs["separators"] = (",", ": ")

    return json.dumps(*args, **kwargs)


class PacketMixin(object):
    """A base set of helper methods for ctypes based packets"""

    def get_value(self, field):
        """Returns the field's value and formats the types value"""
        return self._format_type(getattr(self, field))

    def pack(self):
        """Packs the current data structure into a compressed binary

        Returns:
            (bytes):
                - The packed binary

        """
        return bytes(self)

    @classmethod
    def size(cls):
        return ctypes.sizeof(cls)

    @classmethod
    def unpack(cls, buffer):
        """Attempts to unpack the binary structure into a python structure

        Args:
            buffer (bytes):
                - The encoded buffer to decode

        """
        return cls.from_buffer_copy(buffer)

    def to_dict(self):
        """Returns a ``dict`` with key-values derived from _fields_"""
        return {k: self.get_value(k) for k, _ in self._fields_}

    def to_json(self):
        """Returns a ``str`` of sorted JSON derived from _fields_"""
        return to_json(self.to_dict())

    def _format_type(self, value):
        """A type helper to format values"""
        class_name = type(value).__name__

        if class_name == "float":
            return round(value, 3)

        if class_name == "bytes":
            return value.decode()

        if isinstance(value, ctypes.Array):
            return _format_array_type(value)

        if hasattr(value, "to_dict"):
            return value.to_dict()

        return value


def _format_array_type(value):
    results = []

    for item in value:
        if isinstance(item, Packet):
            results.append(item.to_dict())
        else:
            results.append(item)

    return results


class Packet(ctypes.LittleEndianStructure, PacketMixin):
    """The base packet class for API version F1 22"""

    _pack_ = 1

    def __repr__(self):
        return self.to_json()
    
"""
The following code was produced by:
https://github.com/JulMai/f1_udp_socket_spec/tree/main/src/write/packet_classes/packet_classes.py
"""

class PacketHeader(Packet):
	_fields_ = [
		("packetFormat", ctypes.c_uint16),
		("gameYear", ctypes.c_uint8),
		("gameMajorVersion", ctypes.c_uint8),
		("gameMinorVersion", ctypes.c_uint8),
		("packetVersion", ctypes.c_uint8),
		("packetId", ctypes.c_uint8),
		("sessionUID", ctypes.c_uint64),
		("sessionTime", ctypes.c_float),
		("frameIdentifier", ctypes.c_uint32),
		("overallFrameIdentifier", ctypes.c_uint32),
		("playerCarIndex", ctypes.c_uint8),
		("secondaryPlayerCarIndex", ctypes.c_uint8),
	]


class CarMotionData(Packet):
	_fields_ = [
		("worldPositionX", ctypes.c_float),
		("worldPositionY", ctypes.c_float),
		("worldPositionZ", ctypes.c_float),
		("worldVelocityX", ctypes.c_float),
		("worldVelocityY", ctypes.c_float),
		("worldVelocityZ", ctypes.c_float),
		("worldForwardDirX", ctypes.c_int16),
		("worldForwardDirY", ctypes.c_int16),
		("worldForwardDirZ", ctypes.c_int16),
		("worldRightDirX", ctypes.c_int16),
		("worldRightDirY", ctypes.c_int16),
		("worldRightDirZ", ctypes.c_int16),
		("gForceLateral", ctypes.c_float),
		("gForceLongitudinal", ctypes.c_float),
		("gForceVertical", ctypes.c_float),
		("yaw", ctypes.c_float),
		("pitch", ctypes.c_float),
		("roll", ctypes.c_float),
	]


class PacketMotionData(Packet):
	_fields_ = [
		("header", PacketHeader),
		("carMotionData", CarMotionData * 22),
	]


class MarshalZone(Packet):
	_fields_ = [
		("zoneStart", ctypes.c_float),
		("zoneFlag", ctypes.c_int8),
	]


class WeatherForecastSample(Packet):
	_fields_ = [
		("sessionType", ctypes.c_uint8),
		("timeOffset", ctypes.c_uint8),
		("weather", ctypes.c_uint8),
		("trackTemperature", ctypes.c_int8),
		("trackTemperatureChange", ctypes.c_int8),
		("airTemperature", ctypes.c_int8),
		("airTemperatureChange", ctypes.c_int8),
		("rainPercentage", ctypes.c_uint8),
	]


class PacketSessionData(Packet):
	_fields_ = [
		("header", PacketHeader),
		("weather", ctypes.c_uint8),
		("trackTemperature", ctypes.c_int8),
		("airTemperature", ctypes.c_int8),
		("totalLaps", ctypes.c_uint8),
		("trackLength", ctypes.c_uint16),
		("sessionType", ctypes.c_uint8),
		("trackId", ctypes.c_int8),
		("formula", ctypes.c_uint8),
		("sessionTimeLeft", ctypes.c_uint16),
		("sessionDuration", ctypes.c_uint16),
		("pitSpeedLimit", ctypes.c_uint8),
		("gamePaused", ctypes.c_uint8),
		("isSpectating", ctypes.c_uint8),
		("spectatorCarIndex", ctypes.c_uint8),
		("sliProNativeSupport", ctypes.c_uint8),
		("numMarshalZones", ctypes.c_uint8),
		("marshalZones", MarshalZone * 21),
		("safetyCarStatus", ctypes.c_uint8),
		("networkGame", ctypes.c_uint8),
		("numWeatherForecastSamples", ctypes.c_uint8),
		("weatherForecastSamples", WeatherForecastSample * 56),
		("forecastAccuracy", ctypes.c_uint8),
		("aiDifficulty", ctypes.c_uint8),
		("seasonLinkIdentifier", ctypes.c_uint32),
		("weekendLinkIdentifier", ctypes.c_uint32),
		("sessionLinkIdentifier", ctypes.c_uint32),
		("pitStopWindowIdealLap", ctypes.c_uint8),
		("pitStopWindowLatestLap", ctypes.c_uint8),
		("pitStopRejoinPosition", ctypes.c_uint8),
		("steeringAssist", ctypes.c_uint8),
		("brakingAssist", ctypes.c_uint8),
		("gearboxAssist", ctypes.c_uint8),
		("pitAssist", ctypes.c_uint8),
		("pitReleaseAssist", ctypes.c_uint8),
		("ERSAssist", ctypes.c_uint8),
		("DRSAssist", ctypes.c_uint8),
		("dynamicRacingLine", ctypes.c_uint8),
		("dynamicRacingLineType", ctypes.c_uint8),
		("gameMode", ctypes.c_uint8),
		("ruleSet", ctypes.c_uint8),
		("timeOfDay", ctypes.c_uint32),
		("sessionLength", ctypes.c_uint8),
		("speedUnitsLeadPlayer", ctypes.c_uint8),
		("temperatureUnitsLeadPlayer", ctypes.c_uint8),
		("speedUnitsSecondaryPlayer", ctypes.c_uint8),
		("temperatureUnitsSecondaryPlayer", ctypes.c_uint8),
		("numSafetyCarPeriods", ctypes.c_uint8),
		("numVirtualSafetyCarPeriods", ctypes.c_uint8),
		("numRedFlagPeriods", ctypes.c_uint8),
	]


class LapData(Packet):
	_fields_ = [
		("lastLapTimeInMS", ctypes.c_uint32),
		("currentLapTimeInMS", ctypes.c_uint32),
		("sector1TimeInMS", ctypes.c_uint16),
		("sector1TimeMinutes", ctypes.c_uint8),
		("sector2TimeInMS", ctypes.c_uint16),
		("sector2TimeMinutes", ctypes.c_uint8),
		("deltaToCarInFrontInMS", ctypes.c_uint16),
		("deltaToRaceLeaderInMS", ctypes.c_uint16),
		("lapDistance", ctypes.c_float),
		("totalDistance", ctypes.c_float),
		("safetyCarDelta", ctypes.c_float),
		("carPosition", ctypes.c_uint8),
		("currentLapNum", ctypes.c_uint8),
		("pitStatus", ctypes.c_uint8),
		("numPitStops", ctypes.c_uint8),
		("sector", ctypes.c_uint8),
		("currentLapInvalid", ctypes.c_uint8),
		("penalties", ctypes.c_uint8),
		("totalWarnings", ctypes.c_uint8),
		("cornerCuttingWarnings", ctypes.c_uint8),
		("numUnservedDriveThroughPens", ctypes.c_uint8),
		("numUnservedStopGoPens", ctypes.c_uint8),
		("gridPosition", ctypes.c_uint8),
		("driverStatus", ctypes.c_uint8),
		("resultStatus", ctypes.c_uint8),
		("pitLaneTimerActive", ctypes.c_uint8),
		("pitLaneTimeInLaneInMS", ctypes.c_uint16),
		("pitStopTimerInMS", ctypes.c_uint16),
		("pitStopShouldServePen", ctypes.c_uint8),
	]


class PacketLapData(Packet):
	_fields_ = [
		("header", PacketHeader),
		("lapData", LapData * 22),
		("timeTrialPBCarIdx", ctypes.c_uint8),
		("timeTrialRivalCarIdx", ctypes.c_uint8),
	]


class PacketEventData(Packet):
	_fields_ = [
		("header", PacketHeader),
		("eventStringCode", ctypes.c_uint8 * 4),
	]


class ParticipantData(Packet):
	_fields_ = [
		("aiControlled", ctypes.c_uint8),
		("driverId", ctypes.c_uint8),
		("networkId", ctypes.c_uint8),
		("teamId", ctypes.c_uint8),
		("myTeam", ctypes.c_uint8),
		("raceNumber", ctypes.c_uint8),
		("nationality", ctypes.c_uint8),
		("name", ctypes.c_char * 48),
		("yourTelemetry", ctypes.c_uint8),
		("showOnlineNames", ctypes.c_uint8),
		("platform", ctypes.c_uint8),
	]


class PacketParticipantsData(Packet):
	_fields_ = [
		("header", PacketHeader),
		("numActiveCars", ctypes.c_uint8),
		("participants", ParticipantData * 22),
	]


class CarSetupData(Packet):
	_fields_ = [
		("frontWing", ctypes.c_uint8),
		("rearWing", ctypes.c_uint8),
		("onThrottle", ctypes.c_uint8),
		("offThrottle", ctypes.c_uint8),
		("frontCamber", ctypes.c_float),
		("rearCamber", ctypes.c_float),
		("frontToe", ctypes.c_float),
		("rearToe", ctypes.c_float),
		("frontSuspension", ctypes.c_uint8),
		("rearSuspension", ctypes.c_uint8),
		("frontAntiRollBar", ctypes.c_uint8),
		("rearAntiRollBar", ctypes.c_uint8),
		("frontSuspensionHeight", ctypes.c_uint8),
		("rearSuspensionHeight", ctypes.c_uint8),
		("brakePressure", ctypes.c_uint8),
		("brakeBias", ctypes.c_uint8),
		("rearLeftTyrePressure", ctypes.c_float),
		("rearRightTyrePressure", ctypes.c_float),
		("frontLeftTyrePressure", ctypes.c_float),
		("frontRightTyrePressure", ctypes.c_float),
		("ballast", ctypes.c_uint8),
		("fuelLoad", ctypes.c_float),
	]


class PacketCarSetupData(Packet):
	_fields_ = [
		("header", PacketHeader),
		("carSetups", CarSetupData * 22),
	]


class CarTelemetryData(Packet):
	_fields_ = [
		("speed", ctypes.c_uint16),
		("throttle", ctypes.c_float),
		("steer", ctypes.c_float),
		("brake", ctypes.c_float),
		("clutch", ctypes.c_uint8),
		("gear", ctypes.c_int8),
		("engineRPM", ctypes.c_uint16),
		("drs", ctypes.c_uint8),
		("revLightsPercent", ctypes.c_uint8),
		("revLightsBitValue", ctypes.c_uint16),
		("brakesTemperature", ctypes.c_uint16 * 4),
		("tyresSurfaceTemperature", ctypes.c_uint8 * 4),
		("tyresInnerTemperature", ctypes.c_uint8 * 4),
		("engineTemperature", ctypes.c_uint16),
		("tyresPressure", ctypes.c_float * 4),
		("surfaceType", ctypes.c_uint8 * 4),
	]


class PacketCarTelemetryData(Packet):
	_fields_ = [
		("header", PacketHeader),
		("carTelemetryData", CarTelemetryData * 22),
		("mfdPanelIndex", ctypes.c_uint8),
		("mfdPanelIndexSecondaryPlayer", ctypes.c_uint8),
		("suggestedGear", ctypes.c_int8),
	]


class CarStatusData(Packet):
	_fields_ = [
		("tractionControl", ctypes.c_uint8),
		("antiLockBrakes", ctypes.c_uint8),
		("fuelMix", ctypes.c_uint8),
		("frontBrakeBias", ctypes.c_uint8),
		("pitLimiterStatus", ctypes.c_uint8),
		("fuelInTank", ctypes.c_float),
		("fuelCapacity", ctypes.c_float),
		("fuelRemainingLaps", ctypes.c_float),
		("maxRPM", ctypes.c_uint16),
		("idleRPM", ctypes.c_uint16),
		("maxGears", ctypes.c_uint8),
		("drsAllowed", ctypes.c_uint8),
		("drsActivationDistance", ctypes.c_uint16),
		("actualTyreCompound", ctypes.c_uint8),
		("visualTyreCompound", ctypes.c_uint8),
		("tyresAgeLaps", ctypes.c_uint8),
		("vehicleFiaFlags", ctypes.c_int8),
		("enginePowerICE", ctypes.c_float),
		("enginePowerMGUK", ctypes.c_float),
		("ersStoreEnergy", ctypes.c_float),
		("ersDeployMode", ctypes.c_uint8),
		("ersHarvestedThisLapMGUK", ctypes.c_float),
		("ersHarvestedThisLapMGUH", ctypes.c_float),
		("ersDeployedThisLap", ctypes.c_float),
		("networkPaused", ctypes.c_uint8),
	]


class PacketCarStatusData(Packet):
	_fields_ = [
		("header", PacketHeader),
		("carStatusData", CarStatusData * 22),
	]


class FinalClassificationData(Packet):
	_fields_ = [
		("position", ctypes.c_uint8),
		("numLaps", ctypes.c_uint8),
		("gridPosition", ctypes.c_uint8),
		("points", ctypes.c_uint8),
		("numPitStops", ctypes.c_uint8),
		("resultStatus", ctypes.c_uint8),
		("bestLapTimeInMS", ctypes.c_uint32),
		("totalRaceTime", ctypes.c_double),
		("penaltiesTime", ctypes.c_uint8),
		("numPenalties", ctypes.c_uint8),
		("numTyreStints", ctypes.c_uint8),
		("tyreStintsActual", ctypes.c_uint8 * 8),
		("tyreStintsVisual", ctypes.c_uint8 * 8),
		("tyreStintsEndLaps", ctypes.c_uint8 * 8),
	]


class PacketFinalClassificationData(Packet):
	_fields_ = [
		("header", PacketHeader),
		("numCars", ctypes.c_uint8),
		("classificationData", FinalClassificationData * 22),
	]


class LobbyInfoData(Packet):
	_fields_ = [
		("aiControlled", ctypes.c_uint8),
		("teamId", ctypes.c_uint8),
		("nationality", ctypes.c_uint8),
		("platform", ctypes.c_uint8),
		("name", ctypes.c_char * 48),
		("carNumber", ctypes.c_uint8),
		("readyStatus", ctypes.c_uint8),
	]


class PacketLobbyInfoData(Packet):
	_fields_ = [
		("header", PacketHeader),
		("numPlayers", ctypes.c_uint8),
		("lobbyPlayers", LobbyInfoData * 22),
	]


class CarDamageData(Packet):
	_fields_ = [
		("tyresWear", ctypes.c_float * 4),
		("tyresDamage", ctypes.c_uint8 * 4),
		("brakesDamage", ctypes.c_uint8 * 4),
		("frontLeftWingDamage", ctypes.c_uint8),
		("frontRightWingDamage", ctypes.c_uint8),
		("rearWingDamage", ctypes.c_uint8),
		("floorDamage", ctypes.c_uint8),
		("diffuserDamage", ctypes.c_uint8),
		("sidepodDamage", ctypes.c_uint8),
		("drsFault", ctypes.c_uint8),
		("ersFault", ctypes.c_uint8),
		("gearBoxDamage", ctypes.c_uint8),
		("engineDamage", ctypes.c_uint8),
		("engineMGUHWear", ctypes.c_uint8),
		("engineESWear", ctypes.c_uint8),
		("engineCEWear", ctypes.c_uint8),
		("engineICEWear", ctypes.c_uint8),
		("engineMGUKWear", ctypes.c_uint8),
		("engineTCWear", ctypes.c_uint8),
		("engineBlown", ctypes.c_uint8),
		("engineSeized", ctypes.c_uint8),
	]


class PacketCarDamageData(Packet):
	_fields_ = [
		("header", PacketHeader),
		("carDamageData", CarDamageData * 22),
	]


class LapHistoryData(Packet):
	_fields_ = [
		("lapTimeInMS", ctypes.c_uint32),
		("sector1TimeInMS", ctypes.c_uint16),
		("sector1TimeMinutes", ctypes.c_uint8),
		("sector2TimeInMS", ctypes.c_uint16),
		("sector1TimeMinutes", ctypes.c_uint8),
		("sector3TimeInMS", ctypes.c_uint16),
		("sector3TimeMinutes", ctypes.c_uint8),
		("lapValidBitFlags", ctypes.c_uint8),
	]


class TyreStintHistoryData(Packet):
	_fields_ = [
		("endLap", ctypes.c_uint8),
		("tyreActualCompound", ctypes.c_uint8),
		("tyreVisualCompound", ctypes.c_uint8),
	]


class PacketSessionHistoryData(Packet):
	_fields_ = [
		("header", PacketHeader),
		("carIdx", ctypes.c_uint8),
		("numLaps", ctypes.c_uint8),
		("numTyreStints", ctypes.c_uint8),
		("bestLapTimeLapNum", ctypes.c_uint8),
		("bestSector1LapNum", ctypes.c_uint8),
		("bestSector2LapNum", ctypes.c_uint8),
		("bestSector3LapNum", ctypes.c_uint8),
		("lapHistoryData", LapHistoryData * 100),
		("tyreStintsHistoryData", TyreStintHistoryData * 8),
	]


class TyreSetData(Packet):
	_fields_ = [
		("actualTyreCompound", ctypes.c_uint8),
		("visualTyreCompound", ctypes.c_uint8),
		("wear", ctypes.c_uint8),
		("available", ctypes.c_uint8),
		("recommendedSession", ctypes.c_uint8),
		("lifeSpan", ctypes.c_uint8),
		("usableLife", ctypes.c_uint8),
		("lapDeltaTime", ctypes.c_int16),
		("fitted", ctypes.c_uint8),
	]


class PacketTyreSetsData(Packet):
	_fields_ = [
		("header", PacketHeader),
		("carIdx", ctypes.c_uint8),
		("tyreSetData", TyreSetData * 20),
		("fittedIdx", ctypes.c_uint8),
	]


class PacketMotionExData(Packet):
	_fields_ = [
		("header", PacketHeader),
		("suspensionPosition", ctypes.c_float * 4),
		("suspensionVelocity", ctypes.c_float * 4),
		("suspensionAcceleration", ctypes.c_float * 4),
		("wheelSpeed", ctypes.c_float * 4),
		("wheelSlipRatio", ctypes.c_float * 4),
		("wheelSlipAngle", ctypes.c_float * 4),
		("wheelLatForce", ctypes.c_float * 4),
		("wheelLongForce", ctypes.c_float * 4),
		("heightOfCOGAboveGround", ctypes.c_float),
		("localVelocityX", ctypes.c_float),
		("localVelocityY", ctypes.c_float),
		("localVelocityZ", ctypes.c_float),
		("angularVelocityX", ctypes.c_float),
		("angularVelocityY", ctypes.c_float),
		("angularVelocityZ", ctypes.c_float),
		("angularAccelerationX", ctypes.c_float),
		("angularAccelerationY", ctypes.c_float),
		("angularAccelerationZ", ctypes.c_float),
		("frontWheelsAngle", ctypes.c_float),
		("wheelVertForce", ctypes.c_float * 4),
	]


HEADER_FIELD_TO_PACKET_TYPE = {
	(2023, 1, 0) : PacketMotionData,
	(2023, 1, 1) : PacketSessionData,
	(2023, 1, 2) : PacketLapData,
	(2023, 1, 3) : PacketEventData,
	(2023, 1, 4) : PacketParticipantsData,
	(2023, 1, 5) : PacketCarSetupData,
	(2023, 1, 6) : PacketCarTelemetryData,
	(2023, 1, 7) : PacketCarStatusData,
	(2023, 1, 8) : PacketFinalClassificationData,
	(2023, 1, 9) : PacketLobbyInfoData,
	(2023, 1, 10) : PacketCarDamageData,
	(2023, 1, 11) : PacketSessionHistoryData,
	(2023, 1, 12) : PacketTyreSetsData,
	(2023, 1, 13) : PacketMotionExData,
}

PACKET_ID_TO_PACKET_TYPE_STR = {
	0: 'PacketMotionData',
	1: 'PacketSessionData',
	2: 'PacketLapData',
	3: 'PacketEventData',
	4: 'PacketParticipantsData',
	5: 'PacketCarSetupData',
	6: 'PacketCarTelemetryData',
	7: 'PacketCarStatusData',
	8: 'PacketFinalClassificationData',
	9: 'PacketLobbyInfoData',
	10: 'PacketCarDamageData',
	11: 'PacketSessionHistoryData',
	12: 'PacketTyreSetsData',
	13: 'PacketMotionExData',
}

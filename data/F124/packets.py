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
		("packet_format", ctypes.c_uint16),
		("game_year", ctypes.c_uint8),
		("game_major_version", ctypes.c_uint8),
		("game_minor_version", ctypes.c_uint8),
		("packet_version", ctypes.c_uint8),
		("packet_id", ctypes.c_uint8),
		("session_uid", ctypes.c_uint64),
		("session_time", ctypes.c_float),
		("frame_identifier", ctypes.c_uint32),
		("overall_frame_identifier", ctypes.c_uint32),
		("player_car_index", ctypes.c_uint8),
		("secondary_player_car_index", ctypes.c_uint8),
	]


class CarMotionData(Packet):
	_fields_ = [
		("world_position_x", ctypes.c_float),
		("world_position_y", ctypes.c_float),
		("world_position_z", ctypes.c_float),
		("world_velocity_x", ctypes.c_float),
		("world_velocity_y", ctypes.c_float),
		("world_velocity_z", ctypes.c_float),
		("world_forward_dir_x", ctypes.c_int16),
		("world_forward_dir_y", ctypes.c_int16),
		("world_forward_dir_z", ctypes.c_int16),
		("world_right_dir_x", ctypes.c_int16),
		("world_right_dir_y", ctypes.c_int16),
		("world_right_dir_z", ctypes.c_int16),
		("g_force_lateral", ctypes.c_float),
		("g_force_longitudinal", ctypes.c_float),
		("g_force_vertical", ctypes.c_float),
		("yaw", ctypes.c_float),
		("pitch", ctypes.c_float),
		("roll", ctypes.c_float),
	]


class PacketMotionData(Packet):
	_fields_ = [
		("header", PacketHeader),
		("car_motion_data", CarMotionData * 22),
	]


class MarshalZone(Packet):
	_fields_ = [
		("zone_start", ctypes.c_float),
		("zone_flag", ctypes.c_int8),
	]


class WeatherForecastSample(Packet):
	_fields_ = [
		("session_type", ctypes.c_uint8),
		("time_offset", ctypes.c_uint8),
		("weather", ctypes.c_uint8),
		("track_temperature", ctypes.c_int8),
		("track_temperature_change", ctypes.c_int8),
		("air_temperature", ctypes.c_int8),
		("air_temperature_change", ctypes.c_int8),
		("rain_percentage", ctypes.c_uint8),
	]


class PacketSessionData(Packet):
	_fields_ = [
		("header", PacketHeader),
		("weather", ctypes.c_uint8),
		("track_temperature", ctypes.c_int8),
		("air_temperature", ctypes.c_int8),
		("total_laps", ctypes.c_uint8),
		("track_length", ctypes.c_uint16),
		("session_type", ctypes.c_uint8),
		("track_id", ctypes.c_int8),
		("formula", ctypes.c_uint8),
		("session_time_left", ctypes.c_uint16),
		("session_duration", ctypes.c_uint16),
		("pit_speed_limit", ctypes.c_uint8),
		("game_paused", ctypes.c_uint8),
		("is_spectating", ctypes.c_uint8),
		("spectator_car_index", ctypes.c_uint8),
		("sli_pro_native_support", ctypes.c_uint8),
		("num_marshal_zones", ctypes.c_uint8),
		("marshal_zones", MarshalZone * 21),
		("safety_car_status", ctypes.c_uint8),
		("network_game", ctypes.c_uint8),
		("num_weather_forecast_samples", ctypes.c_uint8),
		("weather_forecast_samples", WeatherForecastSample * 64),
		("forecast_accuracy", ctypes.c_uint8),
		("ai_difficulty", ctypes.c_uint8),
		("season_link_identifier", ctypes.c_uint32),
		("weekend_link_identifier", ctypes.c_uint32),
		("session_link_identifier", ctypes.c_uint32),
		("pit_stop_window_ideal_lap", ctypes.c_uint8),
		("pit_stop_window_latest_lap", ctypes.c_uint8),
		("pit_stop_rejoin_position", ctypes.c_uint8),
		("steering_assist", ctypes.c_uint8),
		("braking_assist", ctypes.c_uint8),
		("gearbox_assist", ctypes.c_uint8),
		("pit_assist", ctypes.c_uint8),
		("pit_release_assist", ctypes.c_uint8),
		("ersassist", ctypes.c_uint8),
		("drsassist", ctypes.c_uint8),
		("dynamic_racing_line", ctypes.c_uint8),
		("dynamic_racing_line_type", ctypes.c_uint8),
		("game_mode", ctypes.c_uint8),
		("rule_set", ctypes.c_uint8),
		("time_of_day", ctypes.c_uint32),
		("session_length", ctypes.c_uint8),
		("speed_units_lead_player", ctypes.c_uint8),
		("temperature_units_lead_player", ctypes.c_uint8),
		("speed_units_secondary_player", ctypes.c_uint8),
		("temperature_units_secondary_player", ctypes.c_uint8),
		("num_safety_car_periods", ctypes.c_uint8),
		("num_virtual_safety_car_periods", ctypes.c_uint8),
		("num_red_flag_periods", ctypes.c_uint8),
		("equal_car_performance", ctypes.c_uint8),
		("recovery_mode", ctypes.c_uint8),
		("flashback_limit", ctypes.c_uint8),
		("surface_type", ctypes.c_uint8),
		("low_fuel_mode", ctypes.c_uint8),
		("race_starts", ctypes.c_uint8),
		("tyre_temperature", ctypes.c_uint8),
		("pit_lane_tyre_sim", ctypes.c_uint8),
		("car_damage", ctypes.c_uint8),
		("car_damage_rate", ctypes.c_uint8),
		("collisions", ctypes.c_uint8),
		("collisions_off_for_first_lap_only", ctypes.c_uint8),
		("mp_unsafe_pit_release", ctypes.c_uint8),
		("mp_off_for_griefing", ctypes.c_uint8),
		("corner_cutting_stringency", ctypes.c_uint8),
		("parc_ferme_rules", ctypes.c_uint8),
		("pit_stop_experience", ctypes.c_uint8),
		("safety_car", ctypes.c_uint8),
		("safety_car_experience", ctypes.c_uint8),
		("formation_lap", ctypes.c_uint8),
		("formation_lap_experience", ctypes.c_uint8),
		("red_flags", ctypes.c_uint8),
		("affects_licence_level_solo", ctypes.c_uint8),
		("affects_licence_level_mp", ctypes.c_uint8),
		("num_sessions_in_weekend", ctypes.c_uint8),
		("weekend_structure", ctypes.c_uint8 * 12),
		("sector2lap_distance_start", ctypes.c_float),
		("sector3lap_distance_start", ctypes.c_float),
	]


class LapData(Packet):
	_fields_ = [
		("last_lap_time_in_ms", ctypes.c_uint32),
		("current_lap_time_in_ms", ctypes.c_uint32),
		("sector1time_mspart", ctypes.c_uint16),
		("sector1time_minutes_part", ctypes.c_uint8),
		("sector2time_mspart", ctypes.c_uint16),
		("sector2time_minutes_part", ctypes.c_uint8),
		("delta_to_car_in_front_mspart", ctypes.c_uint16),
		("delta_to_car_in_front_minutes_part", ctypes.c_uint8),
		("delta_to_race_leader_mspart", ctypes.c_uint16),
		("delta_to_race_leader_minutes_part", ctypes.c_uint8),
		("lap_distance", ctypes.c_float),
		("total_distance", ctypes.c_float),
		("safety_car_delta", ctypes.c_float),
		("car_position", ctypes.c_uint8),
		("current_lap_num", ctypes.c_uint8),
		("pit_status", ctypes.c_uint8),
		("num_pit_stops", ctypes.c_uint8),
		("sector", ctypes.c_uint8),
		("current_lap_invalid", ctypes.c_uint8),
		("penalties", ctypes.c_uint8),
		("total_warnings", ctypes.c_uint8),
		("corner_cutting_warnings", ctypes.c_uint8),
		("num_unserved_drive_through_pens", ctypes.c_uint8),
		("num_unserved_stop_go_pens", ctypes.c_uint8),
		("grid_position", ctypes.c_uint8),
		("driver_status", ctypes.c_uint8),
		("result_status", ctypes.c_uint8),
		("pit_lane_timer_active", ctypes.c_uint8),
		("pit_lane_time_in_lane_in_ms", ctypes.c_uint16),
		("pit_stop_timer_in_ms", ctypes.c_uint16),
		("pit_stop_should_serve_pen", ctypes.c_uint8),
		("speed_trap_fastest_speed", ctypes.c_float),
		("speed_trap_fastest_lap", ctypes.c_uint8),
	]


class PacketLapData(Packet):
	_fields_ = [
		("header", PacketHeader),
		("lap_data", LapData * 22),
		("time_trial_pbcar_idx", ctypes.c_uint8),
		("time_trial_rival_car_idx", ctypes.c_uint8),
	]


class PacketEventData(Packet):
	_fields_ = [
		("header", PacketHeader),
		("event_string_code", ctypes.c_uint8 * 4),
	]


class ParticipantData(Packet):
	_fields_ = [
		("ai_controlled", ctypes.c_uint8),
		("driver_id", ctypes.c_uint8),
		("network_id", ctypes.c_uint8),
		("team_id", ctypes.c_uint8),
		("my_team", ctypes.c_uint8),
		("race_number", ctypes.c_uint8),
		("nationality", ctypes.c_uint8),
		("name", ctypes.c_char * 48),
		("your_telemetry", ctypes.c_uint8),
		("show_online_names", ctypes.c_uint8),
		("tech_level", ctypes.c_uint16),
		("platform", ctypes.c_uint8),
	]


class PacketParticipantsData(Packet):
	_fields_ = [
		("header", PacketHeader),
		("num_active_cars", ctypes.c_uint8),
		("participants", ParticipantData * 22),
	]


class CarSetupData(Packet):
	_fields_ = [
		("front_wing", ctypes.c_uint8),
		("rear_wing", ctypes.c_uint8),
		("on_throttle", ctypes.c_uint8),
		("off_throttle", ctypes.c_uint8),
		("front_camber", ctypes.c_float),
		("rear_camber", ctypes.c_float),
		("front_toe", ctypes.c_float),
		("rear_toe", ctypes.c_float),
		("front_suspension", ctypes.c_uint8),
		("rear_suspension", ctypes.c_uint8),
		("front_anti_roll_bar", ctypes.c_uint8),
		("rear_anti_roll_bar", ctypes.c_uint8),
		("front_suspension_height", ctypes.c_uint8),
		("rear_suspension_height", ctypes.c_uint8),
		("brake_pressure", ctypes.c_uint8),
		("brake_bias", ctypes.c_uint8),
		("engine_braking", ctypes.c_uint8),
		("rear_left_tyre_pressure", ctypes.c_float),
		("rear_right_tyre_pressure", ctypes.c_float),
		("front_left_tyre_pressure", ctypes.c_float),
		("front_right_tyre_pressure", ctypes.c_float),
		("ballast", ctypes.c_uint8),
		("fuel_load", ctypes.c_float),
	]


class PacketCarSetupData(Packet):
	_fields_ = [
		("header", PacketHeader),
		("car_setups", CarSetupData * 22),
		("next_front_wing_value", ctypes.c_float),
	]


class CarTelemetryData(Packet):
	_fields_ = [
		("speed", ctypes.c_uint16),
		("throttle", ctypes.c_float),
		("steer", ctypes.c_float),
		("brake", ctypes.c_float),
		("clutch", ctypes.c_uint8),
		("gear", ctypes.c_int8),
		("engine_rpm", ctypes.c_uint16),
		("drs", ctypes.c_uint8),
		("rev_lights_percent", ctypes.c_uint8),
		("rev_lights_bit_value", ctypes.c_uint16),
		("brakes_temperature", ctypes.c_uint16 * 4),
		("tyres_surface_temperature", ctypes.c_uint8 * 4),
		("tyres_inner_temperature", ctypes.c_uint8 * 4),
		("engine_temperature", ctypes.c_uint16),
		("tyres_pressure", ctypes.c_float * 4),
		("surface_type", ctypes.c_uint8 * 4),
	]


class PacketCarTelemetryData(Packet):
	_fields_ = [
		("header", PacketHeader),
		("car_telemetry_data", CarTelemetryData * 22),
		("mfd_panel_index", ctypes.c_uint8),
		("mfd_panel_index_secondary_player", ctypes.c_uint8),
		("suggested_gear", ctypes.c_int8),
	]


class CarStatusData(Packet):
	_fields_ = [
		("traction_control", ctypes.c_uint8),
		("anti_lock_brakes", ctypes.c_uint8),
		("fuel_mix", ctypes.c_uint8),
		("front_brake_bias", ctypes.c_uint8),
		("pit_limiter_status", ctypes.c_uint8),
		("fuel_in_tank", ctypes.c_float),
		("fuel_capacity", ctypes.c_float),
		("fuel_remaining_laps", ctypes.c_float),
		("max_rpm", ctypes.c_uint16),
		("idle_rpm", ctypes.c_uint16),
		("max_gears", ctypes.c_uint8),
		("drs_allowed", ctypes.c_uint8),
		("drs_activation_distance", ctypes.c_uint16),
		("actual_tyre_compound", ctypes.c_uint8),
		("visual_tyre_compound", ctypes.c_uint8),
		("tyres_age_laps", ctypes.c_uint8),
		("vehicle_fia_flags", ctypes.c_int8),
		("engine_power_ice", ctypes.c_float),
		("engine_power_mguk", ctypes.c_float),
		("ers_store_energy", ctypes.c_float),
		("ers_deploy_mode", ctypes.c_uint8),
		("ers_harvested_this_lap_mguk", ctypes.c_float),
		("ers_harvested_this_lap_mguh", ctypes.c_float),
		("ers_deployed_this_lap", ctypes.c_float),
		("network_paused", ctypes.c_uint8),
	]


class PacketCarStatusData(Packet):
	_fields_ = [
		("header", PacketHeader),
		("car_status_data", CarStatusData * 22),
	]


class FinalClassificationData(Packet):
	_fields_ = [
		("position", ctypes.c_uint8),
		("num_laps", ctypes.c_uint8),
		("grid_position", ctypes.c_uint8),
		("points", ctypes.c_uint8),
		("num_pit_stops", ctypes.c_uint8),
		("result_status", ctypes.c_uint8),
		("best_lap_time_in_ms", ctypes.c_uint32),
		("total_race_time", ctypes.c_double),
		("penalties_time", ctypes.c_uint8),
		("num_penalties", ctypes.c_uint8),
		("num_tyre_stints", ctypes.c_uint8),
		("tyre_stints_actual", ctypes.c_uint8 * 8),
		("tyre_stints_visual", ctypes.c_uint8 * 8),
		("tyre_stints_end_laps", ctypes.c_uint8 * 8),
	]


class PacketFinalClassificationData(Packet):
	_fields_ = [
		("header", PacketHeader),
		("num_cars", ctypes.c_uint8),
		("classification_data", FinalClassificationData * 22),
	]


class LobbyInfoData(Packet):
	_fields_ = [
		("ai_controlled", ctypes.c_uint8),
		("team_id", ctypes.c_uint8),
		("nationality", ctypes.c_uint8),
		("platform", ctypes.c_uint8),
		("name", ctypes.c_char * 48),
		("car_number", ctypes.c_uint8),
		("your_telemetry", ctypes.c_uint8),
		("show_online_names", ctypes.c_uint8),
		("tech_level", ctypes.c_uint16),
		("ready_status", ctypes.c_uint8),
	]


class PacketLobbyInfoData(Packet):
	_fields_ = [
		("header", PacketHeader),
		("num_players", ctypes.c_uint8),
		("lobby_players", LobbyInfoData * 22),
	]


class CarDamageData(Packet):
	_fields_ = [
		("tyres_wear", ctypes.c_float * 4),
		("tyres_damage", ctypes.c_uint8 * 4),
		("brakes_damage", ctypes.c_uint8 * 4),
		("front_left_wing_damage", ctypes.c_uint8),
		("front_right_wing_damage", ctypes.c_uint8),
		("rear_wing_damage", ctypes.c_uint8),
		("floor_damage", ctypes.c_uint8),
		("diffuser_damage", ctypes.c_uint8),
		("sidepod_damage", ctypes.c_uint8),
		("drs_fault", ctypes.c_uint8),
		("ers_fault", ctypes.c_uint8),
		("gear_box_damage", ctypes.c_uint8),
		("engine_damage", ctypes.c_uint8),
		("engine_mguhwear", ctypes.c_uint8),
		("engine_eswear", ctypes.c_uint8),
		("engine_cewear", ctypes.c_uint8),
		("engine_icewear", ctypes.c_uint8),
		("engine_mgukwear", ctypes.c_uint8),
		("engine_tcwear", ctypes.c_uint8),
		("engine_blown", ctypes.c_uint8),
		("engine_seized", ctypes.c_uint8),
	]


class PacketCarDamageData(Packet):
	_fields_ = [
		("header", PacketHeader),
		("car_damage_data", CarDamageData * 22),
	]


class LapHistoryData(Packet):
	_fields_ = [
		("lap_time_in_ms", ctypes.c_uint32),
		("sector1time_mspart", ctypes.c_uint16),
		("sector1time_minutes_part", ctypes.c_uint8),
		("sector2time_mspart", ctypes.c_uint16),
		("sector2time_minutes_part", ctypes.c_uint8),
		("sector3time_mspart", ctypes.c_uint16),
		("sector3time_minutes_part", ctypes.c_uint8),
		("lap_valid_bit_flags", ctypes.c_uint8),
	]


class TyreStintHistoryData(Packet):
	_fields_ = [
		("end_lap", ctypes.c_uint8),
		("tyre_actual_compound", ctypes.c_uint8),
		("tyre_visual_compound", ctypes.c_uint8),
	]


class PacketSessionHistoryData(Packet):
	_fields_ = [
		("header", PacketHeader),
		("car_idx", ctypes.c_uint8),
		("num_laps", ctypes.c_uint8),
		("num_tyre_stints", ctypes.c_uint8),
		("best_lap_time_lap_num", ctypes.c_uint8),
		("best_sector1lap_num", ctypes.c_uint8),
		("best_sector2lap_num", ctypes.c_uint8),
		("best_sector3lap_num", ctypes.c_uint8),
		("lap_history_data", LapHistoryData * 100),
		("tyre_stints_history_data", TyreStintHistoryData * 8),
	]


class TyreSetData(Packet):
	_fields_ = [
		("actual_tyre_compound", ctypes.c_uint8),
		("visual_tyre_compound", ctypes.c_uint8),
		("wear", ctypes.c_uint8),
		("available", ctypes.c_uint8),
		("recommended_session", ctypes.c_uint8),
		("life_span", ctypes.c_uint8),
		("usable_life", ctypes.c_uint8),
		("lap_delta_time", ctypes.c_int16),
		("fitted", ctypes.c_uint8),
	]


class PacketTyreSetsData(Packet):
	_fields_ = [
		("header", PacketHeader),
		("car_idx", ctypes.c_uint8),
		("tyre_set_data", TyreSetData * 20),
		("fitted_idx", ctypes.c_uint8),
	]


class PacketMotionExData(Packet):
	_fields_ = [
		("header", PacketHeader),
		("suspension_position", ctypes.c_float * 4),
		("suspension_velocity", ctypes.c_float * 4),
		("suspension_acceleration", ctypes.c_float * 4),
		("wheel_speed", ctypes.c_float * 4),
		("wheel_slip_ratio", ctypes.c_float * 4),
		("wheel_slip_angle", ctypes.c_float * 4),
		("wheel_lat_force", ctypes.c_float * 4),
		("wheel_long_force", ctypes.c_float * 4),
		("height_of_cogabove_ground", ctypes.c_float),
		("local_velocity_x", ctypes.c_float),
		("local_velocity_y", ctypes.c_float),
		("local_velocity_z", ctypes.c_float),
		("angular_velocity_x", ctypes.c_float),
		("angular_velocity_y", ctypes.c_float),
		("angular_velocity_z", ctypes.c_float),
		("angular_acceleration_x", ctypes.c_float),
		("angular_acceleration_y", ctypes.c_float),
		("angular_acceleration_z", ctypes.c_float),
		("front_wheels_angle", ctypes.c_float),
		("wheel_vert_force", ctypes.c_float * 4),
		("front_aero_height", ctypes.c_float),
		("rear_aero_height", ctypes.c_float),
		("front_roll_angle", ctypes.c_float),
		("rear_roll_angle", ctypes.c_float),
		("chassis_yaw", ctypes.c_float),
	]


class TimeTrialDataSet(Packet):
	_fields_ = [
		("car_idx", ctypes.c_uint8),
		("team_id", ctypes.c_uint8),
		("lap_time_in_ms", ctypes.c_uint32),
		("sector1time_in_ms", ctypes.c_uint32),
		("sector2time_in_ms", ctypes.c_uint32),
		("sector3time_in_ms", ctypes.c_uint32),
		("traction_control", ctypes.c_uint8),
		("gearbox_assist", ctypes.c_uint8),
		("anti_lock_brakes", ctypes.c_uint8),
		("equal_car_performance", ctypes.c_uint8),
		("custom_setup", ctypes.c_uint8),
		("valid", ctypes.c_uint8),
	]


class PacketTimeTrialData(Packet):
	_fields_ = [
		("header", PacketHeader),
		("player_session_best_data_set", TimeTrialDataSet),
		("personal_best_data_set", TimeTrialDataSet),
		("rival_data_set", TimeTrialDataSet),
	]


HEADER_FIELD_TO_PACKET_TYPE = {
	(2024, 1, 0) : PacketMotionData,
	(2024, 1, 1) : PacketSessionData,
	(2024, 1, 2) : PacketLapData,
	(2024, 1, 3) : PacketEventData,
	(2024, 1, 4) : PacketParticipantsData,
	(2024, 1, 5) : PacketCarSetupData,
	(2024, 1, 6) : PacketCarTelemetryData,
	(2024, 1, 7) : PacketCarStatusData,
	(2024, 1, 8) : PacketFinalClassificationData,
	(2024, 1, 9) : PacketLobbyInfoData,
	(2024, 1, 10) : PacketCarDamageData,
	(2024, 1, 11) : PacketSessionHistoryData,
	(2024, 1, 12) : PacketTyreSetsData,
	(2024, 1, 13) : PacketMotionExData,
	(2024, 1, 14) : PacketTimeTrialData,
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
	14: 'PacketTimeTrialData',
}

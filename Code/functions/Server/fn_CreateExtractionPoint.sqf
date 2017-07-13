if (!isServer) exitWith {};

private ["_markerNo", "_markerName"];

_markerNo = _this select 0;
_markerName = "drn_Escape_ExtractionPos" + str _markerNo;
_markerName2 = "drn_Escape_ExtractionPos" + str _markerNo + "_1";
//private _pos = getMarkerPos _markerName;

private _location = "Land_HelipadEmpty_F" createvehicle (getMarkerPos _markerName);
private _location = "Land_HelipadEmpty_F" createvehicle (getMarkerPos _markerName2);

//_location setvariable ["A3E_ExtractionOnStandby",true];

_isWater = surfaceIsWater (getMarkerPos _markerName);

private _code = compile format["[%1,%2,_this] call A3E_fnc_firedNearExtraction;",_markerNo,_isWater];

_location addeventhandler["firedNear",_code];
diag_log format["fn_CreateExtractionPoint: eventhandler added at %1",(getpos _location)];

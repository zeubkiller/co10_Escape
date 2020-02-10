private["_zoneIndex"];


// ### Basic bootstrap and definitions ###
if(isNil("a3e_patrolZoneIndex")) then {
	a3e_patrolZoneIndex = 0;
	_zoneIndex = 0;
} else {
	a3e_patrolZoneIndex = a3e_patrolZoneIndex + 1;
	_zoneIndex = a3e_patrolZoneIndex;
};
if(isNil("a3e_patrolZones")) then {
	a3e_patrolZones = [];
};

params["_zone"];

private _zonePosition = (_zone select 0);
private _zoneDir = (_x select 1);
private _zoneShape = (_x select 2);
private _zoneSizeXY = (_x select 3);
private _zoneColor = (_x select 4);
private _zoneArea = (_zoneSizeXY select 0)*(_zoneSizeXY select 1);

//Selects the side based on the zone size. Small zones are occupied by locals while large cities are occupied by OPFOR
//If param separated zones are on and is supported by terrain side will be spawned according to villagemarker color
private _side = A3E_VAR_Side_Ind;
if((Param_Separation>0) && (!isNil ("_zoneColor") )) then {
	if(_zoneColor == "ColorRed") then {
		_side = A3E_VAR_Side_Opfor;
	};
	if(_zoneColor == "ColorGreen") then {
		_side = A3E_VAR_Side_Ind;
	};
} else {
	private _side = A3E_VAR_Side_Ind;
	if(_zoneArea > 5000) then {
		_side = A3E_VAR_Side_Opfor;
	};
};

private _name = format["A3E_ZoneMarker%1",_zoneIndex];
private _marker = createMarker [_name,(_x select 0)];
_marker setMarkerDir (_x select 1);
_marker setMarkerShape (_x select 2);
_marker setMarkerSize (_x select 3);
_marker setMarkerColor (_x select 4);
_name = format["A3E_ZoneMarkerText%1",_zoneIndex];
_marker setMarkerAlpha 0;

if(A3E_Debug) then {
	_marker setMarkerAlpha 0.5;
};

private _triggerRange = missionNamespace getvariable ["Param_EnemySpawnDistance",800];

private _trigger = createTrigger["EmptyDetector", _zonePosition, false];
//_trigger setTriggerInterval 5;
private _playerGroup = [] call a3e_fnc_getPlayerGroup;
_trigger triggerAttachVehicle [vehicle (units _playerGroup select 0)];
_trigger setTriggerActivation["MEMBER", "PRESENT", true];
private _rectangle = false;
if(_zoneShape == "RECTANGLE") then {
	_rectangle = true;
};
_trigger setTriggerArea[(_zoneSizeXY select 0)+_triggerRange, (_zoneSizeXY select 1)+_triggerRange, _zoneDir, _rectangle];
_trigger setTriggerTimeout [1, 1, 1, true];
private _activation = format["[%1] call A3E_FNC_activatePatrolZone;",_zoneIndex];
private _deactivation = format["[%1] call A3E_FNC_deactivatePatrolZone;",_zoneIndex];
_trigger setTriggerStatements["this",_activation,_deactivation];



private _zoneArray = [
			["trigger",_trigger],
			["marker",_marker],
			["side",_side],
			["zoneArea",_zoneArea],
			["initialized",false],
			["active",false],
			["patrols",[]],
			["housePatrols",[]]
			];
a3e_patrolZones set [_zoneIndex,_zoneArray];





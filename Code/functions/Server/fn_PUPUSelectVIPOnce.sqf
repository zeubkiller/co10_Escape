private _max_score = 0;
{
	_pScore = score _x;
	if (_pScore < 0) then {
		_pScore = 0;
	};
	if (_pScore > _max_score) then {
		_max_score = _pScore;
	};
} foreach (call A3E_fnc_GetPlayers);

_chosen = nil;
_chosen_roll = -1;
{
	_pScore = score _x;
	if (_pScore < 0) then {
		_pScore = 0;
	};
	_pScore = _max_score - _pScore;
	_roll = random _pScore;
	
	if (_chosen_roll < _roll) then {
		_chosen = _x;
		_chosen_roll = _roll;
	};
	
} foreach (call A3E_fnc_GetPlayers);

//_chosen = call A3E_fnc_GetRandomPlayer;

private _vip_player = profileNamespace getVariable ["A3E_VIPPlayer",nil];
if(!isNil("_vip_player")) then {
	_vip_player setvariable["A3E_PUPUPlayerIsVIP",false,true];
};
_chosen setvariable["A3E_PUPUPlayerIsVIP",true,true];
profileNamespace setVariable ["A3E_VIPPlayer", _chosen];


params[["_initial",true]];

if(isNil("A3E_Param_TimeMultiplier")) then {
	A3E_Param_TimeMultiplier = 1;
};

private _totalVIPTime = 15 * 60;//15 min
//private _totalVIPTime = 25;//TEMP!//PUPU

private _initBossWarningChangeTime = 15;

private _bossWarningChangeTime = (_totalVIPTime/5);
private _bossWaitTime = (_totalVIPTime*4/5); // 12 min

if(_initial) then {
	profileNamespace setVariable ["A3E_VIPPlayer", nil];
	sleep (_initBossWarningChangeTime);
} else {
	systemchat ("VIP change in "+str (_bossWarningChangeTime/60) + " minutes ("+str (_bossWarningChangeTime) + " seconds)");
	sleep (_bossWarningChangeTime);
};

[] call A3E_fnc_PUPUSelectVIPOnce;

private _vip_player = profileNamespace getVariable ["A3E_VIPPlayer",nil];
_msg = format["%1 is the new VIP for %2 minutes.",name _vip_player, str ((_totalVIPTime)/60)];
_msg remoteExec ["systemchat", 0, false];
sleep (_bossWaitTime);

[false] spawn A3E_fnc_PUPUSelectVIPPeriodic;
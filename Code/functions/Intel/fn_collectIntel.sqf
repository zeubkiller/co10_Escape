params ["_unit", "_container"];
private _intelItems = missionnamespace getvariable ["A3E_IntelItems",["Files","FileTopSecret","FilesSecret","FlashDisk","DocumentsSecret","Wallet_ID","FileNetworkStructure","MobilePhone","SmartPhone"]];
private _digitalIntelItems = ["FlashDisk", "MobilePhone", "SmartPhone"];
if(A3E_Param_UseIntel==1) then {

	private _intels = magazines _unit select {_x in _intelItems};
	if (count _intels != 0) then {
	
		_is_vip = (_unit getvariable ["A3E_PUPUPlayerIsVIP",false]);
		//format["A3E_PUPUPlayerIsVIP = %1", _is_vip] remoteexec ["systemchat",0];
		if (_is_vip) then {
		
			private _has_digital_but_no_laptop = false;
			private _reveal_intels = [];
			_unit_has_laptop = ("Laptop_Closed" in (vestItems _unit + uniformItems _unit + backpackItems _unit + assignedItems _unit));
			{
				if (!(_x in _digitalIntelItems) || _unit_has_laptop) then {
					_reveal_intels append [_x];
				} else {
					_has_digital_but_no_laptop = true;
				};
			} foreach _intels;
			
			if (count _reveal_intels != 0) then {
				[count _reveal_intels] remoteExec ["A3E_fnc_RevealPOI", 2];
				_unit addScore ((count _reveal_intels)*5);
				{
					_unit removeMagazine _x;	
				} foreach _reveal_intels;
			};
			
			if (_has_digital_but_no_laptop) then {
				format["%1 has digital intel but no laptop.", name _unit] remoteexec ["systemchat",0];
			};
		} else {
			format["%1 has intel but is not VIP.", name _unit] remoteexec ["systemchat",0];
		};
	};
};
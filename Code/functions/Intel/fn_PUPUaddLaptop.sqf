params["_unit"];
private _chance = ((missionnamespace getvariable ["A3E_Param_IntelChance",20])/5);

if(_chance >= random 100) then {

	private _containers = [];
	if(!isNull(uniformContainer _unit)) then {_containers pushBack 1;};
	if(!isNull(vestContainer _unit)) then {_containers pushBack 2;};
	if(!isNull(backpackContainer _unit)) then {_containers pushBack 3;};	
	switch (selectRandom _containers) do {
		case 1: { _unit addItemToUniform ("Laptop_Closed"); };
		case 2: { _unit addItemToVest ("Laptop_Closed");};
		case 3: { _unit addItemToBackpack ("Laptop_Closed");};
		default { _unit addMagazineGlobal ("Laptop_Closed");};
	};
};




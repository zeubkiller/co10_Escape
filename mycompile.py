import json
import os
import argparse
from shutil import copy, copyfile, copytree, ignore_patterns, rmtree
import subprocess
from datetime import datetime
from subprocess import call

parser = argparse.ArgumentParser(description='Compile and pack escape mod')
parser.add_argument('--mod', help='Specify mod to use', default='')
parser.add_argument('-m', '--mission', help='Specify mission to use', default='')
parser.add_argument('-i', '--island', help='Specify island to use', default='')
# parser.add_argument('-a', '--addon', help='Specify addon to use', default='')
parser.add_argument('-f', '--full',help='Compile and pack mods', default=False, action="store_true")
parser.add_argument('-s', '--symlink',help='Create symlink in arma3 MpMission folder', default=False, action="store_true")

args = parser.parse_args()

print('Loading config ...')
with open('Configs/config_local.json') as json_data_file:
    config_local_data = json.load(json_data_file)
if(not os.path.exists(config_local_data['arma3_editor_MpMissionPath'])):
    print("Arma3 mpMission path is wrong or empty")
    exit()

arma3_MpMission_path = config_local_data['arma3_editor_MpMissionPath']

with open('Configs/config.json') as json_data_file:
    data = json.load(json_data_file)
mods = data['Mods'];
islands = data['Islands']
missions = data['Missions']
addons = data['Addons']
for scfg in data['Subconfigs']:
    print("Parsing config "+scfg)    
    with open(scfg) as json_adata:  
        adata = json.load(json_adata)  
        mods = mods + adata['Mods'];
        islands = islands + adata['Islands'];
        missions = missions + adata['Missions'];
        addons = addons + adata['Addons']
#Add devbuild number to version
#if os.environ['GIT_BRANCH'] == "develop":
data['replace']['VERSION'] += ' dev ' + datetime.today().strftime("%y%m%d %H%M")
data['replace']['RELEASE'] = 'Mission'

if args.mod != '':
    print("Filter missions by mods with " + args.mod)
    missions = [m for m in missions if m['mod'] == args.mod]
    if missions==[]:
        print("Error No match for mod " + args.mod)
        exit()
if args.island != '':
    print("Filter missions by islands with " + args.island)
    missions = [m for m in missions if m['island'] == args.island]
    if missions==[]:
        print("Error No match for island " + args.island)
        exit()
if args.mission != '':
    print("Filter missions with " + args.mission)
    missions = [m for m in missions if m['name'] == args.mission]
    if missions==[]:
        print("Error No match for mission " + args.mission)
        exit()
# if args.addon != '':
#     print("Filter addons with " + args.addon)
#     addons = [m for m in addons if m['name'] == args.addon]
#     if addons==[]:
#         print("Error No match for addon " + args.addon)
#         exit()

print('making DIR')
for directory in [data['BuildDir'], data['PackedDir'], data['PackedDir']+'/Addons', data['PackedDir']+'/Missions']:
    print('making DIR... : ', directory)
    if not os.path.exists(directory):
        print('making DIR!')
        print(directory)
        os.mkdir(directory)
    else:
        print('not making DIR!')
print('making DIR done...')

for the_file in os.listdir(data['BuildDir']):
    file_path = os.path.join(data['BuildDir'], the_file)
    if os.path.isfile(file_path):
        os.unlink(file_path)
        
#for mission in missions:
#    modname =  mission['mod']
#    islandname = mission['island']
#    print ('Creating a mission with mod', modname, 'on', islandname)

# exit(0)

for mission in missions:
    modname =  mission['mod']
    islandname = mission['island']
    print ('Creating a mission with mod', modname, 'on', islandname)
    missionMod = None
    missionIsland = None
    for mod in mods:
        if mod['name'] == modname:
            missionMod = mod
    for island in islands:
        if island['name'] == islandname:
            missionIsland = island
    if missionMod is None:
        raise NameError('Mod was not found')
    if missionIsland is None:
        raise NameError('Island was not found')
    if not 'name' in mission:
        mission['name'] = data['Missionname']+'_'+missionMod['name']
    missionFolderName = mission['name']+'.'+ missionIsland['class']
    missiondir = data['BuildDir'] + '/missionfiles/' + missionFolderName
    if os.path.exists(missiondir):
        rmtree(missiondir)
    copytree(data['Code']+'/',missiondir, ignore=ignore_patterns('*.git'))
    copytree(missionIsland['path']+'/',missiondir+'/Island/', ignore=ignore_patterns('*.git'))
    copytree(missionMod['path']+'/',missiondir+'/Units', ignore=ignore_patterns('*.git'))
    
    # Create symlink in MPMision folder to test change in live
    arma3_mpmission_mission_folder = os.path.join(arma3_MpMission_path, missionFolderName)
    if(args.symlink and not os.path.exists(arma3_mpmission_mission_folder)):
        print('################ Command to run for symlink: ################')
        print('mklink /J "' + arma3_mpmission_mission_folder + '" "' + os.path.abspath(missiondir) + '"')
        print('#############################################################')

    required = ''
    for req in missionMod['require']:
        required = required + '"'+ req + '",'
    #if len(required) == 0 :
    #    required = '\b\b'

    copy('./Missions/'+mission['sqm']+'/mission.sqm',missiondir+'/mission.sqm')
    replace = dict(list(data['replace'].items()) + list(missionMod['replace'].items()) + list(missionIsland['replace'].items()));
    replace['REQUIRE'] = required
    for root, subFolders, files in os.walk(missiondir):
        for rfile in data['ParsedFiles']:
            if rfile in files:
                print('Found',rfile,'at',os.path.join(root, rfile))
                s=open(os.path.join(root, rfile)).read()
                for key in replace:
                    if '{* '+key+' *}' in s:
                        # print('Found occurrence of',key,'in file. Replacing with',replace[key])
                        s=s.replace('{* '+key+' *}', replace[key])
                    f=open(os.path.join(root, rfile), 'w')
                    f.write(s)
                    f.flush()
                    f.close()
    print("Cpbo extraction")
    f = open(os.devnull, 'w') #Silence the cpbo output
    subprocess.call(["cpbo.exe", "-y", "-p", missiondir], stdout=f)
    copyfile(missiondir + ".pbo", data['PackedDir']+'/Missions/'+mission['name']+'.'+ missionIsland['class']+'.pbo') #Copy build artifact


print("**************************** Mod compilation finished !!!! ****************************")
if not args.full:
    exit()

print("Packing in progress ...")

t = []
for m in missions:
    t.append(m['name'].lower())
addonFolders = list(set(t))
pbos = []
for s in addonFolders:
    print (s)
    listOfMissions = []
    required = []
    missionNumber = 0
    missionMod = [] #should be the same across all missions in a folder
    for mission in missions:
        if s == mission['name'].lower():
            for mod in mods:
                if mod['name'].lower() == mission['mod'].lower():
                    missionMod = mod
            missionIsland = None
            for island in islands:
                if island['name'] == mission['island']:
                    missionIsland = island
            for req in missionMod['require']:
                required.append(req.lower())
            missiondir = mission['name']+'.'+ missionIsland['class']
            addonMissionFolder = mission['name']+'\\'+mission['name']+str(missionNumber)+'.'+ missionIsland['class'] 
            if os.path.exists(data['BuildDir'] + '/addons/' +mission['name']+'/'+mission['name']+str(missionNumber)+'.'+ missionIsland['class']):
                rmtree(data['BuildDir'] + '/addons/' +mission['name']+'/'+mission['name']+str(missionNumber)+'.'+ missionIsland['class'])
            copytree(data['BuildDir'] + '/missionfiles/' + missiondir,data['BuildDir'] + '/addons/' +mission['name']+'/'+mission['name']+str(missionNumber)+'.'+ missionIsland['class'], ignore=ignore_patterns('*.git'))
            ds=open(data['BuildDir'] + '/addons/' +mission['name']+'/'+mission['name']+str(missionNumber)+'.'+ missionIsland['class']+'/include/defines.hpp').read()
            ds=ds.replace('#define RELEASE "Mission"', '#define RELEASE "Addon"')
            f=open(data['BuildDir'] + '/addons/' +mission['name']+'/'+mission['name']+str(missionNumber)+'.'+ missionIsland['class']+'/include/defines.hpp', 'w')
            f.write(ds)
            f.flush()
            f.close()
            listOfMissions.append([mission['name']+str(missionNumber),addonMissionFolder,data['replace']['MISSION_FULL']+" "+missionMod['replace']['MOD'] + " " + data['replace']['VERSION']])
            missionNumber=missionNumber+1
            print ("Copying " + missiondir+" to addonfolder "+addonMissionFolder + " ("+data['replace']['MISSION_FULL']+" "+missionMod['replace']['MOD'] + " " + data['replace']['VERSION']+")")
    requiredList = list(set(required))
    requiredString = ''
    for req in requiredList:
        requiredString = requiredString + '"'+ req + '",'
    requiredString = requiredString[:-1]
    cfgFile = open(data['BuildDir'] + '/addons/' +s+'/config.cpp', 'w')
    toFile = "class CfgPatches\n{\n\tclass "+s+"\n\t{\n\t\tname = \""+data['replace']['MISSION_FULL']+" "+missionMod['replace']['MOD']+ " " + data['replace']['VERSION']+"\";\n\t\tauthor = \"NeoArmageddon and Scruffy\";\n\t\turl = \"https://forums.bistudio.com/forums/topic/180080-co10-escape\";\n\t\tunits[] = {};\n\t\tweapons[] = {};\n\t\trequiredVersion = 1.0;\n\t\trequiredAddons[] = {"+requiredString+"};\n\t};\n};\nclass CfgMissions\n{\n\tclass MPMissions\n\t{\n"""
    for m in listOfMissions:
        toFile += "\t\tclass "+m[0]+"\n\t\t{\n"
        toFile += "\t\t\tbriefingName = \""+m[2]+"\";\n"
        toFile += "\t\t\tdirectory = \""+m[1]+"\";\n"
        toFile += "\t\t};\n"
    toFile += "\t};\n};"
    cfgFile.write(toFile)
    cfgFile.close()
    subprocess.call(["cpbo.exe", "-y", "-p", data['BuildDir'] + '/addons/' + s]) #Pack folder to pbo
    print("Done packing pbo of "+data['replace']['MISSION_FULL']+" "+missionMod['replace']['MOD'])  
    pbos.append([s + '.pbo',missionMod['name']])
print("Done packing pbos. Start collecting...")    
for addon in addons:
    if not os.path.exists(data['BuildDir']+'/addons/' + '@'+data['Missionname']+'_'+addon['name']):
        os.makedirs(data['BuildDir']+'/addons/' + '@'+data['Missionname']+'_'+addon['name']) #Create target folder
        os.makedirs(data['BuildDir']+'/addons/' + '@'+data['Missionname']+'_'+addon['name']+'/addons') #Create target folder
    for mod in addon['mods']:
        for pbo in pbos:
            print(pbo[0]+" "+pbo[1]+" "+mod)
            if pbo[1] == mod:
                if os.path.exists(data['BuildDir']+'/addons/' + '@'+data['Missionname']+'_'+addon['name']+'/addons/'+pbo[0]):
                    os.remove(data['BuildDir']+'/addons/' + '@'+data['Missionname']+'_'+addon['name']+'/addons/'+pbo[0])
                copyfile(data['BuildDir'] + '/addons/' + pbo[0], data['BuildDir']+'/addons/' + '@'+data['Missionname']+'_'+addon['name']+'/addons/'+pbo[0]) #Copy build artifact
        if os.path.exists(data['PackedDir']+'/Addons/'+ '@'+data['Missionname']+'_'+addon['name']):
            rmtree(data['PackedDir']+'/Addons/'+ '@'+data['Missionname']+'_'+addon['name'])
        copytree(data['BuildDir']+'/addons/' + '@'+data['Missionname']+'_'+addon['name'],data['PackedDir']+'/Addons/'+ '@'+data['Missionname']+'_'+addon['name'], ignore=ignore_patterns('*.git'))

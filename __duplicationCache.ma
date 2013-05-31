//Maya ASCII 2011 scene
//Name: __duplicationCache.ma
//Last modified: Fri, Nov 18, 2011 02:08:22 PM
//Codeset: 1252
requires maya "2011";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2011";
fileInfo "version" "2011";
fileInfo "cutIdentifier" "201009060019-781618";
fileInfo "osv" "Microsoft Windows 7 Enterprise Edition, 64-bit Windows 7  (Build 7600)\n";
createNode transform -n "ClavicleJoint__instance_2:module_grp";
lockNode -l 1 -lu 1;
createNode transform -n "ClavicleJoint__instance_2:joints_grp" -p "ClavicleJoint__instance_2:module_grp";
lockNode -l 1 -lu 1;
createNode joint -n "ClavicleJoint__instance_2:clav_1_joint" -p "ClavicleJoint__instance_2:joints_grp";
	setAttr ".v" no;
	setAttr ".t";
	setAttr ".s";
	setAttr ".rp";
	setAttr ".rpt";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo";
lockNode -l 1 -lu 1;
createNode joint -n "ClavicleJoint__instance_2:clav_2_joint" -p "ClavicleJoint__instance_2:clav_1_joint";
	setAttr ".v" no;
	setAttr ".t";
	setAttr ".ty";
	setAttr ".tz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
lockNode -l 1 -lu 1;
createNode pointConstraint -n "ClavicleJoint__instance_2:clav_1_joint_pointConstraint" 
		-p "ClavicleJoint__instance_2:clav_1_joint";
	addAttr -ci true -k true -sn "w0" -ln "clav_1_joint_translation_controlW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr ".t";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr ".r";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr ".s";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg";
	setAttr -k on ".w0";
lockNode -l 1 -lu 1;
createNode ikEffector -n "ClavicleJoint__instance_2:clav_1_joint_ikEffector" -p "ClavicleJoint__instance_2:clav_1_joint";
	setAttr ".v" no;
	setAttr ".t";
	setAttr ".hd" yes;
lockNode -l 1 -lu 1;
createNode ikHandle -n "ClavicleJoint__instance_2:clav_1_joint_ikHandle" -p "ClavicleJoint__instance_2:joints_grp";
	setAttr ".v" no;
	setAttr ".t";
	setAttr ".rp";
	setAttr ".rpt";
	setAttr ".pv";
	setAttr ".roc" yes;
lockNode -l 1 -lu 1;
createNode poleVectorConstraint -n "ClavicleJoint__instance_2:clav_1_joint_ikHandle_poleVectorConstraint1" 
		-p "ClavicleJoint__instance_2:clav_1_joint_ikHandle";
	addAttr -ci true -k true -sn "w0" -ln "clav_1_joint_translation_control_poleVectorLocatorW0" 
		-dv 1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr ".t";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr ".r";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr ".s";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg";
	setAttr ".rst" -type "double3" 0 -0.5 0 ;
	setAttr -k on ".w0";
lockNode -l 1 -lu 1;
createNode pointConstraint -n "ClavicleJoint__instance_2:clav_1_joint_ikHandle_pointConstraint" 
		-p "ClavicleJoint__instance_2:clav_1_joint_ikHandle";
	addAttr -ci true -k true -sn "w0" -ln "clav_2_joint_endPosLocatorW0" -dv 1 -min 
		0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr ".t";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr ".r";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr ".s";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg";
	setAttr ".rst" -type "double3" 4 0 0 ;
	setAttr -k on ".w0";
lockNode -l 1 -lu 1;
createNode transform -n "ClavicleJoint__instance_2:clav_1_joint_rootPosLocator" 
		-p "ClavicleJoint__instance_2:joints_grp";
	setAttr ".v" no;
	setAttr ".t";
	setAttr ".rp";
	setAttr ".rpt";
lockNode -l 1 -lu 1;
createNode locator -n "ClavicleJoint__instance_2:clav_1_joint_rootPosLocatorShape" 
		-p "ClavicleJoint__instance_2:clav_1_joint_rootPosLocator";
	setAttr -k off ".v";
lockNode -l 1 -lu 1;
createNode pointConstraint -n "ClavicleJoint__instance_2:clav_1_joint_rootPosLocator_pointConstraint" 
		-p "ClavicleJoint__instance_2:clav_1_joint_rootPosLocator";
	addAttr -ci true -k true -sn "w0" -ln "clav_1_jointW0" -dv 1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr ".t";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr ".r";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr ".s";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg";
	setAttr -k on ".w0";
lockNode -l 1 -lu 1;
createNode transform -n "ClavicleJoint__instance_2:clav_2_joint_endPosLocator" -p
		 "ClavicleJoint__instance_2:joints_grp";
	setAttr ".v" no;
	setAttr ".t";
	setAttr ".rp";
	setAttr ".rpt";
lockNode -l 1 -lu 1;
createNode locator -n "ClavicleJoint__instance_2:clav_2_joint_endPosLocatorShape" 
		-p "ClavicleJoint__instance_2:clav_2_joint_endPosLocator";
	setAttr -k off ".v";
lockNode -l 1 -lu 1;
createNode pointConstraint -n "ClavicleJoint__instance_2:clav_2_joint_endPosLocator_pointConstraint" 
		-p "ClavicleJoint__instance_2:clav_2_joint_endPosLocator";
	addAttr -ci true -k true -sn "w0" -ln "clav_2_joint_translation_controlW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr ".t";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr ".r";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr ".s";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg";
	setAttr ".rst" -type "double3" 4 0 0 ;
	setAttr -k on ".w0";
lockNode -l 1 -lu 1;
createNode transform -n "ClavicleJoint__instance_2:orientationControls_grp" -p "ClavicleJoint__instance_2:module_grp";
lockNode -l 1 -lu 1;
createNode transform -n "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp" 
		-p "ClavicleJoint__instance_2:orientationControls_grp";
	setAttr ".t";
	setAttr ".r";
	setAttr ".ro";
	setAttr ".s";
	setAttr ".rp";
	setAttr ".rpt";
lockNode -l 1 -lu 1;
createNode transform -n "ClavicleJoint__instance_2:clav_1_joint_orientation_control" 
		-p "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp";
	setAttr -l on -k off ".v";
	setAttr ".t";
	setAttr -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr ".r";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr ".s";
	setAttr -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
lockNode -l 1 -lu 1;
createNode mesh -n "ClavicleJoint__instance_2:clav_1_joint_orientation_controlShape" 
		-p "ClavicleJoint__instance_2:clav_1_joint_orientation_control";
	addAttr -ci true -sn "mso" -ln "miShadingSamplesOverride" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "msh" -ln "miShadingSamples" -min 0 -smx 8 -at "float";
	addAttr -ci true -sn "mdo" -ln "miMaxDisplaceOverride" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "mmd" -ln "miMaxDisplace" -min 0 -smx 1 -at "float";
	setAttr -k off ".v";
	setAttr -s 2 ".iog[0].og";
	setAttr ".iog[0].og[0].gcl" -type "componentList" 2 "f[0:10]" "f[28:33]";
	setAttr ".iog[0].og[1].gcl" -type "componentList" 1 "f[11:27]";
	setAttr ".iog[0].og";
	setAttr ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".ciog[0].cog";
	setAttr ".ciog";
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 72 ".uvst[0].uvsp[0:71]" -type "float2" 0.62640893 0.064408526 
		0.54828387 0.0076473951 0.45171607 0.00764741 0.37359107 0.064408556 0.34375 0.15625001 
		0.37359107 0.24809146 0.4517161 0.3048526 0.54828393 0.3048526 0.62640893 0.24809144 
		0.65625 0.15625 0.375 0.3125 0.40000001 0.3125 0.42500001 0.3125 0.45000002 0.3125 
		0.47500002 0.3125 0.5 0.3125 0.52499998 0.3125 0.54999995 0.3125 0.57499993 0.3125 
		0.5999999 0.3125 0.62499988 0.3125 0.5 0.68843985 0.375 0.3125 0.40000001 0.3125 
		0.5 0.68843985 0.42500001 0.3125 0.45000002 0.3125 0.47500002 0.3125 0.5 0.3125 0.52499998 
		0.3125 0.54999995 0.3125 0.57499993 0.3125 0.5999999 0.3125 0.62499988 0.3125 0.62640893 
		0.064408526 0.65625 0.15625 0.62640893 0.24809144 0.54828393 0.3048526 0.4517161 
		0.3048526 0.37359107 0.24809146 0.34375 0.15625001 0.37359107 0.064408556 0.45171607 
		0.00764741 0.54828387 0.0076473951 0.375 0 0.625 0 0.625 0.25 0.375 0.25 0.625 0.5 
		0.375 0.5 0.625 0.75 0.375 0.75 0.625 1 0.375 1 0.875 0 0.875 0.25 0.125 0 0.125 
		0.25 0.375 0 0.625 0 0.625 0.25 0.375 0.25 0.625 0.5 0.375 0.5 0.625 0.75 0.375 0.75 
		0.625 1 0.375 1 0.875 0 0.875 0.25 0.125 0 0.125 0.25;
	setAttr ".uvst";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".o";
	setAttr ".bnr" 0;
	setAttr -s 38 ".pt[0:37]" -type "float3"  0.5 0 0 0.5 0 0 0.5 0 0 0.5 
		0 0 0.5 0 0 0.5 0 0 0.5 0 0 0.5 0 0 0.5 0 0 0.5 0 0 0.5 0 0 0.5 0 0 0.5 0 0 0.5 0 
		0 0.5 0 0 0.5 0 0 0.5 0 0 0.5 0 0 0.5 0 0 0.5 0 0 0.5 0 0 0.5 0 0 0.5 0 0 0.5 0 0 
		0.5 0 0 0.5 0 0 0.5 0 0 0.5 0 0 0.5 0 0 0.5 0 0 0.5 0 0 0.5 0 0 0.5 0 0 0.5 0 0 0.5 
		0 0 0.5 0 0 0.5 0 0 0.5 0 0;
	setAttr -s 38 ".vt[0:37]"  0.095147073 0.49463958 -0.069128409 0.036342937 
		0.49463958 -0.11185211 -0.036342964 0.49463958 -0.11185209 -0.095147088 0.49463958 
		-0.069128387 -0.11760826 0.49463958 7.0099975e-009 -0.095147073 0.49463958 0.069128402 
		-0.036342941 0.49463958 0.11185209 0.036342949 0.49463958 0.11185209 0.095147066 
		0.49463958 0.069128387 0.11760824 0.49463958 0 -4.5564983e-009 0.72985607 -4.205998e-010 
		0.095147073 0.069128409 0.49463958 0.036342937 0.11185211 0.49463958 -0.036342964 
		0.11185209 0.49463958 -0.095147088 0.069128387 0.49463958 -0.11760826 -7.0099975e-009 
		0.49463958 -0.095147073 -0.069128402 0.49463958 -0.036342941 -0.11185209 0.49463958 
		0.036342949 -0.11185209 0.49463958 0.095147066 -0.069128387 0.49463958 0.11760824 
		1.0983205e-016 0.49463958 -4.5564983e-009 4.2059997e-010 0.72985607 -0.5 -0.075000018 
		-0.5 0.5 -0.075000018 -0.5 -0.5 -0.074999988 0.5 0.5 -0.074999988 0.5 -0.5 0.075000018 
		0.5 0.5 0.075000018 0.5 -0.5 0.074999988 -0.5 0.5 0.074999988 -0.5 -0.5 -0.5 -0.074999988 
		0.5 -0.5 -0.074999988 -0.5 -0.5 0.075000018 0.5 -0.5 0.075000018 -0.5 0.5 0.074999988 
		0.5 0.5 0.074999988 -0.5 0.5 -0.075000018 0.5 0.5 -0.075000018;
	setAttr -s 64 ".ed[0:63]"  0 1 0 1 2 0 
		2 3 0 3 4 0 4 5 0 5 6 0 
		6 7 0 7 8 0 8 9 0 9 0 0 
		0 10 0 1 10 0 2 10 0 3 10 0 
		4 10 0 5 10 0 6 10 0 7 10 0 
		8 10 0 9 10 0 11 12 0 12 13 0 
		13 14 0 14 15 0 15 16 0 16 17 0 
		17 18 0 18 19 0 19 20 0 20 11 0 
		11 21 0 12 21 0 13 21 0 14 21 0 
		15 21 0 16 21 0 17 21 0 18 21 0 
		19 21 0 20 21 0 22 23 0 24 25 0 
		26 27 0 28 29 0 22 24 0 23 25 0 
		24 26 0 25 27 0 26 28 0 27 29 0 
		28 22 0 29 23 0 30 31 0 32 33 0 
		34 35 0 36 37 0 30 32 0 31 33 0 
		32 34 0 33 35 0 34 36 0 35 37 0 
		36 30 0 37 31 0;
	setAttr -s 34 ".fc[0:33]" -type "polyFaces" 
		f 3 0 11 -11 
		mu 0 3 10 11 21 
		f 3 1 12 -12 
		mu 0 3 11 12 21 
		f 3 2 13 -13 
		mu 0 3 12 13 21 
		f 3 3 14 -14 
		mu 0 3 13 14 21 
		f 3 4 15 -15 
		mu 0 3 14 15 21 
		f 3 5 16 -16 
		mu 0 3 15 16 21 
		f 3 6 17 -17 
		mu 0 3 16 17 21 
		f 3 7 18 -18 
		mu 0 3 17 18 21 
		f 3 8 19 -19 
		mu 0 3 18 19 21 
		f 3 9 10 -20 
		mu 0 3 19 20 21 
		f 10 -10 -9 -8 -7 -6 -5 -4 -3 -2 -1 
		
		mu 0 10 0 9 8 7 6 5 4 3 2 
		1 
		f 3 20 31 -31 
		mu 0 3 22 23 24 
		f 3 21 32 -32 
		mu 0 3 23 25 24 
		f 3 22 33 -33 
		mu 0 3 25 26 24 
		f 3 23 34 -34 
		mu 0 3 26 27 24 
		f 3 24 35 -35 
		mu 0 3 27 28 24 
		f 3 25 36 -36 
		mu 0 3 28 29 24 
		f 3 26 37 -37 
		mu 0 3 29 30 24 
		f 3 27 38 -38 
		mu 0 3 30 31 24 
		f 3 28 39 -39 
		mu 0 3 31 32 24 
		f 3 29 30 -40 
		mu 0 3 32 33 24 
		f 10 -30 -29 -28 -27 -26 -25 -24 -23 -22 -21 
		
		mu 0 10 34 35 36 37 38 39 40 41 42 
		43 
		f 4 40 45 -42 -45 
		mu 0 4 44 45 46 47 
		f 4 41 47 -43 -47 
		mu 0 4 47 46 48 49 
		f 4 42 49 -44 -49 
		mu 0 4 49 48 50 51 
		f 4 43 51 -41 -51 
		mu 0 4 51 50 52 53 
		f 4 -52 -50 -48 -46 
		mu 0 4 45 54 55 46 
		f 4 50 44 46 48 
		mu 0 4 56 44 47 57 
		f 4 52 57 -54 -57 
		mu 0 4 58 59 60 61 
		f 4 53 59 -55 -59 
		mu 0 4 61 60 62 63 
		f 4 54 61 -56 -61 
		mu 0 4 63 62 64 65 
		f 4 55 63 -53 -63 
		mu 0 4 65 64 66 67 
		f 4 -64 -62 -60 -58 
		mu 0 4 59 68 69 60 
		f 4 62 56 58 60 
		mu 0 4 70 58 61 71 ;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".atm" no;
lockNode -l 1 -lu 1;
createNode parentConstraint -n "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp_parentConstraint1" 
		-p "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp";
	addAttr -ci true -k true -sn "w0" -ln "clav_1_jointW0" -dv 1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr ".t";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr ".r";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr ".s";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg";
	setAttr -k on ".w0";
lockNode -l 1 -lu 1;
createNode scaleConstraint -n "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp_scaleConstraint1" 
		-p "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp";
	addAttr -ci true -k true -sn "w0" -ln "module_transformW0" -dv 1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr ".t";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr ".r";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr ".s";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg";
	setAttr -k on ".w0";
lockNode -l 1 -lu 1;
createNode transform -n "ClavicleJoint__instance_2:preferredAngleRepresentation_grp" 
		-p "ClavicleJoint__instance_2:module_grp";
lockNode -l 1 -lu 1;
createNode transform -n "ClavicleJoint__instance_2:hook_grp" -p "ClavicleJoint__instance_2:module_grp";
lockNode -l 1 -lu 1;
createNode joint -n "ClavicleJoint__instance_2:hook_root_joint" -p "ClavicleJoint__instance_2:hook_grp";
	setAttr ".v" no;
	setAttr ".t";
	setAttr ".ro";
	setAttr ".s";
	setAttr ".rp";
	setAttr ".rpt";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 89.999999999999986 ;
	setAttr ".jo";
lockNode -l 1 -lu 1;
createNode joint -n "ClavicleJoint__instance_2:hook_target_joint" -p "ClavicleJoint__instance_2:hook_root_joint";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0.0010000000474974513 2.2204460492503131e-019 0 ;
	setAttr ".t";
	setAttr ".ty";
	setAttr ".tz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -89.999999999999986 ;
lockNode -l 1 -lu 1;
createNode ikEffector -n "ClavicleJoint__instance_2:hook_root_joint_ikEffector" 
		-p "ClavicleJoint__instance_2:hook_root_joint";
	setAttr ".v" no;
	setAttr ".t";
	setAttr ".hd" yes;
lockNode -l 1 -lu 1;
createNode pointConstraint -n "ClavicleJoint__instance_2:hook_root_joint_pointConstraint" 
		-p "ClavicleJoint__instance_2:hook_root_joint";
	addAttr -ci true -k true -sn "w0" -ln "clav_1_joint_translation_controlW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr ".t";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr ".r";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr ".s";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg";
	setAttr -k on ".w0";
lockNode -l 1 -lu 1;
createNode transform -n "ClavicleJoint__instance_2:unhookedTarget" -p "ClavicleJoint__instance_2:hook_grp";
	setAttr ".v" no;
	setAttr ".t";
	setAttr ".rp";
	setAttr ".rpt";
lockNode -l 1 -lu 1;
createNode locator -n "ClavicleJoint__instance_2:unhookedTargetShape" -p "ClavicleJoint__instance_2:unhookedTarget";
	setAttr -k off ".v";
lockNode -l 1 -lu 1;
createNode pointConstraint -n "ClavicleJoint__instance_2:unhookedTarget_pointConstraint1" 
		-p "ClavicleJoint__instance_2:unhookedTarget";
	addAttr -ci true -k true -sn "w0" -ln "clav_1_joint_translation_controlW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr ".t";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr ".r";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr ".s";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg";
	setAttr ".o" -type "double3" 0 0.001 0 ;
	setAttr ".rst" -type "double3" 0 0.001 0 ;
	setAttr -k on ".w0";
lockNode -l 1 -lu 1;
createNode ikHandle -n "ClavicleJoint__instance_2:hook_root_joint_ikHandle" -p "ClavicleJoint__instance_2:hook_grp";
	setAttr ".v" no;
	setAttr ".t";
	setAttr ".rp";
	setAttr ".rpt";
	setAttr ".pv";
	setAttr ".roc" yes;
lockNode -l 1 -lu 1;
createNode poleVectorConstraint -n "ClavicleJoint__instance_2:hook_root_joint_ikHandle_poleVectorConstraint1" 
		-p "ClavicleJoint__instance_2:hook_root_joint_ikHandle";
	addAttr -ci true -k true -sn "w0" -ln "hook_root_joint_ikHandle_poleVectorLocatorW0" 
		-dv 1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr ".t";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr ".r";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr ".s";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg";
	setAttr ".rst" -type "double3" 0 1 0 ;
	setAttr -k on ".w0";
lockNode -l 1 -lu 1;
createNode pointConstraint -n "ClavicleJoint__instance_2:hook_root_joint_ikHandle_pointConstraint" 
		-p "ClavicleJoint__instance_2:hook_root_joint_ikHandle";
	addAttr -ci true -k true -sn "w0" -ln "hook_target_joint_endPosLocatorW0" -dv 1 
		-min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr ".t";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr ".r";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr ".s";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg";
	setAttr ".rst" -type "double3" 0 0.001 0 ;
	setAttr -k on ".w0";
lockNode -l 1 -lu 1;
createNode transform -n "ClavicleJoint__instance_2:hook_root_joint_rootPosLocator" 
		-p "ClavicleJoint__instance_2:hook_grp";
	setAttr ".v" no;
	setAttr ".t";
	setAttr ".rp";
	setAttr ".rpt";
lockNode -l 1 -lu 1;
createNode locator -n "ClavicleJoint__instance_2:hook_root_joint_rootPosLocatorShape" 
		-p "ClavicleJoint__instance_2:hook_root_joint_rootPosLocator";
	setAttr -k off ".v";
lockNode -l 1 -lu 1;
createNode pointConstraint -n "ClavicleJoint__instance_2:hook_root_joint_rootPosLocator_pointConstraint" 
		-p "ClavicleJoint__instance_2:hook_root_joint_rootPosLocator";
	addAttr -ci true -k true -sn "w0" -ln "hook_root_jointW0" -dv 1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr ".t";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr ".r";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr ".s";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg";
	setAttr -k on ".w0";
lockNode -l 1 -lu 1;
createNode transform -n "ClavicleJoint__instance_2:hook_target_joint_endPosLocator" 
		-p "ClavicleJoint__instance_2:hook_grp";
	setAttr ".v" no;
	setAttr ".t";
	setAttr ".rp";
	setAttr ".rpt";
lockNode -l 1 -lu 1;
createNode locator -n "ClavicleJoint__instance_2:hook_target_joint_endPosLocatorShape" 
		-p "ClavicleJoint__instance_2:hook_target_joint_endPosLocator";
	setAttr -k off ".v";
lockNode -l 1 -lu 1;
createNode pointConstraint -n "ClavicleJoint__instance_2:hook_pointConstraint" -p
		 "ClavicleJoint__instance_2:hook_target_joint_endPosLocator";
	addAttr -ci true -k true -sn "w0" -ln "unhookedTargetW0" -dv 1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr ".t";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr ".r";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr ".s";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg";
	setAttr ".rst" -type "double3" 0 0.001 0 ;
	setAttr -k on ".w0";
lockNode -l 1 -lu 1;
createNode transform -n "ClavicleJoint__instance_2:hook_root_joint_ikHandle_poleVectorLocator" 
		-p "ClavicleJoint__instance_2:hook_grp";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 1 0 ;
	setAttr ".t";
	setAttr ".rp";
	setAttr ".rpt";
lockNode -l 1 -lu 1;
createNode locator -n "ClavicleJoint__instance_2:hook_root_joint_ikHandle_poleVectorLocatorShape" 
		-p "ClavicleJoint__instance_2:hook_root_joint_ikHandle_poleVectorLocator";
	setAttr -k off ".v";
lockNode -l 1 -lu 1;
createNode transform -n "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp" 
		-p "ClavicleJoint__instance_2:hook_grp";
	setAttr ".t";
	setAttr ".r";
	setAttr ".ro";
	setAttr ".s";
	setAttr ".rp";
	setAttr ".rpt";
lockNode -l 1 -lu 1;
createNode transform -n "ClavicleJoint__instance_2:hook_root_joint_hook_representation" 
		-p "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp";
lockNode -l 1 -lu 1;
createNode nurbsSurface -n "ClavicleJoint__instance_2:hook_root_joint_hook_representationShape" 
		-p "ClavicleJoint__instance_2:hook_root_joint_hook_representation";
	addAttr -ci true -sn "mso" -ln "miShadingSamplesOverride" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "msh" -ln "miShadingSamples" -min 0 -smx 8 -at "float";
	addAttr -ci true -sn "mdo" -ln "miMaxDisplaceOverride" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "mmd" -ln "miMaxDisplace" -min 0 -smx 1 -at "float";
	setAttr -k off ".v";
	setAttr ".iog";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		6 0 0 0 10 10 10
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		44
		0 -0.15672232497824501 -0.15672232497824506
		0 -0.22163883751087782 -3.5945998741709007e-017
		0 -0.15672232497824509 0.15672232497824481
		0 -2.862699950697759e-016 0.22163883751087754
		0 0.15672232497824459 0.15672232497824484
		0 0.22163883751087743 5.5517673144427339e-018
		0 0.15672232497824468 -0.15672232497824484
		0 -1.030019529394196e-016 -0.22163883751087765
		0 -0.15672232497824501 -0.15672232497824506
		0 -0.22163883751087782 -3.5945998741709007e-017
		0 -0.15672232497824509 0.15672232497824481
		0.33333333333333337 -0.15672232497824487 -0.15672232497824504
		0.33333333333333337 -0.22163883751087768 4.8755612298694312e-018
		0.33333333333333337 -0.15672232497824495 0.15672232497824484
		0.33333333333333331 -1.3824025845308839e-016 0.22163883751087757
		0.33333333333333326 0.15672232497824473 0.15672232497824487
		0.33333333333333326 0.22163883751087757 4.6373327286021172e-017
		0.33333333333333326 0.15672232497824481 -0.15672232497824481
		0.33333333333333331 4.502778367726793e-017 -0.22163883751087762
		0.33333333333333337 -0.15672232497824487 -0.15672232497824504
		0.33333333333333337 -0.22163883751087768 4.8755612298694312e-018
		0.33333333333333337 -0.15672232497824495 0.15672232497824484
		0.66666666666666674 -0.1567223249782447 -0.15672232497824498
		0.66666666666666674 -0.22163883751087751 4.5697121201447876e-017
		0.66666666666666674 -0.15672232497824479 0.1567223249782449
		0.66666666666666674 9.7894781635991762e-018 0.22163883751087762
		0.66666666666666663 0.1567223249782449 0.15672232497824493
		0.66666666666666663 0.22163883751087773 8.719488725759961e-017
		0.66666666666666663 0.15672232497824498 -0.15672232497824476
		0.66666666666666674 1.9305752029395549e-016 -0.22163883751087757
		0.66666666666666674 -0.1567223249782447 -0.15672232497824498
		0.66666666666666674 -0.22163883751087751 4.5697121201447876e-017
		0.66666666666666674 -0.15672232497824479 0.1567223249782449
		1 -0.15672232497824456 -0.15672232497824495
		1 -0.22163883751087737 8.651868117302632e-017
		1 -0.15672232497824465 0.15672232497824493
		1 1.5781921478028672e-016 0.22163883751087765
		1 0.15672232497824504 0.15672232497824495
		1 0.22163883751087787 1.2801644722917804e-016
		1 0.15672232497824512 -0.15672232497824473
		1 3.4108725691064299e-016 -0.22163883751087754
		1 -0.15672232497824456 -0.15672232497824495
		1 -0.22163883751087737 8.651868117302632e-017
		1 -0.15672232497824465 0.15672232497824493
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
lockNode -l 1 -lu 1;
createNode parentConstraint -n "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp_parentConstraint1" 
		-p "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp";
	addAttr -ci true -k true -sn "w0" -ln "hook_root_jointW0" -dv 1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr ".t";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr ".r";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr ".s";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg";
	setAttr ".lr" -type "double3" 0 0 89.999999999999986 ;
	setAttr ".rsrr" -type "double3" 0 0 89.999999999999986 ;
	setAttr -k on ".w0";
lockNode -l 1 -lu 1;
createNode scaleConstraint -n "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp_scaleConstraint1" 
		-p "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp";
	addAttr -ci true -k true -sn "w0" -ln "module_transformW0" -dv 1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr ".t";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr ".r";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr ".s";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg";
	setAttr -k on ".w0";
lockNode -l 1 -lu 1;
createNode transform -n "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocator_parentConstraintGroup" 
		-p "ClavicleJoint__instance_2:module_grp";
	setAttr ".t";
	setAttr ".r";
	setAttr ".ro";
	setAttr ".rp";
	setAttr ".rpt";
lockNode -l 1 -lu 1;
createNode transform -n "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocator" 
		-p "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocator_parentConstraintGroup";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 -0.5 0 ;
	setAttr ".t";
	setAttr ".rp";
	setAttr ".rpt";
lockNode -l 1 -lu 1;
createNode locator -n "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocatorShape" 
		-p "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocator";
	setAttr -k off ".v";
lockNode -l 1 -lu 1;
createNode parentConstraint -n "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocator_parentConstraintGroup_parentConstraint1" 
		-p "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocator_parentConstraintGroup";
	addAttr -ci true -k true -sn "w0" -ln "clav_1_joint_translation_controlW0" -dv 
		1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr ".t";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr ".r";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr ".s";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr ".tg";
	setAttr -k on ".w0";
lockNode -l 1 -lu 1;
createNode transform -n "ClavicleJoint__instance_2:module_transform";
	addAttr -ci true -h true -sn "aal" -ln "attributeAliasList" -dt "attributeAlias";
	setAttr ".t" -type "double3" 0 1.1549921062360939 0 ;
	setAttr ".s";
	setAttr ".aal" -type "attributeAlias" {"globalScale","scaleY"} ;
lockNode -l 1 -lu 1;
createNode mesh -n "ClavicleJoint__instance_2:module_transformShape" -p "ClavicleJoint__instance_2:module_transform";
	setAttr -k off ".v";
	setAttr ".iog";
	setAttr ".ovs" no;
	setAttr ".ove" yes;
	setAttr ".ovc" 4;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 26 ".uvst[0].uvsp[0:25]" -type "float2" 0.375 0 0.625 0 
		0.375 0.25 0.625 0.25 0.375 0.5 0.625 0.5 0.375 0.75 0.625 0.75 0.375 1 0.625 1 0.875 
		0 0.875 0.25 0.125 0 0.125 0.25 0.375 0 0.625 0 0.625 0.25 0.375 0.25 0.375 0 0.625 
		0 0.625 0.25 0.375 0.25 0.375 0 0.625 0 0.625 0.25 0.375 0.25;
	setAttr ".uvst";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".o";
	setAttr ".bnr" 0;
	setAttr -s 20 ".vt[0:19]"  -1 -1 1 1 -1 1 -1 1 1 1 1 1 -1 1 -1 1 1 
		-1 -1 -1 -1 1 -1 -1 -4.3673398e-007 -1.4887053 0 4.3673398e-007 -1.4887053 0 -4.3673398e-007 
		1.4887053 0 4.3673398e-007 1.4887053 0 1.4887053 -4.3673398e-007 0 1.4887053 4.3673398e-007 
		0 -1.4887053 -4.3673398e-007 0 -1.4887053 4.3673398e-007 0 3.3055887e-016 -4.3673398e-007 
		-1.4887053 3.3055905e-016 4.3673398e-007 -1.4887053 -3.3055905e-016 -4.3673398e-007 
		1.4887053 -3.3055887e-016 4.3673398e-007 1.4887053;
	setAttr -s 24 ".ed[0:23]"  0 1 0 2 3 0 
		4 5 0 6 7 0 0 2 0 1 3 0 
		2 4 0 3 5 0 4 6 0 5 7 0 
		6 0 0 7 1 0 8 9 0 10 11 0 
		8 10 0 9 11 0 12 13 0 14 15 0 
		12 14 0 13 15 0 16 17 0 18 19 0 
		16 18 0 17 19 0;
	setAttr -s 9 ".fc[0:8]" -type "polyFaces" 
		f 4 0 5 -2 -5 
		mu 0 4 0 1 3 2 
		f 4 1 7 -3 -7 
		mu 0 4 2 3 5 4 
		f 4 2 9 -4 -9 
		mu 0 4 4 5 7 6 
		f 4 3 11 -1 -11 
		mu 0 4 6 7 9 8 
		f 4 -12 -10 -8 -6 
		mu 0 4 1 10 11 3 
		f 4 10 4 6 8 
		mu 0 4 12 0 2 13 
		f 4 12 15 -14 -15 
		mu 0 4 14 15 16 17 
		f 4 16 19 -18 -19 
		mu 0 4 18 19 20 21 
		f 4 20 23 -22 -23 
		mu 0 4 22 23 24 25 ;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".atm" no;
lockNode -l 1 -lu 1;
createNode transform -n "ClavicleJoint__instance_2:clav_1_joint_translation_control" 
		-p "ClavicleJoint__instance_2:module_transform";
	setAttr -l on -k off ".v";
	setAttr ".r";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr ".ro";
	setAttr ".s";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".rp";
	setAttr ".rpt";
lockNode -l 1 -lu 1;
createNode nurbsSurface -n "ClavicleJoint__instance_2:clav_1_joint_translation_controlShape" 
		-p "ClavicleJoint__instance_2:clav_1_joint_translation_control";
	setAttr -k off ".v";
	setAttr ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		9.596474681976929e-017 -1 -2.5316183359690662e-016
		9.596474681976929e-017 -1 -2.5316183359690662e-016
		9.596474681976929e-017 -1 -2.5316183359690662e-016
		9.596474681976929e-017 -1 -2.5316183359690662e-016
		9.596474681976929e-017 -1 -2.5316183359690662e-016
		9.596474681976929e-017 -1 -2.5316183359690662e-016
		9.596474681976929e-017 -1 -2.5316183359690662e-016
		9.596474681976929e-017 -1 -2.5316183359690662e-016
		9.596474681976929e-017 -1 -2.5316183359690662e-016
		9.596474681976929e-017 -1 -2.5316183359690662e-016
		9.596474681976929e-017 -1 -2.5316183359690662e-016
		0.19991679083637254 -1 -0.19991679083637298
		0.2827250369469036 -1 -6.2210285873682227e-017
		0.1999167908363727 -1 0.19991679083637259
		1.151601345627845e-016 -1 0.28272503694690354
		-0.19991679083637259 -1 0.19991679083637273
		-0.28272503694690365 -1 5.7191723447539755e-017
		-0.19991679083637276 -1 -0.19991679083637259
		-1.8508566094318079e-016 -1 -0.28272503694690365
		0.19991679083637254 -1 -0.19991679083637298
		0.2827250369469036 -1 -6.2210285873682227e-017
		0.1999167908363727 -1 0.19991679083637259
		0.61642997969058899 -0.78361162489122427 -0.61642997969058999
		0.87176363753180319 -0.78361162489122427 1.0506190143399388e-016
		0.61642997969058932 -0.78361162489122427 0.61642997969058932
		1.9902882483877521e-016 -0.78361162489122427 0.87176363753180319
		-0.61642997969058921 -0.78361162489122427 0.61642997969058955
		-0.8717636375318033 -0.78361162489122427 1.6111055650702835e-016
		-0.61642997969058944 -0.78361162489122427 -0.61642997969058899
		-4.1463948278396632e-016 -0.78361162489122427 -0.87176363753180319
		0.61642997969058899 -0.78361162489122427 -0.61642997969058999
		0.87176363753180319 -0.78361162489122427 1.0506190143399388e-016
		0.61642997969058932 -0.78361162489122427 0.61642997969058932
		0.8672024474915413 6.5353909630129576e-017 -0.86720244749154252
		1.2264094625656803 1.2253074553466144e-017 2.901104977298788e-016
		0.86720244749154163 -4.0847760523197208e-017 0.86720244749154185
		2.051909376318187e-016 -6.284284658528814e-017 1.2264094625656803
		-0.86720244749154163 -4.0847760523197208e-017 0.86720244749154185
		-1.2264094625656805 1.2253074553466149e-017 2.1934926354574312e-016
		-0.86720244749154174 6.5353909630129502e-017 -0.8672024474915413
		-5.0851507246572639e-016 8.7348995692220465e-017 -1.2264094625656803
		0.8672024474915413 6.5353909630129576e-017 -0.86720244749154252
		1.2264094625656803 1.2253074553466144e-017 2.901104977298788e-016
		0.86720244749154163 -4.0847760523197208e-017 0.86720244749154185
		0.61642997969058932 0.78361162489122449 -0.61642997969058999
		0.87176363753180341 0.78361162489122449 3.0737422288956035e-016
		0.61642997969058944 0.78361162489122449 0.61642997969058966
		9.2681250202978354e-017 0.78361162489122449 0.87176363753180341
		-0.61642997969058944 0.78361162489122449 0.61642997969058966
		-0.87176363753180353 0.78361162489122449 1.507277286910009e-016
		-0.61642997969058955 0.78361162489122449 -0.61642997969058932
		-3.0829190814816951e-016 0.78361162489122449 -0.87176363753180341
		0.61642997969058932 0.78361162489122449 -0.61642997969058999
		0.87176363753180341 0.78361162489122449 3.0737422288956035e-016
		0.61642997969058944 0.78361162489122449 0.61642997969058966
		0.19991679083637276 0.99999999999999989 -0.19991679083637284
		0.28272503694690371 0.99999999999999989 1.9596904050327137e-016
		0.1999167908363727 0.99999999999999989 0.19991679083637293
		-2.0554511899433756e-017 0.99999999999999989 0.28272503694690376
		-0.19991679083637282 0.99999999999999989 0.19991679083637282
		-0.28272503694690376 0.99999999999999989 4.3941756900056795e-017
		-0.19991679083637273 0.99999999999999989 -0.1999167908363727
		-4.9371014480962574e-017 0.99999999999999989 -0.28272503694690365
		0.19991679083637276 0.99999999999999989 -0.19991679083637284
		0.28272503694690371 0.99999999999999989 1.9596904050327137e-016
		0.1999167908363727 0.99999999999999989 0.19991679083637293
		1.739967336636337e-016 1 -1.6799646886496759e-017
		1.739967336636337e-016 1 -1.6799646886496759e-017
		1.739967336636337e-016 1 -1.6799646886496759e-017
		1.739967336636337e-016 1 -1.6799646886496759e-017
		1.739967336636337e-016 1 -1.6799646886496759e-017
		1.739967336636337e-016 1 -1.6799646886496759e-017
		1.739967336636337e-016 1 -1.6799646886496759e-017
		1.739967336636337e-016 1 -1.6799646886496759e-017
		1.739967336636337e-016 1 -1.6799646886496759e-017
		1.739967336636337e-016 1 -1.6799646886496759e-017
		1.739967336636337e-016 1 -1.6799646886496759e-017
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
lockNode -l 1 -lu 1;
createNode transform -n "ClavicleJoint__instance_2:clav_2_joint_translation_control" 
		-p "ClavicleJoint__instance_2:module_transform";
	setAttr -l on -k off ".v";
	setAttr ".t" -type "double3" 4 0 0 ;
	setAttr ".r";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr ".s";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".rp";
	setAttr ".rpt";
lockNode -l 1 -lu 1;
createNode nurbsSurface -n "ClavicleJoint__instance_2:clav_2_joint_translation_controlShape" 
		-p "ClavicleJoint__instance_2:clav_2_joint_translation_control";
	setAttr -k off ".v";
	setAttr ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".dvu" 0;
	setAttr ".dvv" 0;
	setAttr ".cpr" 4;
	setAttr ".cps" 4;
	setAttr ".cc" -type "nurbsSurface" 
		3 3 0 2 no 
		9 0 0 0 1 2 3 4 4 4
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		
		77
		9.596474681976929e-017 -1 -2.5316183359690662e-016
		9.596474681976929e-017 -1 -2.5316183359690662e-016
		9.596474681976929e-017 -1 -2.5316183359690662e-016
		9.596474681976929e-017 -1 -2.5316183359690662e-016
		9.596474681976929e-017 -1 -2.5316183359690662e-016
		9.596474681976929e-017 -1 -2.5316183359690662e-016
		9.596474681976929e-017 -1 -2.5316183359690662e-016
		9.596474681976929e-017 -1 -2.5316183359690662e-016
		9.596474681976929e-017 -1 -2.5316183359690662e-016
		9.596474681976929e-017 -1 -2.5316183359690662e-016
		9.596474681976929e-017 -1 -2.5316183359690662e-016
		0.19991679083637254 -1 -0.19991679083637298
		0.2827250369469036 -1 -6.2210285873682227e-017
		0.1999167908363727 -1 0.19991679083637259
		1.151601345627845e-016 -1 0.28272503694690354
		-0.19991679083637259 -1 0.19991679083637273
		-0.28272503694690365 -1 5.7191723447539755e-017
		-0.19991679083637276 -1 -0.19991679083637259
		-1.8508566094318079e-016 -1 -0.28272503694690365
		0.19991679083637254 -1 -0.19991679083637298
		0.2827250369469036 -1 -6.2210285873682227e-017
		0.1999167908363727 -1 0.19991679083637259
		0.61642997969058899 -0.78361162489122427 -0.61642997969058999
		0.87176363753180319 -0.78361162489122427 1.0506190143399388e-016
		0.61642997969058932 -0.78361162489122427 0.61642997969058932
		1.9902882483877521e-016 -0.78361162489122427 0.87176363753180319
		-0.61642997969058921 -0.78361162489122427 0.61642997969058955
		-0.8717636375318033 -0.78361162489122427 1.6111055650702835e-016
		-0.61642997969058944 -0.78361162489122427 -0.61642997969058899
		-4.1463948278396632e-016 -0.78361162489122427 -0.87176363753180319
		0.61642997969058899 -0.78361162489122427 -0.61642997969058999
		0.87176363753180319 -0.78361162489122427 1.0506190143399388e-016
		0.61642997969058932 -0.78361162489122427 0.61642997969058932
		0.8672024474915413 6.5353909630129576e-017 -0.86720244749154252
		1.2264094625656803 1.2253074553466144e-017 2.901104977298788e-016
		0.86720244749154163 -4.0847760523197208e-017 0.86720244749154185
		2.051909376318187e-016 -6.284284658528814e-017 1.2264094625656803
		-0.86720244749154163 -4.0847760523197208e-017 0.86720244749154185
		-1.2264094625656805 1.2253074553466149e-017 2.1934926354574312e-016
		-0.86720244749154174 6.5353909630129502e-017 -0.8672024474915413
		-5.0851507246572639e-016 8.7348995692220465e-017 -1.2264094625656803
		0.8672024474915413 6.5353909630129576e-017 -0.86720244749154252
		1.2264094625656803 1.2253074553466144e-017 2.901104977298788e-016
		0.86720244749154163 -4.0847760523197208e-017 0.86720244749154185
		0.61642997969058932 0.78361162489122449 -0.61642997969058999
		0.87176363753180341 0.78361162489122449 3.0737422288956035e-016
		0.61642997969058944 0.78361162489122449 0.61642997969058966
		9.2681250202978354e-017 0.78361162489122449 0.87176363753180341
		-0.61642997969058944 0.78361162489122449 0.61642997969058966
		-0.87176363753180353 0.78361162489122449 1.507277286910009e-016
		-0.61642997969058955 0.78361162489122449 -0.61642997969058932
		-3.0829190814816951e-016 0.78361162489122449 -0.87176363753180341
		0.61642997969058932 0.78361162489122449 -0.61642997969058999
		0.87176363753180341 0.78361162489122449 3.0737422288956035e-016
		0.61642997969058944 0.78361162489122449 0.61642997969058966
		0.19991679083637276 0.99999999999999989 -0.19991679083637284
		0.28272503694690371 0.99999999999999989 1.9596904050327137e-016
		0.1999167908363727 0.99999999999999989 0.19991679083637293
		-2.0554511899433756e-017 0.99999999999999989 0.28272503694690376
		-0.19991679083637282 0.99999999999999989 0.19991679083637282
		-0.28272503694690376 0.99999999999999989 4.3941756900056795e-017
		-0.19991679083637273 0.99999999999999989 -0.1999167908363727
		-4.9371014480962574e-017 0.99999999999999989 -0.28272503694690365
		0.19991679083637276 0.99999999999999989 -0.19991679083637284
		0.28272503694690371 0.99999999999999989 1.9596904050327137e-016
		0.1999167908363727 0.99999999999999989 0.19991679083637293
		1.739967336636337e-016 1 -1.6799646886496759e-017
		1.739967336636337e-016 1 -1.6799646886496759e-017
		1.739967336636337e-016 1 -1.6799646886496759e-017
		1.739967336636337e-016 1 -1.6799646886496759e-017
		1.739967336636337e-016 1 -1.6799646886496759e-017
		1.739967336636337e-016 1 -1.6799646886496759e-017
		1.739967336636337e-016 1 -1.6799646886496759e-017
		1.739967336636337e-016 1 -1.6799646886496759e-017
		1.739967336636337e-016 1 -1.6799646886496759e-017
		1.739967336636337e-016 1 -1.6799646886496759e-017
		1.739967336636337e-016 1 -1.6799646886496759e-017
		
		;
	setAttr ".nufa" 4.5;
	setAttr ".nvfa" 4.5;
lockNode -l 1 -lu 1;
createNode container -n "ClavicleJoint__instance_2:module_container";
	addAttr -ci true -h true -sn "aal" -ln "attributeAliasList" -dt "attributeAlias";
	setAttr ".isc" yes;
	setAttr -s 28 ".boc";
	setAttr -s 9 ".ish[19:27]" yes yes yes yes yes yes yes yes yes;
	setAttr ".ctor" -type "string" "rgriffin";
	setAttr ".cdat" -type "string" "2011/11/18 14:05:09";
	setAttr ".aal" -type "attributeAlias" {"clav_1_joint_R","borderConnections[0]","moduleTransform_T"
		,"borderConnections[10]","moduleTransform_TX","borderConnections[11]","moduleTransform_TY"
		,"borderConnections[12]","moduleTransform_TZ","borderConnections[13]","moduleTransform_R"
		,"borderConnections[14]","moduleTransform_RX","borderConnections[15]","moduleTransform_RY"
		,"borderConnections[16]","moduleTransform_RZ","borderConnections[17]","moduleTransform_globalScale"
		,"borderConnections[18]","clav_1_joint_T","borderConnections[19]","clav_1_joint_RX"
		,"borderConnections[1]","clav_1_joint_TX","borderConnections[20]","clav_1_joint_TY"
		,"borderConnections[21]","clav_1_joint_TZ","borderConnections[22]","clav_2_joint_T"
		,"borderConnections[23]","clav_2_joint_TX","borderConnections[24]","clav_2_joint_TY"
		,"borderConnections[25]","clav_2_joint_TZ","borderConnections[26]","clav_1_joint_orientation"
		,"borderConnections[27]","clav_1_joint_RY","borderConnections[2]","clav_1_joint_RZ"
		,"borderConnections[3]","clav_1_joint_rotateOrder","borderConnections[4]","clav_2_joint_R"
		,"borderConnections[5]","clav_2_joint_RX","borderConnections[6]","clav_2_joint_RY"
		,"borderConnections[7]","clav_2_joint_RZ","borderConnections[8]","clav_2_joint_rotateOrder"
		,"borderConnections[9]"} ;
lockNode -l 1 -lu 1;
createNode blendColors -n "ClavicleJoint__instance_2:clav_1_joint_ikHandle_lockBlend";
	setAttr ".b" 1;
	setAttr ".c1";
	setAttr ".c2" -type "float3" 1 0 1 ;
lockNode -l 1 -lu 1;
createNode distanceBetween -n "ClavicleJoint__instance_2:distBetween_clav_1_joint_rootPosLocator_clav_2_joint_endPosLocator";
lockNode -l 1 -lu 1;
createNode hyperLayout -n "hyperLayout3";
	setAttr ".ihi" 0;
	setAttr -s 34 ".hyp";
createNode container -n "ClavicleJoint__instance_2:clav_1_joint_orientation_control_container";
	addAttr -ci true -h true -sn "aal" -ln "attributeAliasList" -dt "attributeAlias";
	setAttr ".ctor" -type "string" "Administrator";
	setAttr ".cdat" -type "string" "2009/07/28 18:25:27";
	setAttr ".aal" -type "attributeAlias" {"clav_1_joint_orientation","borderConnections[0]"
		} ;
lockNode -l 1 -lu 1;
createNode container -n "ClavicleJoint__instance_2:clav_2_joint_translation_control_container";
	addAttr -ci true -h true -sn "aal" -ln "attributeAliasList" -dt "attributeAlias";
	setAttr -s 4 ".boc";
	setAttr ".ctor" -type "string" "Administrator";
	setAttr ".cdat" -type "string" "2009/08/05 11:57:53";
	setAttr ".aal" -type "attributeAlias" {"clav_2_joint_T","borderConnections[0]","clav_2_joint_TX"
		,"borderConnections[1]","clav_2_joint_TY","borderConnections[2]","clav_2_joint_TZ"
		,"borderConnections[3]"} ;
lockNode -l 1 -lu 1;
createNode container -n "ClavicleJoint__instance_2:hook_container";
	addAttr -ci true -h true -sn "aal" -ln "attributeAliasList" -dt "attributeAlias";
	setAttr ".isc" yes;
	setAttr -s 8 ".boc";
	setAttr ".ctor" -type "string" "rgriffin";
	setAttr ".cdat" -type "string" "2011/11/18 14:05:10";
	setAttr ".aal" -type "attributeAlias" {"hook_root_joint_R","borderConnections[0]"
		,"hook_root_joint_RX","borderConnections[1]","hook_root_joint_RY","borderConnections[2]"
		,"hook_root_joint_RZ","borderConnections[3]","hook_target_joint_R","borderConnections[4]"
		,"hook_target_joint_RX","borderConnections[5]","hook_target_joint_RY","borderConnections[6]"
		,"hook_target_joint_RZ","borderConnections[7]"} ;
lockNode -l 1 -lu 1;
createNode container -n "ClavicleJoint__instance_2:clav_1_joint_translation_control_container";
	addAttr -ci true -h true -sn "aal" -ln "attributeAliasList" -dt "attributeAlias";
	setAttr -s 4 ".boc";
	setAttr ".ctor" -type "string" "Administrator";
	setAttr ".cdat" -type "string" "2009/08/05 11:57:53";
	setAttr ".aal" -type "attributeAlias" {"clav_1_joint_T","borderConnections[0]","clav_1_joint_TX"
		,"borderConnections[1]","clav_1_joint_TY","borderConnections[2]","clav_1_joint_TZ"
		,"borderConnections[3]"} ;
lockNode -l 1 -lu 1;
createNode multiplyDivide -n "ClavicleJoint__instance_2:clav_2_joint_scaleMultiply";
	setAttr ".i1" -type "float3" 4 0 0 ;
	setAttr ".i2";
lockNode -l 1 -lu 1;
createNode multiplyDivide -n "ClavicleJoint__instance_2:clav_1_joint_ikHandle_scaleFactor";
	setAttr ".op" 2;
	setAttr ".i1";
	setAttr ".i2" -type "float3" 4 1 1 ;
lockNode -l 1 -lu 1;
createNode materialInfo -n "translation_control01_materialInfo3";
createNode shadingEngine -n "ClavicleJoint__instance_2:clav_1_joint_m_translation_control_SG";
	setAttr ".ro" yes;
lockNode -l 1 -lu 1;
createNode lambert -n "ClavicleJoint__instance_2:clav_1_joint_m_translation_control";
	setAttr ".c" -type "float3" 0.75800002 0.050785981 0.1018231 ;
lockNode -l 1 -lu 1;
createNode materialInfo -n "translation_control01_materialInfo4";
createNode shadingEngine -n "ClavicleJoint__instance_2:clav_2_joint_m_translation_control_SG";
	setAttr ".ro" yes;
lockNode -l 1 -lu 1;
createNode lambert -n "ClavicleJoint__instance_2:clav_2_joint_m_translation_control";
	setAttr ".c" -type "float3" 0.75800002 0.050785981 0.1018231 ;
lockNode -l 1 -lu 1;
createNode hyperLayout -n "orientation_control_hyperLayout1";
	setAttr ".ihi" 0;
	setAttr -s 9 ".hyp";
	setAttr ".hyp[0].x" 286;
	setAttr ".hyp[0].y" 613;
	setAttr ".hyp[0].isf" yes;
	setAttr ".hyp[1].x" 286;
	setAttr ".hyp[1].y" 93;
	setAttr ".hyp[1].isf" yes;
	setAttr ".hyp[3].x" 497;
	setAttr ".hyp[3].y" 487;
	setAttr ".hyp[3].isf" yes;
	setAttr ".hyp[4].x" 474;
	setAttr ".hyp[4].y" 223;
	setAttr ".hyp[4].isf" yes;
	setAttr ".hyp[5].x" 148;
	setAttr ".hyp[5].y" 353;
	setAttr ".hyp[5].isf" yes;
	setAttr ".hyp[6].x" 148;
	setAttr ".hyp[6].y" 353;
	setAttr ".hyp[6].isf" yes;
	setAttr ".anf" yes;
createNode shadingEngine -n "ClavicleJoint__instance_2:clav_1_joint_m_zAxisBlockSG";
	setAttr ".ihi" 0;
	setAttr ".mwc";
	setAttr ".ro" yes;
lockNode -l 1 -lu 1;
createNode shadingEngine -n "ClavicleJoint__instance_2:clav_1_joint_m_yAxisBlockSG";
	setAttr ".ihi" 0;
	setAttr ".mwc";
	setAttr ".ro" yes;
lockNode -l 1 -lu 1;
createNode lambert -n "ClavicleJoint__instance_2:clav_1_joint_m_yAxisBlock";
	setAttr ".c" -type "float3" 0.43241283 1 0.19700003 ;
lockNode -l 1 -lu 1;
createNode lambert -n "ClavicleJoint__instance_2:clav_1_joint_m_zAxisBlock";
	setAttr ".c" -type "float3" 0.097775996 0.38538396 0.87300003 ;
lockNode -l 1 -lu 1;
createNode materialInfo -n "orientation_control_materialInfo1";
createNode materialInfo -n "materialInfo2";
createNode groupId -n "groupId19";
	setAttr ".ihi" 0;
createNode groupId -n "groupId20";
	setAttr ".ihi" 0;
createNode groupId -n "groupId18";
	setAttr ".ihi" 0;
createNode hyperLayout -n "translation_control01_hyperLayout5";
	setAttr ".ihi" 0;
	setAttr -s 4 ".hyp";
	setAttr ".hyp[0].x" 71;
	setAttr ".hyp[0].y" 93;
	setAttr ".hyp[0].isf" yes;
	setAttr ".hyp[1].x" 409;
	setAttr ".hyp[1].y" 309;
	setAttr ".hyp[1].isf" yes;
	setAttr ".hyp[2].x" 240;
	setAttr ".hyp[2].y" 309;
	setAttr ".hyp[2].isf" yes;
	setAttr ".hyp[3].x" 71;
	setAttr ".hyp[3].y" 309;
	setAttr ".hyp[3].isf" yes;
	setAttr ".anf" yes;
createNode blendColors -n "ClavicleJoint__instance_2:hook_root_joint_ikHandle_lockBlend";
	setAttr ".b" 1;
	setAttr ".c1";
	setAttr ".c2" -type "float3" 1 0 1 ;
lockNode -l 1 -lu 1;
createNode distanceBetween -n "ClavicleJoint__instance_2:distBetween_hook_root_joint_rootPosLocator_hook_target_joint_endPosLocator";
lockNode -l 1 -lu 1;
createNode hyperLayout -n "hyperLayout4";
	setAttr ".ihi" 0;
	setAttr -s 24 ".hyp";
createNode container -n "ClavicleJoint__instance_2:hook_root_joint_hook_representation_container";
	setAttr ".ctor" -type "string" "Administrator";
	setAttr ".cdat" -type "string" "2009/07/28 18:18:37";
lockNode -l 1 -lu 1;
createNode multiplyDivide -n "ClavicleJoint__instance_2:hook_target_joint_scaleMultiply";
	setAttr ".i1" -type "float3" 0.001 0 0 ;
	setAttr ".i2";
lockNode -l 1 -lu 1;
createNode multiplyDivide -n "ClavicleJoint__instance_2:hook_root_joint_ikHandle_scaleFactor";
	setAttr ".op" 2;
	setAttr ".i1";
	setAttr ".i2" -type "float3" 0.001 1 1 ;
lockNode -l 1 -lu 1;
createNode hyperLayout -n "hook_representation_hyperLayout2";
	setAttr ".ihi" 0;
	setAttr -s 7 ".hyp";
	setAttr ".hyp[1].x" 71;
	setAttr ".hyp[1].y" 93;
	setAttr ".hyp[1].isf" yes;
	setAttr ".hyp[3].x" 259;
	setAttr ".hyp[3].y" 93;
	setAttr ".hyp[3].isf" yes;
	setAttr ".anf" yes;
createNode shadingEngine -n "ClavicleJoint__instance_2:hook_root_joint_m_hookRepresentation_SG";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
lockNode -l 1 -lu 1;
createNode lambert -n "ClavicleJoint__instance_2:hook_root_joint_m_hookRepresentation";
	setAttr ".c" -type "float3" 0.595788 0.69519699 0.75800002 ;
lockNode -l 1 -lu 1;
createNode materialInfo -n "hook_representation_materialInfo2";
createNode ikRPsolver -n "ikRPsolver";
createNode hyperLayout -n "translation_control01_hyperLayout4";
	setAttr ".ihi" 0;
	setAttr -s 4 ".hyp";
	setAttr ".hyp[0].x" 71;
	setAttr ".hyp[0].y" 93;
	setAttr ".hyp[0].isf" yes;
	setAttr ".hyp[1].x" 409;
	setAttr ".hyp[1].y" 309;
	setAttr ".hyp[1].isf" yes;
	setAttr ".hyp[2].x" 240;
	setAttr ".hyp[2].y" 309;
	setAttr ".hyp[2].isf" yes;
	setAttr ".hyp[3].x" 71;
	setAttr ".hyp[3].y" 309;
	setAttr ".hyp[3].isf" yes;
	setAttr ".anf" yes;
createNode lightLinker -s -n "lightLinker1";
	setAttr -s 22 ".lnk";
	setAttr -s 22 ".slnk";
select -ne :time1;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".o" 1;
	setAttr ".unw" 1;
select -ne :renderPartition;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 14 ".st";
	setAttr -cb on ".an";
	setAttr -cb on ".pt";
select -ne :initialShadingGroup;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".dsm";
	setAttr -k on ".mwc";
	setAttr -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr -k on ".ro" yes;
	setAttr -cb on ".mimt";
	setAttr -cb on ".miop";
	setAttr -cb on ".mise";
	setAttr -cb on ".mism";
	setAttr -cb on ".mice";
	setAttr -av -cb on ".micc";
	setAttr -cb on ".mica";
	setAttr -cb on ".micw";
	setAttr -cb on ".mirw";
select -ne :initialParticleSE;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".mwc";
	setAttr -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr -k on ".ro" yes;
	setAttr -cb on ".mimt";
	setAttr -cb on ".miop";
	setAttr -cb on ".mise";
	setAttr -cb on ".mism";
	setAttr -cb on ".mice";
	setAttr -av -cb on ".micc";
	setAttr -cb on ".mica";
	setAttr -cb on ".micw";
	setAttr -cb on ".mirw";
select -ne :defaultShaderList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 14 ".s";
select -ne :postProcessList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".p";
select -ne :defaultRenderUtilityList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 26 ".u";
select -ne :renderGlobalsList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
select -ne :defaultLightSet;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -k on ".mwc";
	setAttr -k on ".an";
	setAttr -k on ".il";
	setAttr -k on ".vo";
	setAttr -k on ".eo";
	setAttr -k on ".fo";
	setAttr -k on ".epo";
	setAttr -k on ".ro" yes;
select -ne :defaultObjectSet;
	setAttr ".ro" yes;
select -ne :hardwareRenderGlobals;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
	setAttr -k off ".fbfm";
	setAttr -k off -cb on ".ehql";
	setAttr -k off -cb on ".eams";
	setAttr -k off -cb on ".eeaa";
	setAttr -k off -cb on ".engm";
	setAttr -k off -cb on ".mes";
	setAttr -k off -cb on ".emb";
	setAttr -av -k off -cb on ".mbbf";
	setAttr -k off -cb on ".mbs";
	setAttr -k off -cb on ".trm";
	setAttr -k off -cb on ".tshc";
	setAttr -k off ".enpt";
	setAttr -k off -cb on ".clmt";
	setAttr -k off -cb on ".tcov";
	setAttr -k off -cb on ".lith";
	setAttr -k off -cb on ".sobc";
	setAttr -k off -cb on ".cuth";
	setAttr -k off -cb on ".hgcd";
	setAttr -k off -cb on ".hgci";
	setAttr -k off -cb on ".mgcs";
	setAttr -k off -cb on ".twa";
	setAttr -k off -cb on ".twz";
	setAttr -k on ".hwcc";
	setAttr -k on ".hwdp";
	setAttr -k on ".hwql";
	setAttr -k on ".hwfr";
select -ne :defaultHardwareRenderGlobals;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".rp";
	setAttr -k on ".cai";
	setAttr -k on ".coi";
	setAttr -cb on ".bc";
	setAttr -av -k on ".bcb";
	setAttr -av -k on ".bcg";
	setAttr -av -k on ".bcr";
	setAttr -k on ".ei";
	setAttr -k on ".ex";
	setAttr -av -k on ".es";
	setAttr -av -k on ".ef";
	setAttr -av -k on ".bf";
	setAttr -k on ".fii";
	setAttr -av -k on ".sf";
	setAttr -k on ".gr";
	setAttr -k on ".li";
	setAttr -k on ".ls";
	setAttr -k on ".mb";
	setAttr -k on ".ti";
	setAttr -k on ".txt";
	setAttr -k on ".mpr";
	setAttr -k on ".wzd";
	setAttr -k on ".fn" -type "string" "im";
	setAttr -k on ".if";
	setAttr -k on ".res" -type "string" "ntsc_4d 646 485 1.333";
	setAttr -k on ".as";
	setAttr -k on ".ds";
	setAttr -k on ".lm";
	setAttr -k on ".fir";
	setAttr -k on ".aap";
	setAttr -k on ".gh";
	setAttr -cb on ".sd";
select -ne :ikSystem;
	setAttr -av ".gsn";
	setAttr -s 4 ".sol";
connectAttr "ClavicleJoint__instance_2:clav_1_joint_pointConstraint.ctx" "ClavicleJoint__instance_2:clav_1_joint.tx"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_pointConstraint.cty" "ClavicleJoint__instance_2:clav_1_joint.ty"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_pointConstraint.ctz" "ClavicleJoint__instance_2:clav_1_joint.tz"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint.s" "ClavicleJoint__instance_2:clav_2_joint.is"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_2_joint_scaleMultiply.ox" "ClavicleJoint__instance_2:clav_2_joint.tx"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint.pim" "ClavicleJoint__instance_2:clav_1_joint_pointConstraint.cpim"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint.rp" "ClavicleJoint__instance_2:clav_1_joint_pointConstraint.crp"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint.rpt" "ClavicleJoint__instance_2:clav_1_joint_pointConstraint.crt"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control.t" "ClavicleJoint__instance_2:clav_1_joint_pointConstraint.tg[0].tt"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control.rp" "ClavicleJoint__instance_2:clav_1_joint_pointConstraint.tg[0].trp"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control.rpt" "ClavicleJoint__instance_2:clav_1_joint_pointConstraint.tg[0].trt"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control.pm" "ClavicleJoint__instance_2:clav_1_joint_pointConstraint.tg[0].tpm"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_pointConstraint.w0" "ClavicleJoint__instance_2:clav_1_joint_pointConstraint.tg[0].tw"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_2_joint.tx" "ClavicleJoint__instance_2:clav_1_joint_ikEffector.tx"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_2_joint.ty" "ClavicleJoint__instance_2:clav_1_joint_ikEffector.ty"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_2_joint.tz" "ClavicleJoint__instance_2:clav_1_joint_ikEffector.tz"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint.msg" "ClavicleJoint__instance_2:clav_1_joint_ikHandle.hsj"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_ikEffector.hp" "ClavicleJoint__instance_2:clav_1_joint_ikHandle.hee"
		 -l on;
connectAttr "ikRPsolver.msg" "ClavicleJoint__instance_2:clav_1_joint_ikHandle.hsv"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_ikHandle_poleVectorConstraint1.ctx" "ClavicleJoint__instance_2:clav_1_joint_ikHandle.pvx"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_ikHandle_poleVectorConstraint1.cty" "ClavicleJoint__instance_2:clav_1_joint_ikHandle.pvy"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_ikHandle_poleVectorConstraint1.ctz" "ClavicleJoint__instance_2:clav_1_joint_ikHandle.pvz"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_ikHandle_pointConstraint.ctx" "ClavicleJoint__instance_2:clav_1_joint_ikHandle.tx"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_ikHandle_pointConstraint.cty" "ClavicleJoint__instance_2:clav_1_joint_ikHandle.ty"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_ikHandle_pointConstraint.ctz" "ClavicleJoint__instance_2:clav_1_joint_ikHandle.tz"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_ikHandle.pim" "ClavicleJoint__instance_2:clav_1_joint_ikHandle_poleVectorConstraint1.cpim"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint.pm" "ClavicleJoint__instance_2:clav_1_joint_ikHandle_poleVectorConstraint1.ps"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint.t" "ClavicleJoint__instance_2:clav_1_joint_ikHandle_poleVectorConstraint1.crp"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocator.t" "ClavicleJoint__instance_2:clav_1_joint_ikHandle_poleVectorConstraint1.tg[0].tt"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocator.rp" "ClavicleJoint__instance_2:clav_1_joint_ikHandle_poleVectorConstraint1.tg[0].trp"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocator.rpt" "ClavicleJoint__instance_2:clav_1_joint_ikHandle_poleVectorConstraint1.tg[0].trt"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocator.pm" "ClavicleJoint__instance_2:clav_1_joint_ikHandle_poleVectorConstraint1.tg[0].tpm"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_ikHandle_poleVectorConstraint1.w0" "ClavicleJoint__instance_2:clav_1_joint_ikHandle_poleVectorConstraint1.tg[0].tw"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_ikHandle.pim" "ClavicleJoint__instance_2:clav_1_joint_ikHandle_pointConstraint.cpim"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_ikHandle.rp" "ClavicleJoint__instance_2:clav_1_joint_ikHandle_pointConstraint.crp"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_ikHandle.rpt" "ClavicleJoint__instance_2:clav_1_joint_ikHandle_pointConstraint.crt"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_2_joint_endPosLocator.t" "ClavicleJoint__instance_2:clav_1_joint_ikHandle_pointConstraint.tg[0].tt"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_2_joint_endPosLocator.rp" "ClavicleJoint__instance_2:clav_1_joint_ikHandle_pointConstraint.tg[0].trp"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_2_joint_endPosLocator.rpt" "ClavicleJoint__instance_2:clav_1_joint_ikHandle_pointConstraint.tg[0].trt"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_2_joint_endPosLocator.pm" "ClavicleJoint__instance_2:clav_1_joint_ikHandle_pointConstraint.tg[0].tpm"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_ikHandle_pointConstraint.w0" "ClavicleJoint__instance_2:clav_1_joint_ikHandle_pointConstraint.tg[0].tw"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_rootPosLocator_pointConstraint.ctx" "ClavicleJoint__instance_2:clav_1_joint_rootPosLocator.tx"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_rootPosLocator_pointConstraint.cty" "ClavicleJoint__instance_2:clav_1_joint_rootPosLocator.ty"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_rootPosLocator_pointConstraint.ctz" "ClavicleJoint__instance_2:clav_1_joint_rootPosLocator.tz"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_rootPosLocator.pim" "ClavicleJoint__instance_2:clav_1_joint_rootPosLocator_pointConstraint.cpim"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_rootPosLocator.rp" "ClavicleJoint__instance_2:clav_1_joint_rootPosLocator_pointConstraint.crp"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_rootPosLocator.rpt" "ClavicleJoint__instance_2:clav_1_joint_rootPosLocator_pointConstraint.crt"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint.t" "ClavicleJoint__instance_2:clav_1_joint_rootPosLocator_pointConstraint.tg[0].tt"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint.rp" "ClavicleJoint__instance_2:clav_1_joint_rootPosLocator_pointConstraint.tg[0].trp"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint.rpt" "ClavicleJoint__instance_2:clav_1_joint_rootPosLocator_pointConstraint.tg[0].trt"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint.pm" "ClavicleJoint__instance_2:clav_1_joint_rootPosLocator_pointConstraint.tg[0].tpm"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_rootPosLocator_pointConstraint.w0" "ClavicleJoint__instance_2:clav_1_joint_rootPosLocator_pointConstraint.tg[0].tw"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_2_joint_endPosLocator_pointConstraint.ctx" "ClavicleJoint__instance_2:clav_2_joint_endPosLocator.tx"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_2_joint_endPosLocator_pointConstraint.cty" "ClavicleJoint__instance_2:clav_2_joint_endPosLocator.ty"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_2_joint_endPosLocator_pointConstraint.ctz" "ClavicleJoint__instance_2:clav_2_joint_endPosLocator.tz"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_2_joint_endPosLocator.pim" "ClavicleJoint__instance_2:clav_2_joint_endPosLocator_pointConstraint.cpim"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_2_joint_endPosLocator.rp" "ClavicleJoint__instance_2:clav_2_joint_endPosLocator_pointConstraint.crp"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_2_joint_endPosLocator.rpt" "ClavicleJoint__instance_2:clav_2_joint_endPosLocator_pointConstraint.crt"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_2_joint_translation_control.t" "ClavicleJoint__instance_2:clav_2_joint_endPosLocator_pointConstraint.tg[0].tt"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_2_joint_translation_control.rp" "ClavicleJoint__instance_2:clav_2_joint_endPosLocator_pointConstraint.tg[0].trp"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_2_joint_translation_control.rpt" "ClavicleJoint__instance_2:clav_2_joint_endPosLocator_pointConstraint.tg[0].trt"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_2_joint_translation_control.pm" "ClavicleJoint__instance_2:clav_2_joint_endPosLocator_pointConstraint.tg[0].tpm"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_2_joint_endPosLocator_pointConstraint.w0" "ClavicleJoint__instance_2:clav_2_joint_endPosLocator_pointConstraint.tg[0].tw"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp_parentConstraint1.ctx" "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp.tx"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp_parentConstraint1.cty" "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp.ty"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp_parentConstraint1.ctz" "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp.tz"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp_parentConstraint1.crx" "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp.rx"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp_parentConstraint1.cry" "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp.ry"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp_parentConstraint1.crz" "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp.rz"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_2_joint.tx" "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp.sx"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp_scaleConstraint1.csy" "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp.sy"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp_scaleConstraint1.csz" "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp.sz"
		 -l on;
connectAttr "groupId19.id" "ClavicleJoint__instance_2:clav_1_joint_orientation_controlShape.iog.og[0].gid"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_m_yAxisBlockSG.mwc" "ClavicleJoint__instance_2:clav_1_joint_orientation_controlShape.iog.og[0].gco"
		 -l on;
connectAttr "groupId20.id" "ClavicleJoint__instance_2:clav_1_joint_orientation_controlShape.iog.og[1].gid"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_m_zAxisBlockSG.mwc" "ClavicleJoint__instance_2:clav_1_joint_orientation_controlShape.iog.og[1].gco"
		 -l on;
connectAttr "groupId18.id" "ClavicleJoint__instance_2:clav_1_joint_orientation_controlShape.ciog.cog[0].cgid"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp.ro" "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp_parentConstraint1.cro"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp.pim" "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp_parentConstraint1.cpim"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp.rp" "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp_parentConstraint1.crp"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp.rpt" "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp_parentConstraint1.crt"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint.t" "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp_parentConstraint1.tg[0].tt"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint.rp" "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp_parentConstraint1.tg[0].trp"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint.rpt" "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp_parentConstraint1.tg[0].trt"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint.r" "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp_parentConstraint1.tg[0].tr"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint.ro" "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp_parentConstraint1.tg[0].tro"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint.s" "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp_parentConstraint1.tg[0].ts"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint.pm" "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp_parentConstraint1.tg[0].tpm"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint.jo" "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp_parentConstraint1.tg[0].tjo"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp_parentConstraint1.w0" "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp_parentConstraint1.tg[0].tw"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp.pim" "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp_scaleConstraint1.cpim"
		 -l on;
connectAttr "ClavicleJoint__instance_2:module_transform.s" "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp_scaleConstraint1.tg[0].ts"
		 -l on;
connectAttr "ClavicleJoint__instance_2:module_transform.pm" "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp_scaleConstraint1.tg[0].tpm"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp_scaleConstraint1.w0" "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp_scaleConstraint1.tg[0].tw"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_pointConstraint.ctx" "ClavicleJoint__instance_2:hook_root_joint.tx"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_pointConstraint.cty" "ClavicleJoint__instance_2:hook_root_joint.ty"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_pointConstraint.ctz" "ClavicleJoint__instance_2:hook_root_joint.tz"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint.s" "ClavicleJoint__instance_2:hook_target_joint.is"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_target_joint_scaleMultiply.ox" "ClavicleJoint__instance_2:hook_target_joint.tx"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_target_joint.tx" "ClavicleJoint__instance_2:hook_root_joint_ikEffector.tx"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_target_joint.ty" "ClavicleJoint__instance_2:hook_root_joint_ikEffector.ty"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_target_joint.tz" "ClavicleJoint__instance_2:hook_root_joint_ikEffector.tz"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint.pim" "ClavicleJoint__instance_2:hook_root_joint_pointConstraint.cpim"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint.rp" "ClavicleJoint__instance_2:hook_root_joint_pointConstraint.crp"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint.rpt" "ClavicleJoint__instance_2:hook_root_joint_pointConstraint.crt"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control.t" "ClavicleJoint__instance_2:hook_root_joint_pointConstraint.tg[0].tt"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control.rp" "ClavicleJoint__instance_2:hook_root_joint_pointConstraint.tg[0].trp"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control.rpt" "ClavicleJoint__instance_2:hook_root_joint_pointConstraint.tg[0].trt"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control.pm" "ClavicleJoint__instance_2:hook_root_joint_pointConstraint.tg[0].tpm"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_pointConstraint.w0" "ClavicleJoint__instance_2:hook_root_joint_pointConstraint.tg[0].tw"
		 -l on;
connectAttr "ClavicleJoint__instance_2:unhookedTarget_pointConstraint1.ctx" "ClavicleJoint__instance_2:unhookedTarget.tx"
		 -l on;
connectAttr "ClavicleJoint__instance_2:unhookedTarget_pointConstraint1.cty" "ClavicleJoint__instance_2:unhookedTarget.ty"
		 -l on;
connectAttr "ClavicleJoint__instance_2:unhookedTarget_pointConstraint1.ctz" "ClavicleJoint__instance_2:unhookedTarget.tz"
		 -l on;
connectAttr "ClavicleJoint__instance_2:unhookedTarget.pim" "ClavicleJoint__instance_2:unhookedTarget_pointConstraint1.cpim"
		 -l on;
connectAttr "ClavicleJoint__instance_2:unhookedTarget.rp" "ClavicleJoint__instance_2:unhookedTarget_pointConstraint1.crp"
		 -l on;
connectAttr "ClavicleJoint__instance_2:unhookedTarget.rpt" "ClavicleJoint__instance_2:unhookedTarget_pointConstraint1.crt"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control.t" "ClavicleJoint__instance_2:unhookedTarget_pointConstraint1.tg[0].tt"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control.rp" "ClavicleJoint__instance_2:unhookedTarget_pointConstraint1.tg[0].trp"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control.rpt" "ClavicleJoint__instance_2:unhookedTarget_pointConstraint1.tg[0].trt"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control.pm" "ClavicleJoint__instance_2:unhookedTarget_pointConstraint1.tg[0].tpm"
		 -l on;
connectAttr "ClavicleJoint__instance_2:unhookedTarget_pointConstraint1.w0" "ClavicleJoint__instance_2:unhookedTarget_pointConstraint1.tg[0].tw"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint.msg" "ClavicleJoint__instance_2:hook_root_joint_ikHandle.hsj"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_ikEffector.hp" "ClavicleJoint__instance_2:hook_root_joint_ikHandle.hee"
		 -l on;
connectAttr "ikRPsolver.msg" "ClavicleJoint__instance_2:hook_root_joint_ikHandle.hsv"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_ikHandle_poleVectorConstraint1.ctx" "ClavicleJoint__instance_2:hook_root_joint_ikHandle.pvx"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_ikHandle_poleVectorConstraint1.cty" "ClavicleJoint__instance_2:hook_root_joint_ikHandle.pvy"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_ikHandle_poleVectorConstraint1.ctz" "ClavicleJoint__instance_2:hook_root_joint_ikHandle.pvz"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_ikHandle_pointConstraint.ctx" "ClavicleJoint__instance_2:hook_root_joint_ikHandle.tx"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_ikHandle_pointConstraint.cty" "ClavicleJoint__instance_2:hook_root_joint_ikHandle.ty"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_ikHandle_pointConstraint.ctz" "ClavicleJoint__instance_2:hook_root_joint_ikHandle.tz"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_ikHandle.pim" "ClavicleJoint__instance_2:hook_root_joint_ikHandle_poleVectorConstraint1.cpim"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint.pm" "ClavicleJoint__instance_2:hook_root_joint_ikHandle_poleVectorConstraint1.ps"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint.t" "ClavicleJoint__instance_2:hook_root_joint_ikHandle_poleVectorConstraint1.crp"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_ikHandle_poleVectorLocator.t" "ClavicleJoint__instance_2:hook_root_joint_ikHandle_poleVectorConstraint1.tg[0].tt"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_ikHandle_poleVectorLocator.rp" "ClavicleJoint__instance_2:hook_root_joint_ikHandle_poleVectorConstraint1.tg[0].trp"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_ikHandle_poleVectorLocator.rpt" "ClavicleJoint__instance_2:hook_root_joint_ikHandle_poleVectorConstraint1.tg[0].trt"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_ikHandle_poleVectorLocator.pm" "ClavicleJoint__instance_2:hook_root_joint_ikHandle_poleVectorConstraint1.tg[0].tpm"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_ikHandle_poleVectorConstraint1.w0" "ClavicleJoint__instance_2:hook_root_joint_ikHandle_poleVectorConstraint1.tg[0].tw"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_ikHandle.pim" "ClavicleJoint__instance_2:hook_root_joint_ikHandle_pointConstraint.cpim"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_ikHandle.rp" "ClavicleJoint__instance_2:hook_root_joint_ikHandle_pointConstraint.crp"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_ikHandle.rpt" "ClavicleJoint__instance_2:hook_root_joint_ikHandle_pointConstraint.crt"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_target_joint_endPosLocator.t" "ClavicleJoint__instance_2:hook_root_joint_ikHandle_pointConstraint.tg[0].tt"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_target_joint_endPosLocator.rp" "ClavicleJoint__instance_2:hook_root_joint_ikHandle_pointConstraint.tg[0].trp"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_target_joint_endPosLocator.rpt" "ClavicleJoint__instance_2:hook_root_joint_ikHandle_pointConstraint.tg[0].trt"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_target_joint_endPosLocator.pm" "ClavicleJoint__instance_2:hook_root_joint_ikHandle_pointConstraint.tg[0].tpm"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_ikHandle_pointConstraint.w0" "ClavicleJoint__instance_2:hook_root_joint_ikHandle_pointConstraint.tg[0].tw"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_rootPosLocator_pointConstraint.ctx" "ClavicleJoint__instance_2:hook_root_joint_rootPosLocator.tx"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_rootPosLocator_pointConstraint.cty" "ClavicleJoint__instance_2:hook_root_joint_rootPosLocator.ty"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_rootPosLocator_pointConstraint.ctz" "ClavicleJoint__instance_2:hook_root_joint_rootPosLocator.tz"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_rootPosLocator.pim" "ClavicleJoint__instance_2:hook_root_joint_rootPosLocator_pointConstraint.cpim"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_rootPosLocator.rp" "ClavicleJoint__instance_2:hook_root_joint_rootPosLocator_pointConstraint.crp"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_rootPosLocator.rpt" "ClavicleJoint__instance_2:hook_root_joint_rootPosLocator_pointConstraint.crt"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint.t" "ClavicleJoint__instance_2:hook_root_joint_rootPosLocator_pointConstraint.tg[0].tt"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint.rp" "ClavicleJoint__instance_2:hook_root_joint_rootPosLocator_pointConstraint.tg[0].trp"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint.rpt" "ClavicleJoint__instance_2:hook_root_joint_rootPosLocator_pointConstraint.tg[0].trt"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint.pm" "ClavicleJoint__instance_2:hook_root_joint_rootPosLocator_pointConstraint.tg[0].tpm"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_rootPosLocator_pointConstraint.w0" "ClavicleJoint__instance_2:hook_root_joint_rootPosLocator_pointConstraint.tg[0].tw"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_pointConstraint.ctx" "ClavicleJoint__instance_2:hook_target_joint_endPosLocator.tx"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_pointConstraint.cty" "ClavicleJoint__instance_2:hook_target_joint_endPosLocator.ty"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_pointConstraint.ctz" "ClavicleJoint__instance_2:hook_target_joint_endPosLocator.tz"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_target_joint_endPosLocator.pim" "ClavicleJoint__instance_2:hook_pointConstraint.cpim"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_target_joint_endPosLocator.rp" "ClavicleJoint__instance_2:hook_pointConstraint.crp"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_target_joint_endPosLocator.rpt" "ClavicleJoint__instance_2:hook_pointConstraint.crt"
		 -l on;
connectAttr "ClavicleJoint__instance_2:unhookedTarget.t" "ClavicleJoint__instance_2:hook_pointConstraint.tg[0].tt"
		 -l on;
connectAttr "ClavicleJoint__instance_2:unhookedTarget.rp" "ClavicleJoint__instance_2:hook_pointConstraint.tg[0].trp"
		 -l on;
connectAttr "ClavicleJoint__instance_2:unhookedTarget.rpt" "ClavicleJoint__instance_2:hook_pointConstraint.tg[0].trt"
		 -l on;
connectAttr "ClavicleJoint__instance_2:unhookedTarget.pm" "ClavicleJoint__instance_2:hook_pointConstraint.tg[0].tpm"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_pointConstraint.w0" "ClavicleJoint__instance_2:hook_pointConstraint.tg[0].tw"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp_parentConstraint1.ctx" "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp.tx"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp_parentConstraint1.cty" "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp.ty"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp_parentConstraint1.ctz" "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp.tz"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp_parentConstraint1.crx" "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp.rx"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp_parentConstraint1.cry" "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp.ry"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp_parentConstraint1.crz" "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp.rz"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_target_joint.tx" "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp.sx"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp_scaleConstraint1.csy" "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp.sy"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp_scaleConstraint1.csz" "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp.sz"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp.ro" "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp_parentConstraint1.cro"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp.pim" "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp_parentConstraint1.cpim"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp.rp" "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp_parentConstraint1.crp"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp.rpt" "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp_parentConstraint1.crt"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint.t" "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp_parentConstraint1.tg[0].tt"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint.rp" "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp_parentConstraint1.tg[0].trp"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint.rpt" "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp_parentConstraint1.tg[0].trt"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint.r" "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp_parentConstraint1.tg[0].tr"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint.ro" "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp_parentConstraint1.tg[0].tro"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint.s" "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp_parentConstraint1.tg[0].ts"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint.pm" "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp_parentConstraint1.tg[0].tpm"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint.jo" "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp_parentConstraint1.tg[0].tjo"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp_parentConstraint1.w0" "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp_parentConstraint1.tg[0].tw"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp.pim" "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp_scaleConstraint1.cpim"
		 -l on;
connectAttr "ClavicleJoint__instance_2:module_transform.s" "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp_scaleConstraint1.tg[0].ts"
		 -l on;
connectAttr "ClavicleJoint__instance_2:module_transform.pm" "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp_scaleConstraint1.tg[0].tpm"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp_scaleConstraint1.w0" "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp_scaleConstraint1.tg[0].tw"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocator_parentConstraintGroup_parentConstraint1.ctx" "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocator_parentConstraintGroup.tx"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocator_parentConstraintGroup_parentConstraint1.cty" "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocator_parentConstraintGroup.ty"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocator_parentConstraintGroup_parentConstraint1.ctz" "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocator_parentConstraintGroup.tz"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocator_parentConstraintGroup_parentConstraint1.crx" "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocator_parentConstraintGroup.rx"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocator_parentConstraintGroup_parentConstraint1.cry" "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocator_parentConstraintGroup.ry"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocator_parentConstraintGroup_parentConstraint1.crz" "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocator_parentConstraintGroup.rz"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocator_parentConstraintGroup.ro" "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocator_parentConstraintGroup_parentConstraint1.cro"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocator_parentConstraintGroup.pim" "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocator_parentConstraintGroup_parentConstraint1.cpim"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocator_parentConstraintGroup.rp" "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocator_parentConstraintGroup_parentConstraint1.crp"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocator_parentConstraintGroup.rpt" "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocator_parentConstraintGroup_parentConstraint1.crt"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control.t" "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocator_parentConstraintGroup_parentConstraint1.tg[0].tt"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control.rp" "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocator_parentConstraintGroup_parentConstraint1.tg[0].trp"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control.rpt" "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocator_parentConstraintGroup_parentConstraint1.tg[0].trt"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control.r" "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocator_parentConstraintGroup_parentConstraint1.tg[0].tr"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control.ro" "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocator_parentConstraintGroup_parentConstraint1.tg[0].tro"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control.s" "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocator_parentConstraintGroup_parentConstraint1.tg[0].ts"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control.pm" "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocator_parentConstraintGroup_parentConstraint1.tg[0].tpm"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocator_parentConstraintGroup_parentConstraint1.w0" "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocator_parentConstraintGroup_parentConstraint1.tg[0].tw"
		 -l on;
connectAttr "ClavicleJoint__instance_2:module_transform.sy" "ClavicleJoint__instance_2:module_transform.sx"
		 -l on;
connectAttr "ClavicleJoint__instance_2:module_transform.sy" "ClavicleJoint__instance_2:module_transform.sz"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint.r" "ClavicleJoint__instance_2:module_container.boc[0]"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint.rx" "ClavicleJoint__instance_2:module_container.boc[1]"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint.ry" "ClavicleJoint__instance_2:module_container.boc[2]"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint.rz" "ClavicleJoint__instance_2:module_container.boc[3]"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint.ro" "ClavicleJoint__instance_2:module_container.boc[4]"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_2_joint.r" "ClavicleJoint__instance_2:module_container.boc[5]"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_2_joint.rx" "ClavicleJoint__instance_2:module_container.boc[6]"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_2_joint.ry" "ClavicleJoint__instance_2:module_container.boc[7]"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_2_joint.rz" "ClavicleJoint__instance_2:module_container.boc[8]"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_2_joint.ro" "ClavicleJoint__instance_2:module_container.boc[9]"
		 -l on;
connectAttr "ClavicleJoint__instance_2:module_transform.t" "ClavicleJoint__instance_2:module_container.boc[10]"
		 -l on;
connectAttr "ClavicleJoint__instance_2:module_transform.tx" "ClavicleJoint__instance_2:module_container.boc[11]"
		 -l on;
connectAttr "ClavicleJoint__instance_2:module_transform.ty" "ClavicleJoint__instance_2:module_container.boc[12]"
		 -l on;
connectAttr "ClavicleJoint__instance_2:module_transform.tz" "ClavicleJoint__instance_2:module_container.boc[13]"
		 -l on;
connectAttr "ClavicleJoint__instance_2:module_transform.r" "ClavicleJoint__instance_2:module_container.boc[14]"
		 -l on;
connectAttr "ClavicleJoint__instance_2:module_transform.rx" "ClavicleJoint__instance_2:module_container.boc[15]"
		 -l on;
connectAttr "ClavicleJoint__instance_2:module_transform.ry" "ClavicleJoint__instance_2:module_container.boc[16]"
		 -l on;
connectAttr "ClavicleJoint__instance_2:module_transform.rz" "ClavicleJoint__instance_2:module_container.boc[17]"
		 -l on;
connectAttr "ClavicleJoint__instance_2:module_transform.sy" "ClavicleJoint__instance_2:module_container.boc[18]"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control_container.boc[0]" "ClavicleJoint__instance_2:module_container.boc[19]"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control_container.boc[1]" "ClavicleJoint__instance_2:module_container.boc[20]"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control_container.boc[2]" "ClavicleJoint__instance_2:module_container.boc[21]"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control_container.boc[3]" "ClavicleJoint__instance_2:module_container.boc[22]"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_2_joint_translation_control_container.boc[0]" "ClavicleJoint__instance_2:module_container.boc[23]"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_2_joint_translation_control_container.boc[1]" "ClavicleJoint__instance_2:module_container.boc[24]"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_2_joint_translation_control_container.boc[2]" "ClavicleJoint__instance_2:module_container.boc[25]"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_2_joint_translation_control_container.boc[3]" "ClavicleJoint__instance_2:module_container.boc[26]"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_orientation_control_container.boc[0]" "ClavicleJoint__instance_2:module_container.boc[27]"
		 -l on;
connectAttr "hyperLayout3.msg" "ClavicleJoint__instance_2:module_container.hl" -l
		 on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_ikHandle_scaleFactor.ox" "ClavicleJoint__instance_2:clav_1_joint_ikHandle_lockBlend.c1r"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_rootPosLocatorShape.wp" "ClavicleJoint__instance_2:distBetween_clav_1_joint_rootPosLocator_clav_2_joint_endPosLocator.p1"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_2_joint_endPosLocatorShape.wp" "ClavicleJoint__instance_2:distBetween_clav_1_joint_rootPosLocator_clav_2_joint_endPosLocator.p2"
		 -l on;
connectAttr "ClavicleJoint__instance_2:module_grp.msg" "hyperLayout3.hyp[0].dn";
connectAttr "ClavicleJoint__instance_2:joints_grp.msg" "hyperLayout3.hyp[1].dn";
connectAttr "ClavicleJoint__instance_2:orientationControls_grp.msg" "hyperLayout3.hyp[3].dn"
		;
connectAttr "ClavicleJoint__instance_2:preferredAngleRepresentation_grp.msg" "hyperLayout3.hyp[4].dn"
		;
connectAttr "ClavicleJoint__instance_2:clav_1_joint.msg" "hyperLayout3.hyp[5].dn"
		;
connectAttr "ClavicleJoint__instance_2:clav_2_joint.msg" "hyperLayout3.hyp[6].dn"
		;
connectAttr "ClavicleJoint__instance_2:module_transform.msg" "hyperLayout3.hyp[7].dn"
		;
connectAttr "ClavicleJoint__instance_2:module_transformShape.msg" "hyperLayout3.hyp[8].dn"
		;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control_container.msg" "hyperLayout3.hyp[9].dn"
		;
connectAttr "ClavicleJoint__instance_2:clav_2_joint_translation_control_container.msg" "hyperLayout3.hyp[10].dn"
		;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_pointConstraint.msg" "hyperLayout3.hyp[11].dn"
		;
connectAttr "ClavicleJoint__instance_2:hook_container.msg" "hyperLayout3.hyp[12].dn"
		;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_ikHandle.msg" "hyperLayout3.hyp[14].dn"
		;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_ikHandle_poleVectorConstraint1.msg" "hyperLayout3.hyp[15].dn"
		;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_ikHandle_pointConstraint.msg" "hyperLayout3.hyp[16].dn"
		;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_ikEffector.msg" "hyperLayout3.hyp[17].dn"
		;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_rootPosLocator.msg" "hyperLayout3.hyp[18].dn"
		;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_rootPosLocatorShape.msg" "hyperLayout3.hyp[19].dn"
		;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_rootPosLocator_pointConstraint.msg" "hyperLayout3.hyp[20].dn"
		;
connectAttr "ClavicleJoint__instance_2:clav_2_joint_endPosLocator.msg" "hyperLayout3.hyp[21].dn"
		;
connectAttr "ClavicleJoint__instance_2:clav_2_joint_endPosLocatorShape.msg" "hyperLayout3.hyp[22].dn"
		;
connectAttr "ClavicleJoint__instance_2:distBetween_clav_1_joint_rootPosLocator_clav_2_joint_endPosLocator.msg" "hyperLayout3.hyp[23].dn"
		;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_ikHandle_scaleFactor.msg" "hyperLayout3.hyp[24].dn"
		;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_ikHandle_lockBlend.msg" "hyperLayout3.hyp[25].dn"
		;
connectAttr "ClavicleJoint__instance_2:clav_2_joint_scaleMultiply.msg" "hyperLayout3.hyp[26].dn"
		;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocator_parentConstraintGroup.msg" "hyperLayout3.hyp[27].dn"
		;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocator.msg" "hyperLayout3.hyp[28].dn"
		;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocatorShape.msg" "hyperLayout3.hyp[29].dn"
		;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control_poleVectorLocator_parentConstraintGroup_parentConstraint1.msg" "hyperLayout3.hyp[30].dn"
		;
connectAttr "ClavicleJoint__instance_2:clav_2_joint_endPosLocator_pointConstraint.msg" "hyperLayout3.hyp[31].dn"
		;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_orientation_control_container.msg" "hyperLayout3.hyp[33].dn"
		;
connectAttr "orientation_control_hyperLayout1.msg" "ClavicleJoint__instance_2:clav_1_joint_orientation_control_container.hl"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_orientation_control.rx" "ClavicleJoint__instance_2:clav_1_joint_orientation_control_container.boc[0]"
		;
connectAttr "translation_control01_hyperLayout5.msg" "ClavicleJoint__instance_2:clav_2_joint_translation_control_container.hl"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_2_joint_translation_control.t" "ClavicleJoint__instance_2:clav_2_joint_translation_control_container.boc[0]"
		;
connectAttr "ClavicleJoint__instance_2:clav_2_joint_translation_control.tx" "ClavicleJoint__instance_2:clav_2_joint_translation_control_container.boc[1]"
		;
connectAttr "ClavicleJoint__instance_2:clav_2_joint_translation_control.ty" "ClavicleJoint__instance_2:clav_2_joint_translation_control_container.boc[2]"
		;
connectAttr "ClavicleJoint__instance_2:clav_2_joint_translation_control.tz" "ClavicleJoint__instance_2:clav_2_joint_translation_control_container.boc[3]"
		;
connectAttr "ClavicleJoint__instance_2:hook_root_joint.r" "ClavicleJoint__instance_2:hook_container.boc[0]"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint.rx" "ClavicleJoint__instance_2:hook_container.boc[1]"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint.ry" "ClavicleJoint__instance_2:hook_container.boc[2]"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint.rz" "ClavicleJoint__instance_2:hook_container.boc[3]"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_target_joint.r" "ClavicleJoint__instance_2:hook_container.boc[4]"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_target_joint.rx" "ClavicleJoint__instance_2:hook_container.boc[5]"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_target_joint.ry" "ClavicleJoint__instance_2:hook_container.boc[6]"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_target_joint.rz" "ClavicleJoint__instance_2:hook_container.boc[7]"
		 -l on;
connectAttr "hyperLayout4.msg" "ClavicleJoint__instance_2:hook_container.hl" -l on
		;
connectAttr "translation_control01_hyperLayout4.msg" "ClavicleJoint__instance_2:clav_1_joint_translation_control_container.hl"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control.t" "ClavicleJoint__instance_2:clav_1_joint_translation_control_container.boc[0]"
		;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control.tx" "ClavicleJoint__instance_2:clav_1_joint_translation_control_container.boc[1]"
		;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control.ty" "ClavicleJoint__instance_2:clav_1_joint_translation_control_container.boc[2]"
		;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control.tz" "ClavicleJoint__instance_2:clav_1_joint_translation_control_container.boc[3]"
		;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_ikHandle_scaleFactor.ox" "ClavicleJoint__instance_2:clav_2_joint_scaleMultiply.i2x"
		 -l on;
connectAttr "ClavicleJoint__instance_2:distBetween_clav_1_joint_rootPosLocator_clav_2_joint_endPosLocator.d" "ClavicleJoint__instance_2:clav_1_joint_ikHandle_scaleFactor.i1x"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_m_translation_control_SG.msg" "translation_control01_materialInfo3.sg"
		;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_m_translation_control.msg" "translation_control01_materialInfo3.m"
		;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_m_translation_control.oc" "ClavicleJoint__instance_2:clav_1_joint_m_translation_control_SG.ss"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_controlShape.iog" "ClavicleJoint__instance_2:clav_1_joint_m_translation_control_SG.dsm"
		 -l on -na;
connectAttr "ClavicleJoint__instance_2:clav_2_joint_m_translation_control_SG.msg" "translation_control01_materialInfo4.sg"
		;
connectAttr "ClavicleJoint__instance_2:clav_2_joint_m_translation_control.msg" "translation_control01_materialInfo4.m"
		;
connectAttr "ClavicleJoint__instance_2:clav_2_joint_m_translation_control.oc" "ClavicleJoint__instance_2:clav_2_joint_m_translation_control_SG.ss"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_2_joint_translation_controlShape.iog" "ClavicleJoint__instance_2:clav_2_joint_m_translation_control_SG.dsm"
		 -l on -na;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_m_yAxisBlock.msg" "orientation_control_hyperLayout1.hyp[0].dn"
		;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_m_zAxisBlock.msg" "orientation_control_hyperLayout1.hyp[1].dn"
		;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_m_yAxisBlockSG.msg" "orientation_control_hyperLayout1.hyp[3].dn"
		;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_m_zAxisBlockSG.msg" "orientation_control_hyperLayout1.hyp[4].dn"
		;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_orientation_control.msg" "orientation_control_hyperLayout1.hyp[5].dn"
		;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_orientation_controlShape.msg" "orientation_control_hyperLayout1.hyp[6].dn"
		;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp.msg" "orientation_control_hyperLayout1.hyp[7].dn"
		;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp_parentConstraint1.msg" "orientation_control_hyperLayout1.hyp[8].dn"
		;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_orientation_control_parentConstraint_grp_scaleConstraint1.msg" "orientation_control_hyperLayout1.hyp[9].dn"
		;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_m_zAxisBlock.oc" "ClavicleJoint__instance_2:clav_1_joint_m_zAxisBlockSG.ss"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_orientation_controlShape.iog.og[1]" "ClavicleJoint__instance_2:clav_1_joint_m_zAxisBlockSG.dsm"
		 -l on -na;
connectAttr "groupId20.msg" "ClavicleJoint__instance_2:clav_1_joint_m_zAxisBlockSG.gn"
		 -l on -na;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_m_yAxisBlock.oc" "ClavicleJoint__instance_2:clav_1_joint_m_yAxisBlockSG.ss"
		 -l on;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_orientation_controlShape.iog.og[0]" "ClavicleJoint__instance_2:clav_1_joint_m_yAxisBlockSG.dsm"
		 -l on -na;
connectAttr "groupId19.msg" "ClavicleJoint__instance_2:clav_1_joint_m_yAxisBlockSG.gn"
		 -l on -na;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_m_zAxisBlockSG.msg" "orientation_control_materialInfo1.sg"
		;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_m_zAxisBlock.msg" "orientation_control_materialInfo1.m"
		;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_m_yAxisBlockSG.msg" "materialInfo2.sg"
		;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_m_yAxisBlock.msg" "materialInfo2.m"
		;
connectAttr "ClavicleJoint__instance_2:clav_2_joint_translation_controlShape.msg" "translation_control01_hyperLayout5.hyp[0].dn"
		;
connectAttr "ClavicleJoint__instance_2:clav_2_joint_translation_control.msg" "translation_control01_hyperLayout5.hyp[1].dn"
		;
connectAttr "ClavicleJoint__instance_2:clav_2_joint_m_translation_control_SG.msg" "translation_control01_hyperLayout5.hyp[2].dn"
		;
connectAttr "ClavicleJoint__instance_2:clav_2_joint_m_translation_control.msg" "translation_control01_hyperLayout5.hyp[3].dn"
		;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_ikHandle_scaleFactor.ox" "ClavicleJoint__instance_2:hook_root_joint_ikHandle_lockBlend.c1r"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_rootPosLocatorShape.wp" "ClavicleJoint__instance_2:distBetween_hook_root_joint_rootPosLocator_hook_target_joint_endPosLocator.p1"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_target_joint_endPosLocatorShape.wp" "ClavicleJoint__instance_2:distBetween_hook_root_joint_rootPosLocator_hook_target_joint_endPosLocator.p2"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_grp.msg" "hyperLayout4.hyp[0].dn";
connectAttr "ClavicleJoint__instance_2:hook_root_joint.msg" "hyperLayout4.hyp[1].dn"
		;
connectAttr "ClavicleJoint__instance_2:hook_target_joint.msg" "hyperLayout4.hyp[2].dn"
		;
connectAttr "ClavicleJoint__instance_2:unhookedTarget.msg" "hyperLayout4.hyp[3].dn"
		;
connectAttr "ClavicleJoint__instance_2:unhookedTargetShape.msg" "hyperLayout4.hyp[4].dn"
		;
connectAttr "ClavicleJoint__instance_2:unhookedTarget_pointConstraint1.msg" "hyperLayout4.hyp[5].dn"
		;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_ikHandle.msg" "hyperLayout4.hyp[6].dn"
		;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_ikHandle_poleVectorConstraint1.msg" "hyperLayout4.hyp[7].dn"
		;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_ikHandle_pointConstraint.msg" "hyperLayout4.hyp[8].dn"
		;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_ikEffector.msg" "hyperLayout4.hyp[9].dn"
		;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_ikHandle_poleVectorLocator.msg" "hyperLayout4.hyp[10].dn"
		;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_ikHandle_poleVectorLocatorShape.msg" "hyperLayout4.hyp[11].dn"
		;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_rootPosLocator.msg" "hyperLayout4.hyp[12].dn"
		;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_rootPosLocatorShape.msg" "hyperLayout4.hyp[13].dn"
		;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_rootPosLocator_pointConstraint.msg" "hyperLayout4.hyp[14].dn"
		;
connectAttr "ClavicleJoint__instance_2:hook_target_joint_endPosLocator.msg" "hyperLayout4.hyp[15].dn"
		;
connectAttr "ClavicleJoint__instance_2:hook_target_joint_endPosLocatorShape.msg" "hyperLayout4.hyp[16].dn"
		;
connectAttr "ClavicleJoint__instance_2:distBetween_hook_root_joint_rootPosLocator_hook_target_joint_endPosLocator.msg" "hyperLayout4.hyp[17].dn"
		;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_ikHandle_scaleFactor.msg" "hyperLayout4.hyp[18].dn"
		;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_ikHandle_lockBlend.msg" "hyperLayout4.hyp[19].dn"
		;
connectAttr "ClavicleJoint__instance_2:hook_target_joint_scaleMultiply.msg" "hyperLayout4.hyp[20].dn"
		;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_pointConstraint.msg" "hyperLayout4.hyp[21].dn"
		;
connectAttr "ClavicleJoint__instance_2:hook_pointConstraint.msg" "hyperLayout4.hyp[22].dn"
		;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_hook_representation_container.msg" "hyperLayout4.hyp[23].dn"
		;
connectAttr "hook_representation_hyperLayout2.msg" "ClavicleJoint__instance_2:hook_root_joint_hook_representation_container.hl"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_ikHandle_scaleFactor.ox" "ClavicleJoint__instance_2:hook_target_joint_scaleMultiply.i2x"
		 -l on;
connectAttr "ClavicleJoint__instance_2:distBetween_hook_root_joint_rootPosLocator_hook_target_joint_endPosLocator.d" "ClavicleJoint__instance_2:hook_root_joint_ikHandle_scaleFactor.i1x"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_m_hookRepresentation.msg" "hook_representation_hyperLayout2.hyp[1].dn"
		;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_m_hookRepresentation_SG.msg" "hook_representation_hyperLayout2.hyp[3].dn"
		;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_hook_representation.msg" "hook_representation_hyperLayout2.hyp[4].dn"
		;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_hook_representationShape.msg" "hook_representation_hyperLayout2.hyp[5].dn"
		;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp.msg" "hook_representation_hyperLayout2.hyp[6].dn"
		;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp_parentConstraint1.msg" "hook_representation_hyperLayout2.hyp[7].dn"
		;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_hook_representation_parentConstraint_grp_scaleConstraint1.msg" "hook_representation_hyperLayout2.hyp[8].dn"
		;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_m_hookRepresentation.oc" "ClavicleJoint__instance_2:hook_root_joint_m_hookRepresentation_SG.ss"
		 -l on;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_hook_representationShape.iog" "ClavicleJoint__instance_2:hook_root_joint_m_hookRepresentation_SG.dsm"
		 -l on -na;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_m_hookRepresentation_SG.msg" "hook_representation_materialInfo2.sg"
		;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_m_hookRepresentation.msg" "hook_representation_materialInfo2.m"
		;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_controlShape.msg" "translation_control01_hyperLayout4.hyp[0].dn"
		;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_translation_control.msg" "translation_control01_hyperLayout4.hyp[1].dn"
		;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_m_translation_control_SG.msg" "translation_control01_hyperLayout4.hyp[2].dn"
		;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_m_translation_control.msg" "translation_control01_hyperLayout4.hyp[3].dn"
		;
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "ClavicleJoint__instance_2:clav_1_joint_m_translation_control_SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "ClavicleJoint__instance_2:clav_2_joint_m_translation_control_SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "ClavicleJoint__instance_2:hook_root_joint_m_hookRepresentation_SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "ClavicleJoint__instance_2:clav_1_joint_m_zAxisBlockSG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "ClavicleJoint__instance_2:clav_1_joint_m_yAxisBlockSG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "ClavicleJoint__instance_2:clav_1_joint_m_translation_control_SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "ClavicleJoint__instance_2:clav_2_joint_m_translation_control_SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "ClavicleJoint__instance_2:hook_root_joint_m_hookRepresentation_SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "ClavicleJoint__instance_2:clav_1_joint_m_zAxisBlockSG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "ClavicleJoint__instance_2:clav_1_joint_m_yAxisBlockSG.message" ":defaultLightSet.message";
connectAttr "ClavicleJoint__instance_2:clav_1_joint_m_translation_control_SG.pa" ":renderPartition.st"
		 -na;
connectAttr "ClavicleJoint__instance_2:clav_2_joint_m_translation_control_SG.pa" ":renderPartition.st"
		 -na;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_m_hookRepresentation_SG.pa" ":renderPartition.st"
		 -na;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_m_zAxisBlockSG.pa" ":renderPartition.st"
		 -na;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_m_yAxisBlockSG.pa" ":renderPartition.st"
		 -na;
connectAttr "ClavicleJoint__instance_2:module_transformShape.iog" ":initialShadingGroup.dsm"
		 -na;
connectAttr "groupId18.msg" ":initialShadingGroup.gn" -na;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_m_translation_control.msg" ":defaultShaderList1.s"
		 -na;
connectAttr "ClavicleJoint__instance_2:clav_2_joint_m_translation_control.msg" ":defaultShaderList1.s"
		 -na;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_m_hookRepresentation.msg" ":defaultShaderList1.s"
		 -na;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_m_yAxisBlock.msg" ":defaultShaderList1.s"
		 -na;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_m_zAxisBlock.msg" ":defaultShaderList1.s"
		 -na;
connectAttr "ClavicleJoint__instance_2:distBetween_hook_root_joint_rootPosLocator_hook_target_joint_endPosLocator.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_ikHandle_scaleFactor.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "ClavicleJoint__instance_2:hook_root_joint_ikHandle_lockBlend.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "ClavicleJoint__instance_2:hook_target_joint_scaleMultiply.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "ClavicleJoint__instance_2:distBetween_clav_1_joint_rootPosLocator_clav_2_joint_endPosLocator.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_ikHandle_scaleFactor.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "ClavicleJoint__instance_2:clav_1_joint_ikHandle_lockBlend.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "ClavicleJoint__instance_2:clav_2_joint_scaleMultiply.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "ikRPsolver.msg" ":ikSystem.sol" -na;
// End of __duplicationCache.ma

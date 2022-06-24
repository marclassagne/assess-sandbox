import ast
import json


chainetest8='{"attributes":[{"type":"Quantitative","name":"pieniche","unit":"euros","val_min":20,"val_med":["40","60","80"],"val_max":100,"method":"PE","mode":"Normal","completed":"False","checked":true,"questionnaire":{"number":3,"points":{"40":0.84,"60":0.53,"80":0.53},"utility":{}},"fonction":"","numero":10000,"pts":{"points":[1,2,3],"coord":[[40,0.84],[60,0.53],[80,0.53],[20,0],[100,1]],"exp":{"a":-1.9191482063869867,"b":0.02581486736601345,"c":1.1452055010184803,"r2":0.44598575328363266},"quad":{"a":-0.4308823525053793,"b":0.00009044117625268966,"c":0.02335294115032276,"r2":0.39715930786390397},"pow":{"a":3.136486157974913,"b":1.4312596466171799,"c":-5.274722945854125,"r2":0.502458234590003},"log":{"a":0.32468596216649903,"b":2.1272950919449,"c":-34.3467348077245,"d":-0.6831498386234012,"r2":0.5310694648771104},"lin":{"a":0.0125,"b":-0.25,"r2":0.32114793303723943},"expo-power":{"a":-1329.51385231972,"b":-7.191169339986957,"c":0.00006494757136591836,"r2":0.48641445061627153}}},{"type":"Quantitative","name":"ccxw","unit":"cxw","val_min":10,"val_med":["32.5","55","77.5"],"val_max":100,"method":"PE","mode":"Normal","completed":"False","checked":true,"questionnaire":{"number":3,"points":{"55":0.99,"32.5":0.53,"77.5":0.73},"utility":{}},"fonction":"exponential","numero":0,"pts":{"points":[1,2,3],"coord":[[55,0.99],[32.5,0.53],[77.5,0.73],[10,0],[100,1]],"exp":{"a":-1.4896251158329652,"b":0.03577322504935598,"c":1.041635670434959,"r2":0.8908352714381447},"quad":{"a":-0.2702977485113743,"b":0.00015918663740026318,"c":0.02862164122514006,"r2":0.8560489649337869},"pow":{"a":1.1969641446475172,"b":1.2992359083227023,"c":-1.991754964471044,"r2":0.888801104602549},"log":{"a":0.3185035756440177,"b":0.1906251085295721,"c":-1.1298276572673602,"d":0.08059963990358916,"r2":0.8871179063021882},"lin":{"a":0.011111111111111112,"b":-0.1111111111111111,"r2":0.5319929556794833},"expo-power":{"a":-1719.011571116851,"b":-7.4489232215532795,"c":0.00003390274544170721,"r2":0.8707831828593062}}},{"type":"Quantitative","name":"mmm","unit":"","val_min":10,"val_med":["32.5","55","77.5"],"val_max":100,"method":"PE","mode":"Normal","completed":"False","checked":true,"questionnaire":{"number":3,"points":{"55":0.82,"32.5":0.2,"77.5":0.39},"utility":{}},"fonction":"exponential","numero":0,"pts":{"points":[1,2,3],"coord":[[55,0.82],[32.5,0.2],[77.5,0.39],[10,0],[100,1]],"exp":{"a":-18.795799923954622,"b":0.0006112841886286983,"c":18.681254626222884,"r2":0.6664950193280739},"quad":{"a":-0.1140159765429742,"b":0.0000029048654318630796,"c":0.01143064630861605,"r2":0.6664772499029203},"pow":{"a":0.015034103358754042,"b":0.0785947120210767,"c":-0.11983804404824973,"r2":0.6674234672113066},"log":{"a":15.217027150825148,"b":0.0045557833974184106,"c":5.990970324325804,"d":-27.35761329067605,"r2":0.6665193211491609},"lin":{"a":0.011111111111111112,"b":-0.1111111111111111,"r2":0.6663726382881858},"expo-power":{"a":-1.193913262417174,"b":-0.03998123550602599,"c":0.6466966305747452,"r2":0.67036429788662}}},{"type":"Quantitative","name":"fdsf","unit":"sfdfq","val_min":20,"val_med":["40","60","80"],"val_max":100,"method":"PE","mode":"Normal","completed":"False","checked":true,"questionnaire":{"number":3,"points":{"40":0.86,"60":0.03,"80":0.96},"utility":{}},"fonction":"exponential","numero":0,"pts":{"points":[1,2,3],"coord":[[40,0.86],[60,0.03],[80,0.96],[20,0],[100,1]],"exp":{"a":-2.3732799817152297,"b":0.008700495775937487,"c":1.9942400318877038,"r2":0.3979369604203541},"quad":{"a":-0.33529411721100444,"b":0.00004264705860550222,"c":0.017617647032660267,"r2":0.3955224726744976},"pow":{"a":0.1641420402642862,"b":0.6531497900629418,"c":-0.8644074295538738,"r2":0.4091527624065955},"log":{"a":0.8478783340439661,"b":0.08253642212774154,"c":1.2806827488076717,"d":-0.9118795333368924,"r2":0.40447379290518615},"lin":{"a":0.0125,"b":-0.25,"r2":0.38598689282960674},"expo-power":{"a":-2.6207480786784547,"b":-0.5623134335768297,"c":0.17974615648554126,"r2":0.4098663929155476}}},{"type":"Quantitative","name":"oussama","unit":"magnif","val_min":20,"val_med":["265","510","755"],"val_max":1000,"method":"PE","mode":"Normal","completed":"False","checked":true,"questionnaire":{"number":3,"points":{"265":0.93,"510":0.03,"755":0.14},"utility":{}},"fonction":"exponential","numero":0,"pts":{"points":[1,2,3],"coord":[[265,0.93],[510,0.03],[755,0.14],[20,0],[1000,1]],"exp":{"a":-7.3890560989306495,"b":0.1,"c":1,"r2":-0.6796890572023062},"quad":{"a":-0.0040424331643147534,"b":-8.182865050495684e-7,"c":0.0001857559281147463,"r2":0.029924726518073652},"pow":{"a":2.2277730073445542e-20,"b":-5.828825015597496,"c":-2.500524609264332e-12,"r2":0.13780323437858122},"log":{"a":-0.20024511228080455,"b":-0.08813221332070803,"c":88.72173611395195,"d":0.8941820935283752,"r2":0.21143773835645174},"lin":{"a":0.0010204081632653062,"b":-0.02040816326530612,"r2":-0.051823799083117406},"expo-power":{"a":-1.0000000075312923,"b":-6.001575939212203e-15,"c":4.687520052571654,"r2":0.13649087042764319}}}],"k_calculus":[{"method":"multiplicative","active":true,"k":[{"ID":1,"ID_attribute":0,"attribute":"pieniche","type":"Quantitative","value":null},{"ID":2,"ID_attribute":1,"attribute":"ccxw","type":"Quantitative","value":null},{"ID":3,"ID_attribute":2,"attribute":"mmm","type":"Quantitative","value":null},{"ID":4,"ID_attribute":3,"attribute":"fdsf","type":"Quantitative","value":null},{"ID":5,"ID_attribute":4,"attribute":"oussama","type":"Quantitative","value":null}],"GU":null,"GK":null},{"method":"multilinear","active":false,"k":[{"ID":"1","ID_attribute":[0],"attribute":["pieniche"],"value":null},{"ID":"2","ID_attribute":[1],"attribute":["ccxw"],"value":null},{"ID":"3","ID_attribute":[2],"attribute":["mmm"],"value":null},{"ID":"4","ID_attribute":[3],"attribute":["fdsf"],"value":null},{"ID":"5","ID_attribute":[4],"attribute":["oussama"],"value":null},{"ID":"1,2","ID_attribute":[0,1],"attribute":["pieniche","ccxw"],"value":null},{"ID":"1,3","ID_attribute":[0,2],"attribute":["pieniche","mmm"],"value":null},{"ID":"1,4","ID_attribute":[0,3],"attribute":["pieniche","fdsf"],"value":null},{"ID":"1,5","ID_attribute":[0,4],"attribute":["pieniche","oussama"],"value":null},{"ID":"2,3","ID_attribute":[1,2],"attribute":["ccxw","mmm"],"value":null},{"ID":"2,4","ID_attribute":[1,3],"attribute":["ccxw","fdsf"],"value":null},{"ID":"2,5","ID_attribute":[1,4],"attribute":["ccxw","oussama"],"value":null},{"ID":"3,4","ID_attribute":[2,3],"attribute":["mmm","fdsf"],"value":null},{"ID":"3,5","ID_attribute":[2,4],"attribute":["mmm","oussama"],"value":null},{"ID":"4,5","ID_attribute":[3,4],"attribute":["fdsf","oussama"],"value":null},{"ID":"1,2,3","ID_attribute":[0,1,2],"attribute":["pieniche","ccxw","mmm"],"value":null},{"ID":"1,2,4","ID_attribute":[0,1,3],"attribute":["pieniche","ccxw","fdsf"],"value":null},{"ID":"1,2,5","ID_attribute":[0,1,4],"attribute":["pieniche","ccxw","oussama"],"value":null},{"ID":"1,3,4","ID_attribute":[0,2,3],"attribute":["pieniche","mmm","fdsf"],"value":null},{"ID":"1,3,5","ID_attribute":[0,2,4],"attribute":["pieniche","mmm","oussama"],"value":null},{"ID":"1,4,5","ID_attribute":[0,3,4],"attribute":["pieniche","fdsf","oussama"],"value":null},{"ID":"2,3,4","ID_attribute":[1,2,3],"attribute":["ccxw","mmm","fdsf"],"value":null},{"ID":"2,3,5","ID_attribute":[1,2,4],"attribute":["ccxw","mmm","oussama"],"value":null},{"ID":"2,4,5","ID_attribute":[1,3,4],"attribute":["ccxw","fdsf","oussama"],"value":null},{"ID":"3,4,5","ID_attribute":[2,3,4],"attribute":["mmm","fdsf","oussama"],"value":null},{"ID":"1,2,3,4","ID_attribute":[0,1,2,3],"attribute":["pieniche","ccxw","mmm","fdsf"],"value":null},{"ID":"1,2,3,5","ID_attribute":[0,1,2,4],"attribute":["pieniche","ccxw","mmm","oussama"],"value":null},{"ID":"1,2,4,5","ID_attribute":[0,1,3,4],"attribute":["pieniche","ccxw","fdsf","oussama"],"value":null},{"ID":"1,3,4,5","ID_attribute":[0,2,3,4],"attribute":["pieniche","mmm","fdsf","oussama"],"value":null},{"ID":"2,3,4,5","ID_attribute":[1,2,3,4],"attribute":["ccxw","mmm","fdsf","oussama"],"value":null},{"ID":"1,2,3,4,5","ID_attribute":[0,1,2,3,4],"attribute":["pieniche","ccxw","mmm","fdsf","oussama"],"value":null}],"GK":null,"GU":null}],"settings":{"decimals_equations":"2","decimals_dpl":"8","proba_ce":"0.3","proba_le":"0.3","language":"french","display":"trees"}}'

i=0







def scientific_2_float(dico):
    for key in dico.keys():
        dico[key]="{:.8f}".format(float((dico[key])))
        
    return dico

def clean_attribut(dico): #inutile
    L_dico_2_clean_max=["exp","quad","lin","pow","expo-power","log"]
    
    
    for elt in L_dico_2_clean_max:
        if elt in dico["pts"].keys():
            # print(scientific_2_float(dico["pts"][elt]))
            # dico[elt]=scientific_2_float(dico["pts"][elt])
            for key in dico["pts"][elt].keys():
                if dico["pts"][elt][key]<0.01:
                    # dico["pts"][elt][key]=0.01
                    1+1
            
    return dico



def selecteur1(chaine,i):
    
   
    # print("0000000000-------------chaine",[chaine])
    resu=str(chaine)
    
    resu=resu.replace("null","None")
    resu=resu.replace("true","True")
    resu=resu.replace("false","False")
    # resu=resu.replace("e-","")

    # print(resu)

    resu=ast.literal_eval(resu)
    # resu=json.loads(chaine)
    # print()
    # print("0000000000-------------resu",[resu])
    
    total_attributes=resu["attributes"]
    attribute_cible=total_attributes[int(i)]
    resu["attributes"]=[attribute_cible]
    
    resu2=json.dumps(resu)
    # print()
    # print("0000000000-------------resu2",[resu2])
    # print()
    # return resu2
    
    
    return resu2

# print(selecteur1(chainetest8, i))

# {"type": "Quantitative", "name": "fdsf", "unit": "sfdfq", "val_min": 20, "val_med": ["40", "60", "80"], "val_max": 100, "method": "PE", "mode": "Normal", "completed": "False", "checked": True, "questionnaire": {"number": 3, "points": {"40": 0.86, "60": 0.03, "80": 0.96}, "utility": {}}, "fonction": "exponential", "numero": 0, "pts": {"points": [1, 2, 3], "coord": [[40, 0.86], [60, 0.03], [80, 0.96], [20, 0], [100, 1]], "exp": {"a": -2.3732799817152297, "b": 0.008700495775937487, "c": 1.9942400318877038, "r2": 0.3979369604203541}, "quad": {"a": -0.33529411721100444, "b": 4.264705860550222e-05, "c": 0.017617647032660267, "r2": 0.3955224726744976}, "pow": {"a": 0.1641420402642862, "b": 0.6531497900629418, "c": -0.8644074295538738, "r2": 0.4091527624065955}, "log": {"a": 0.8478783340439661, "b": 0.08253642212774154, "c": 1.2806827488076717, "d": -0.9118795333368924, "r2": 0.40447379290518615}, "lin": {"a": 0.0125, "b": -0.25, "r2": 0.38598689282960674}, "expo-power": {"a": -2.6207480786784547, "b": -0.5623134335768297, "c": 0.17974615648554126, "r2": 0.4098663929155476}}}
# {"type":"Quantitative","name":"fdsf","unit":"sfdfq","val_min":20,"val_med":["40","60","80"],"val_max":100,"method":"PE","mode":"Normal","completed":"False","checked":True,"questionnaire":{"number":3,"points":{"40":0.86,"60":0.03,"80":0.96},"utility":{}},"fonction":"exponential","numero":0,"pts":{"points":[1,2,3],"coord":[[40,0.86],[60,0.03],[80,0.96],[20,0],[100,1]],"exp":{"a":-2.3732799817152297,"b":0.008700495775937487,"c":1.9942400318877038,"r2":0.3979369604203541},"quad":{"a":-0.33529411721100444,"b":0.00004264705860550222,"c":0.017617647032660267,"r2":0.3955224726744976},"pow":{"a":0.1641420402642862,"b":0.6531497900629418,"c":-0.8644074295538738,"r2":0.4091527624065955},"log":{"a":0.8478783340439661,"b":0.08253642212774154,"c":1.2806827488076717,"d":-0.9118795333368924,"r2":0.40447379290518615},"lin":{"a":0.0125,"b":-0.25,"r2":0.38598689282960674},"expo-power":{"a":-2.6207480786784547,"b":-0.5623134335768297,"c":0.17974615648554126,"r2":0.4098663929155476}}}


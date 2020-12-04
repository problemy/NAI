#Autorzy:Mateusz Konarzewski i Bartosz Konarzewski
#wykorzystanie logiki rozmytej przy kalkulowaniu zapotrzebowania kalorycznego dla mężczyzn
#na podstawie BMI, aktywności i budowy ciała
#Readme:
# numpy <= 1.19.3
# scikitfuzzy
#
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

bmi = ctrl.Antecedent(np.arange(16, 30, 4), 'bmi')
posture = ctrl.Antecedent(np.array([1.117, 1.171, 1.711]), 'posture')
activity = ctrl.Antecedent(np.array([1.2, 1.375, 1.55, 1.725, 1.9]), 'activity')

calories = ctrl.Consequent(np.arange(0, 8000, 1), 'calories')


bmi.automf(3)
activity.automf(3)
posture.automf(3)

#bmi.view()
# qual_lo = fuzz.trimf(x_qual, [0, 0, 5])
# qual_md = fuzz.trimf(x_qual, [0, 5, 10])
# qual_hi = fuzz.trimf(x_qual, [5, 10, 10])
# serv_lo = fuzz.trimf(x_serv, [0, 0, 5])
# serv_md = fuzz.trimf(x_serv, [0, 5, 10])
# serv_hi = fuzz.trimf(x_serv, [5, 10, 10])


calories['verylow'] = fuzz.trimf(calories.universe, [1200, 1300, 1400])
calories['low'] = fuzz.trimf(calories.universe, [1400, 1500, 1700])
calories['medium'] = fuzz.trimf(calories.universe, [1800, 2500, 3200])
calories['high'] = fuzz.trimf(calories.universe, [3200, 4200, 5000])
calories['veryhigh'] = fuzz.trimf(calories.universe, [5000, 6000, 8000])

rule1 = ctrl.Rule(bmi['poor'] & activity['good'] & posture['poor'], calories['high'])
rule2 = ctrl.Rule(bmi['poor'] & activity['good'] & posture['average'], calories['veryhigh'])
rule3 = ctrl.Rule(bmi['poor'] & activity['good'] & posture['good'], calories['medium'])

rule4 = ctrl.Rule(bmi['average'] & activity['good'] & posture['poor'], calories['high'])
rule5 = ctrl.Rule(bmi['average'] & activity['good'] & posture['average'], calories['veryhigh'])
rule6 = ctrl.Rule(bmi['average'] & activity['good'] & posture['good'], calories['medium'])

rule7 = ctrl.Rule(bmi['good'] & activity['good'] & posture['poor'], calories['medium'])
rule8 = ctrl.Rule(bmi['good'] & activity['good'] & posture['average'], calories['veryhigh'])
rule9 = ctrl.Rule(bmi['good'] & activity['good'] & posture['good'], calories['low'])


rule10 = ctrl.Rule(bmi['poor'] & activity['average'] & posture['poor'], calories['medium'])
rule11 = ctrl.Rule(bmi['poor'] & activity['average'] & posture['average'], calories['high'])
rule12 = ctrl.Rule(bmi['poor'] & activity['average'] & posture['good'], calories['medium'])

rule13 = ctrl.Rule(bmi['average'] & activity['average'] & posture['poor'], calories['high'])
rule14 = ctrl.Rule(bmi['average'] & activity['average'] & posture['average'], calories['veryhigh'])
rule15 = ctrl.Rule(bmi['average'] & activity['average'] & posture['good'], calories['medium'])

rule16 = ctrl.Rule(bmi['good'] & activity['average'] & posture['poor'], calories['medium'])
rule17 = ctrl.Rule(bmi['good'] & activity['average'] & posture['average'], calories['high'])
rule18 = ctrl.Rule(bmi['good'] & activity['average'] & posture['good'], calories['low'])

rule19 = ctrl.Rule(bmi['poor'] & activity['poor'] & posture['poor'], calories['medium'])
rule20 = ctrl.Rule(bmi['poor'] & activity['poor'] & posture['average'], calories['high'])
rule21 = ctrl.Rule(bmi['poor'] & activity['poor'] & posture['good'], calories['low'])

rule22 = ctrl.Rule(bmi['average'] & activity['poor'] & posture['poor'], calories['medium'])
rule23 = ctrl.Rule(bmi['average'] & activity['poor'] & posture['average'], calories['high'])
rule24 = ctrl.Rule(bmi['average'] & activity['poor'] & posture['good'], calories['low'])

rule25 = ctrl.Rule(bmi['good'] & activity['poor'] & posture['poor'], calories['medium'])
rule26 = ctrl.Rule(bmi['good'] & activity['poor'] & posture['average'], calories['high'])
rule27 = ctrl.Rule(bmi['good'] & activity['poor'] & posture['good'], calories['low'])

# rule3 = ctrl.Rule(calories['good'] | quality['good'], tip['high'])
#for antecedent: Available options: 'poor'; 'mediocre'; 'average'; 'decent', or 'good'.



calories_ctrl = ctrl.ControlSystem([rule1, rule2,rule3,rule4,rule5,rule6,rule7,rule8,rule9,rule10,rule11,rule12,rule13,
                                    rule14, rule15,rule16,rule17,rule18,rule19,rule20,rule21,rule22,rule23,rule24,rule25,
                                    rule26,rule27])


calories = ctrl.ControlSystemSimulation(calories_ctrl)


calories.input['bmi'] = 23
# 1.2 do 1.9]
calories.input['activity'] = 1.9

#posture = ekto = 1.117, mezo = 1.171, endo = 1.711
calories.input['posture'] = 1.117

calories.compute()

print(calories.output['calories'])




#literatura:
#https://pl.wikipedia.org/wiki/Typologia_Sheldona - wskaźniki dla postury
#"Design of expert system to determine the proper diet using harmony search method" page 2
# https://iopscience.iop.org/article/10.1088/1742-6596/1402/7/077006/pdf




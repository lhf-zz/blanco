from blanco import *


level_prefix = {
    Level._1ST: "1",
    Level._2ND: "2",
    Level._3RD: "3",
    Level._4RTH: "4",
    Level.INTRO: "I",
    Level.PRIX_ST_GEORGES: "P",
    Level.TRAINING: "T"
}

def test_letter(test):
    return test.id


division_letter = {
    Division._12_AND_UNDER: "J",
    Division._13_AND_OVER:"Y",
    Division.ADULT:"A",
    Division.OPEN:"O",
}


def to_var_name(obj):
    string = "%s" % obj
    if len(string) > 0 and string[0] in ['1', '2', '3', '4']:
        return "_%s" % string.upper().replace(" ", "_")
    return string.upper().replace(" ", "_")


def test_var_name(test):
    return "%s.%s" % (to_var_name(test.level.name),
                      to_var_name(test.id))


for level in [Level._1ST, Level._2ND, Level._3RD, Level._4RTH,
              Level.INTRO, Level.PRIX_ST_GEORGES, Level.TRAINING]:
    for test in level.tests:
        for division in DIVISIONS:
            # print("%s%s%s %s %s" % (level_prefix[level],
            #     test_letter(test), division_letter[division],
            #     division, test))
#intro_c = Class(6, Test(Level.INTRO, "C"), Division._12_AND_UNDER, Ring.ONE)
            letters = "%s%s%s" % (level_prefix[level],
                test_letter(test), division_letter[division])
            test_var = test_var_name(test)
            d_var = to_var_name(division)
            print('%s = Class("%s", Level.%s, Division.%s, Ring.ONE)'
                % (letters, letters, test_var, d_var))
            # print("%s%s%s = Class("%s %s" % (level_prefix[level],
            #     test_letter(test), division_letter[division],
            #     division, test))

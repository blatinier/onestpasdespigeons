import re


CONVERSIONS = {"oz__g": 28.3,
               "kg__g": 1000,
               "lb__oz": 16,
               "lb__g": 16 * 28.3}


def convert_to_grams(qte):
    qte = qte.lower()
    qte = re.sub(r"\s+", "", qte)
    kg_pat = re.match(r'^([\d.,]+)kg$', qte)
    if kg_pat:
        return float(kg_pat.groups()[0]) * CONVERSIONS['kg__g']
    oz_pat = re.match(r'^([\d.,]+)oz$', qte)
    if oz_pat:
        return float(oz_pat.groups()[0]) * CONVERSIONS['oz__g']
    lb_pat = re.match(r'^([\d.,]+)lbs?$', qte)
    if lb_pat:
        return float(lb_pat.groups()[0]) * CONVERSIONS['lb__g']
    g_pat = re.match(r'^([\d.,]+)(g|gr|grammes|gramm|gram|grams)$', qte)
    if g_pat:
        return float(g_pat.groups()[0])
    return ""

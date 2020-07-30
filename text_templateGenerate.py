from string import Template
import json
import re
language = 'en'
phead = {
        'origin': ["#[#set#]story#"],
        'set': "[container:#container#]"
    }
with open('data\word_library.json', 'r') as f:
    data = json.load(fp=f)
database = data
prep_dict_en = {
        "euro": "for",
        "split": "into",
        "divide": "into",
        "share": "with",
        "minute": "in",
        "hour": "in",
    }
prep_dict_nl = {
        "euro": "voor",
        "verdelen": "over",
        "delen": "met",
        "minuten": "in",
        "uur": "in",
    }


def template_decider(facts, l):
    global language
    language = l
    import xlrd
    facts_lib = xlrd.open_workbook("data\Facts_library_" + language + ".xlsx")
    template_sheets = facts_lib.sheets()[5]
    final_template = ""
    for fact in facts:
        template_name = ""
        # if there are adverbials like time, place, pop them into a list to reserve them.
        relation = fact['relation']
        entities = fact['entities']
        location_list = []
        for item in entities:
            if 'location' in str(item) or (
                    'there' in relation and 'container' in str(item) and '#location#' not in entities and len(entities)>2):
                location_list.append(item)
        # print(location_list)
        for item in location_list:
            entities.remove(item)
        # print("entities: ", entities)
        if 'Unknown' not in fact:
            if 'there' in relation:
                template_name = 'there'
                if len(entities) > 3:
                    template_name = 'there2'
            elif len(entities) == 3:
                template_name = 'srno'
            elif len(entities) == 4:
                if 'character' in entities[0] and 'character' in entities[1]:
                    template_name = 'srino'
                elif 'character' in entities[0]:
                    template_name = 'srdocno'
                elif 'character' not in entities[0]:
                    template_name = 'dosrno'
            elif len(entities) == 5:
                template_name = 'srnocno'

        else:
            # ("entities: ", entities)
            unknown_entity = fact['Unknown']
            entities.remove(unknown_entity)
            if len(entities) > 1:
                entities[0], entities[1] = entities[1], entities[0]
            if 'more' in relation:
                template_name = 'compare'
            elif len(entities) == 2:
                template_name = 'whsvo'
                if any('euro' in e for e in entities):
                    template_name = 'whsv'
                    entities.reverse()
                if any('distance' in e for e in entities):
                    template_name = 'whsv_distance'
                    entities.reverse()
            elif len(entities) == 1 and 'there' in relation:
                template_name = 'whthere'

        template = template_sheets.cell_value(template_sheets.col_values(0).index(template_name), 1)
        # print(template)
        prep_dict = eval('prep_dict_' + language)
        d = {'relation': relation, 'det': '$det', 'prep': '$prep'}
        if '$prep' in template:
            if relation in prep_dict.keys():
                d['prep'] = prep_dict[relation]
            for e in entities:
                if e in prep_dict.keys():
                    d['prep'] = prep_dict[e]

        i = 0
        for item in template.split(" "):
            if '$' in item and item not in ['$relation', '$det', '$prep']:
                d[item.strip('$')] = entities[i]
                i += 1
        template = Template(template)
        # print(d)
        final_template += template.substitute(d)

        # Add adverbials
        if len(location_list) == 1:
            final_template = final_template + ' in the ' + location_list[0]
        elif len(location_list) == 2:
            final_template = final_template + ' from ' + location_list[0] + ' to ' + location_list[1]
        if 'Unknown' not in fact:
            final_template += '. '
        else:
            final_template += ''

    return final_template


def set_theme(head, theme):
    s = ""
    if theme == 'N':
        s = "[#Normal_theme#]"
    elif theme == 'F':
        s = "[#Fiction_theme#]"
    elif theme == 'M':
        s = "[#Movie_theme#]"
    elif theme == 'C':
        s = "[#Cartoon_theme#]"
    str_list = list(head['origin'][0])
    str_list.insert(1, s)
    head['origin'][0] = "".join(str_list)












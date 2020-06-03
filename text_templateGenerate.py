from string import Template
import json
import re

phead = {
        'origin': ["#[#set#]story#"],
        'set': "[container:#container#][currency:#currency#]"
    }
with open('data\word_library.json', 'r') as f:
    data = json.load(fp=f)
database = data

class TextTemplateGenerator(object):

    def __init__(self, facts):
        self.facts = facts
        self.template = ""

    def srno_template(self, relation, entities):
        template_srno = Template('$subject $relation $nummod ${object}')
        d = {'subject': entities[0], 'relation': relation, 'nummod': entities[1], 'object': entities[2]}
        self.template += template_srno.substitute(d)

    def srino_template(self, relation, entities):
        # iobj: indirect object
        template_srino = Template('$subject $relation $iobj $nummod ${object}')
        d = {'subject': entities[0], 'relation': relation, 'iobj': entities[1], 'nummod': entities[2], 'object': entities[3]}
        self.template += template_srino.substitute(d)

    def srdocno_template(self, relation, entities):
        # subject-relation-det-obj-case-num-obj
        template_srdocno = Template('$subject $relation $det $object $prep $nummod $unit')

        d = {'subject': entities[0], 'relation': relation, 'object': entities[1], 'nummod': entities[2],
             'unit': entities[3],'det':"the", 'prep': get_prep(re.sub('[^a-zA-Z]','',relation))}
        self.template += template_srdocno.substitute(d)

    def there_template(self, relation, entities):
        # there are x objects (and y objects...)
        template_there = 'There are $nummod1 $object1'
        d = {'nummod1': entities[0], 'object1': entities[1]}
        if len(entities) > 3:
            template_there += ' and $nummod2 $object2'
            d['nummod2'] = entities[2]
            d['object2'] = entities[3]

        template_there = Template(template_there)
        self.template += template_there.substitute(d)


    def whsvo_template(self, relation, entities):
        # WHNP
        cop_list = ['is', 'are', 'was', 'were']
        non_countable = ['#liquid#', '#currency#']
        template_whsvo = Template('How many $object does $subject $relation')
        for cop in cop_list:
            if cop in relation:
                template_whsvo = Template('How many $object $relation $location')
                break
        if 'currency' in entities[len(entities)-1]:
            template_whsvo = Template('How much does $subject $relation')
        if 'distance' in entities[len(entities)-1]:
            template_whsvo = Template('How long does $subject $relation')

        d = {'subject': entities[0], 'object': entities[1], 'location': entities[0], 'relation': relation}
        self.template += template_whsvo.substitute(d)
        # if 'have' in relation:
        #     self.template += ' now'
        # else:
        #     self.template += ' in total'

    def compare_template(self, entities):
        template_whthere = Template('How many more $object does $subject1 have than $subject2')
        d = {'subject1': entities[0], 'subject2': entities[1], 'object': entities[2]}
        self.template += template_whthere.substitute(d)

    def whthere_template(self, entities):
        template_whthere = Template('How many $object are there')
        d = {'object': entities[0]}
        self.template += template_whthere.substitute(d)

    def decider(self):
        cop_list = ['is', 'are', 'was', 'were']
        non_countable_list = ['#liquid#', '#currency#']
        divide_list = ['share', 'split']
        for fact in self.facts:
            # if there are adverbials like time, place, pop them into a list to reserve them.
            relation = fact['relation']
            entities = fact['entities']
            location_list = []
            for item in entities:
                if 'location' in str(item) or ('there' in relation and 'container' in str(item) and '#location#' not in entities):
                    location_list.append(item)
            # print(location_list)
            for item in location_list:
                entities.remove(item)
            # print("entities: ", entities)
            if 'Unknown' not in fact:
                if 'there' in relation:
                    self.there_template(relation, entities)
                elif len(entities) == 3:
                    self.srno_template(relation, entities)
                elif len(entities) == 4:
                    if 'character' in entities[1]:
                        self.srino_template(relation, entities)
                    if 'object' in entities[1]:
                        self.srdocno_template(relation, entities)


            else:
                # ("entities: ", entities)
                unknown_entity = fact['Unknown']
                entities.remove(unknown_entity)
                if 'more' in relation:
                    self.compare_template(entities)
                elif len(entities) == 2:
                    self.whsvo_template(relation, entities)
                elif len(entities) == 1 and 'there' in relation:
                    self.whthere_template(entities)
                # self.template += ' in total'

            # Add adverbials
            if len(location_list) == 1:
                self.template = self.template + ' in the ' + location_list[0]
            elif len(location_list) == 2:
                self.template = self.template + ' from ' + location_list[0] + ' to ' + location_list[1]
            if relation in divide_list:
                self.template += ' evenly'
            if 'Unknown' not in fact:
                self.template += '. '
            else:
                self.template += ''

        return self.template


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

def get_prep(relation_word):
    from TemplateA import w2v
    prep_list = ["for", "to", "with"]
    prep_dict = {
        "bought": "for",
        "split": "to",
        "share": "with",
    }
    final_prep = prep_dict[relation_word]
    return final_prep










Attributes in facts_library include:
-Facts_set_index: 
	index of a facts set, each facts set include several facts, which are combined to composite a whole text question.

-Fact index: 
	index of each fact in a facts set.

-Entities:
	-Relation_word: 
		normally is the verb in a sentence. The word should be written in specified language (original c). Note: Relation words with '_' inside such as "there_are" and "have_more" are not language-dependent, please keep it in English version.
	-Other Entities: 
		normally are  the subjects, objects, numbers, and modify words. If you want to retrieve a random word from a general category then put the hashtag on both sides. Numbers should be written as "operands[i]", representing ith operand in the related math expression.

-Unknown_entity:
	If you want to design a fact for a question, where the answer is one of the entities. e.g. How many apples do you have? then the Unknown_entity should be the number of apples. Thus, choose the related unknown entity and put it in here. Or leave it for blank to keep the sentence to be a statement. 

-End_word:
	The generated question will end up with a certain phrase in this cell. Or you can leave it for blank. Notice: The end word won't be automatically changed to another language in the system. If you want to generate question in Dutch version, please manully design the end word  in Dutch here.

///////////////////////////////////////////////////////////////

If you want to build a facts_library in another language version, you should follow the rules:
- Translate the items highlighted with yellow
- The word with hashtag '#' shouldn't be modified, which will be replaced by the generator
- When translate the language structure, the word with '$' should be preserved, and put them in the right location in the new language structure.
- All of the entities should be in its original form without plurals or special tense. The system will add plural / 3rd single/ etc automatically using NLP tools.
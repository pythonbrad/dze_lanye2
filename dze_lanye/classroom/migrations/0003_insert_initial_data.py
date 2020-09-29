from django.db import migrations
from data_lang.word import dict_word
import random

def get_random_color():
	return '#'+''.join(random.choices(['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f'], k=6))

def add_datas(apps, schema_editor):
	User = apps.get_model('classroom', 'User')
	Subject = apps.get_model('classroom', 'Subject')
	Quiz = apps.get_model('classroom', 'Quiz')
	Question = apps.get_model('classroom', 'Question')
	Answer = apps.get_model('classroom', 'Answer')

	owner = User(username='generator')
	owner.save()

	for lang in dict_word:
		subject = Subject(name=lang.capitalize(), color=get_random_color())
		subject.save()

		for theme in dict_word[lang]:
			quiz = Quiz(owner=owner, name=theme.capitalize(), subject=subject)
			quiz.save()

			for question_id in dict_word[lang][theme]['mlang']:
				question = Question(quiz=quiz, text=dict_word[lang][theme]['mlang'][question_id].capitalize())
				question.save()

				temp = random.choices([i for i in dict_word[lang][theme]['lang']], k=10)
				choice_ids = []
				[choice_ids.append(choice_id) for choice_id in temp if not choice_id in choice_ids and choice_id != question_id]

				for choice_id in choice_ids[:4]:
					Answer.objects.create(question=question, text=dict_word[lang][theme]['lang'][choice_id].capitalize())
				Answer.objects.create(question=question, text=dict_word[lang][theme]['lang'][question_id].capitalize(), is_correct=True)

class Migration(migrations.Migration):

	dependencies = [
		('classroom', '0002_create_initial_subjects'),
	]

	operations = [
		migrations.RunPython(add_datas),
	]

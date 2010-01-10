from django.db import models
from hashlib import md5, sha256
from utils import retrieve_textcaptcha
import logging


class QuestionManager(models.Manager):
    
    def valid_captcha_response(self, hash, answer):
        """Check for a valid text-CAPTCHA response

        Returns one of the following statuses:
        
        * None - The question hash does not exist
        * False - The answer was incorrect
        * True - The answer was correct
        """

        # The question must exist
        try:
            question = Question.objects.get(hash=hash)
        
        except Question.DoesNotExist:
            return None

        # Now we need to check the answer
        return question.answer_is_correct(answer), question

    def new_captcha(self):
        """Creates and, or, returns a question"""

        question, answers = retrieve_textcaptcha()
        hash = sha256(question).hexdigest()

        try:
            new_question = Question.objects.get(hash=hash)
            logging.debug("Question exists. Skipping '%s'" % new_question.question)
        
        except Question.DoesNotExist:
            # So now we can create it
            logging.debug("Creating new question '%s'" % question)
            new_question = Question.objects.create(
                question=question,
                hash=hash,
                )

            for answer in answers:
                new_answer = Answer.objects.create(
                    question=new_question,
                    hash=answer)
            
        return new_question


class Question(models.Model):

    question = models.TextField()
    hash = models.CharField(max_length=64,
        db_index=True,
        unique=True,
        help_text='The SHA256 hash of the question')

    # Managers
    objects = QuestionManager()

    def __unicode__(self):
        return self.question

    #def salted_hash(self, salt):
    #    hash = md5(self.hash)
    #    hash.update(salt)
    #    return hash.hexdigest()

    def answer_is_correct(self, given_answer):
        hash = md5(given_answer.strip().lower()).hexdigest()
        return hash in [each.hash for each in self.answer_set.all()]

class Answer(models.Model):
    question = models.ForeignKey(Question)
    hash = models.CharField(max_length=32, db_index=True,
        help_text='The MD5 hash of a correct answer')

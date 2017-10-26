from django.db import models
from apps.login_app.models import User, UserManager
import datetime

class TaskManager(models.Manager):
    def validate_create(self, post_data, user_id):
        print("===================VALIDATING CREATING TASK===================")
        print(post_data)
        errors = []
        if len(post_data['time']) < 0 or len(post_data['task']) < 0:
            errors.append('All fields must be completed')

        # if post_data['date'] < datetime.datetime.now:
        #     error.append("The past is gone! Set date for the future :)...")

        if not errors:
            new_task = Task.objects.create(task=post_data['task'], user=User.objects.get(id=user_id),
                                            status=post_data['status'], date=post_data['date'], 
                                            time=post_data['time'])
            print(new_task)
            return new_task
        print(errors)
        return errors
    def validate_update(self, post_data, user_id):
        print("===================VALIDATING CREATING TASK===================")
        print(post_data)
        errors = []
        if len(post_data['task']) < 0 or len(post_data['date']) < 0:
            errors.append('All fields must be completed')
        if not post_data['date'] or post_data['time']:
            errors.append('Date and Time must be completed')

        # if datetime.datetime.strptime(post_data['date'], '%Y-%m-%d') < datetime.datetime.now:
        #     errors.append("The past is gone! Set date for the future :)...")

        if not errors:
            
            updated_task = Task.objects.update(task=post_data['task'], user=User.objects.get(user_id),
                                            status=post_data['status'], date=post_data['date'], 
                                            time=post_data['time'])
            print(updated_task)
            return updated_task
        print(errors)
        return errors



class Task(models.Model):
    task = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='books')
    status = models.CharField(max_length=10, default='Pending')
    date = models.DateField()
    time = models.TimeField(default=datetime.time(12, 00))
    objects = TaskManager()




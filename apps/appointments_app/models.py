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
            user = User.objects.get(id=user_id)
            new_task = Task.objects.create(task=post_data['task'], user=user,
                                            status=post_data['status'], date=post_data['date'], 
                                            time=post_data['time'])
            print(new_task)
            return new_task
        print(errors)
        return errors
    def validate_update(self, post_data, user_id, task_id):
        print("===================VALIDATING CREATING TASK===================")
        print(post_data)
        errors = []
        if len(post_data['task']) < 0 or len(post_data['date']) < 0:
            errors.append('All fields must be completed')
        if post_data['date'] == '' or post_data['time'] == '':
            errors.append('Date and Time must be completed')
        
        if post_data['time'] == '' or datetime.datetime.strptime(post_data['date'], '%Y-%m-%d') < datetime.datetime.now():
            errors.append("The past is gone! Set date for the future :)...")

        if len(errors) == 0:
            update = Task.objects.get(id=task_id)
            update.task = post_data['task']
            update.status = post_data['status']
            update.date = post_data['date']
            update.time = post_data['time']
            update.save()

            print('updated task: {}'.format(update))
            return update

        print(errors)
        return errors



class Task(models.Model):
    task = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='personal_tasks')
    status = models.CharField(max_length=10, default='Pending')
    date = models.DateField()
    time = models.TimeField(default=datetime.time(12, 00))
    objects = TaskManager()

    def __repr__(self):
        return "<APPOINTMENT object: {} {} {} {} {}>".format(self.task, self.date, self.status, self.user)




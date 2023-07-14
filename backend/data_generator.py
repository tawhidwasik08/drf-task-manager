from task_management_system import asgi

from core.models import UserProfile
from faker import Faker
from task_manager.models import Task, TaskComment
import random
from random import choice
from random import choices

def create_superuser():
    fake = Faker()
    username = "su_admin_01"
    email = "suadmin@test.com"
    password = "12345"

    # Create superuser
    UserProfile.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )

    print("Superuser created:")
    print(f"Username: {username}")
    print(f"Email: {email}")
    print(f"Password: {password}")


def generate_fake_users(num_users):
    fake = Faker()
    roles = ['admin', 'manager', 'team_member']
    weights = [2, 5, 10] 
    admin_ids = []
    manager_ids = []
    team_member_ids = []

    for _ in range(num_users):
        username = fake.user_name()
        email = fake.email()
        password = fake.password()
        role = choices(roles, weights)[0]
        user = UserProfile.objects.create_user(username=username, email=email, role=role, password=password)

    print(f"{num_users} users generated.")

    return None

def generate_tasks(num_tasks):
    task_ids = []
    priority_choices = [1, 2, 3]
    fake = Faker()
    for _ in range(num_tasks):
    
        task_name = fake.word()
        task_description = fake.text()
        task_due_date = fake.future_date()
        task_creator_id = choice(UserProfile.objects.filter(role__in=['admin', 'manager']).values_list('id', flat=True))
        num_assignees = random.randint(0, UserProfile.objects.filter(role='team_member').count())
        task_assignee_ids = random.sample(list(UserProfile.objects.filter(role='team_member').values_list('id', flat=True)), num_assignees)
        priority = choice(priority_choices)
        completed = fake.boolean(chance_of_getting_true=50)
                                
        task = Task.objects.create(
            task_name=task_name,
            task_description=task_description,
            task_due_date=task_due_date,
            task_creator_id=task_creator_id,
            priority=priority,
            completed=completed
        )
        task.task_assignee.set(task_assignee_ids)
        task_ids.append(task.task_id)
    print(f"{num_tasks} tasks generated.")

    return None


def generate_task_comments(num_comments):
    fake = Faker()
    for _ in range(num_comments):
        task_id = choice(Task.objects.values_list('task_id', flat=True))
        task = Task.objects.get(task_id=task_id)
        users = list(task.task_assignee.values_list('id', flat=True))
        users.append(task.task_creator.id)
        user = choice(users)
        
        comment_text = fake.text()

        task_comment = TaskComment(
            task_id=task,
            comment_creator=UserProfile.objects.get(id=user),
            comment=comment_text
        )
        task_comment.save()
        

    print(f"{num_comments} task comments generated.")

    return None



generate_fake_users(10)
generate_tasks(20)
generate_task_comments(50)

# create_superuser()
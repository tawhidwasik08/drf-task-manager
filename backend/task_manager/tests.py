from core.models import UserProfile
from . models import Task, TaskComment
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
import json
from rest_framework.authtoken.models import Token

class TaskTestCase(APITestCase):
    """
    Test suite for Task Api
    """
    def setUp(self):
        self.client = APIClient()
        self.url = "/tasks/"

        # admin user creation
        admin_user = UserProfile.objects.create_user(username='admin_1', email = "admin_1@wow.com", password='admin_password', role="admin")
        admin_user.save()
        self.admin_user_id = admin_user.id
        self.admin_token = Token.objects.get(user=admin_user)

        # manager user creation
        manager_user = UserProfile.objects.create_user(username='manager_1', email = "manager@wow.com", password='manager_password', role="manager")
        manager_user.save()
        self.manager_user_id = manager_user.id
        self.manager_token = Token.objects.get(user=manager_user)

        # normal user creation
        member_user = UserProfile.objects.create_user(username='member_1', email = "member_1@wow.com", password='member_password', role="team_member")
        member_user.save()
        self.member_user_id = member_user.id
        self.member_token = Token.objects.get(user=member_user)

        # task data
        self.valid_task_data = {
            "task_name": "test_task_1",
            "task_description": "test_description",
            "task_due_date": "2025-12-12",
            "task_assignee": [self.manager_user_id, self.member_user_id],
            "priority": 1,
            "completed": False,
            }

    def test_create_task(self):
        '''
        Success: Test successful creation of a task by manager
        '''
        data = json.dumps(self.valid_task_data)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.manager_token.key)
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().task_name, "test_task_1")
    
    def test_create_task_without_task_name(self):
        '''
        Error: Test successful creation of a task by manager without task name
        '''
        self.valid_task_data.pop("task_name")
        data = json.dumps(self.valid_task_data)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.manager_token.key)
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_task_without_optional_fields(self):
        '''
        Success: Test successful creation of a task by manager without all optional fields
        '''
        self.valid_task_data.pop("task_description")
        self.valid_task_data.pop("task_due_date")
        self.valid_task_data.pop("task_assignee")
        self.valid_task_data.pop("priority")
        self.valid_task_data.pop("completed")
        data = json.dumps(self.valid_task_data)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.manager_token.key)
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
    
    def test_get_task_with_id(self):
        """
        Success: Test successful retrieval of the task by its id
        """

        # insert one task
        data = json.dumps(self.valid_task_data)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.manager_token.key)
        response = self.client.post(self.url, data, content_type='application/json')
        created_task_id = response.json()['data']['created_task']['task_id']

        # get task by id
        response = self.client.get(self.url+f'{created_task_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['data']['attributes']['task_id'], created_task_id)

    def test_get_all_tasks(self):
        """
        Success: Test successful retrieval of the all thet tasks by admin
        """

        # create 5 tasks
        for i in range(5):
            data = json.dumps(self.valid_task_data)
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.manager_token.key)
            response = self.client.post(self.url, data, content_type='application/json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # get all the tasks, passing admin token, the creator manager would also work
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['data']), 5)

    def test_update_task_with_valid_data(self):
        """
        Success: Test updating a task with valid data
        """
        
        # Create a task
        data = json.dumps(self.valid_task_data)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.manager_token.key)
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get the task ID
        created_task_id = response.json()['data']['created_task']['task_id']

        # Update the task with valid data
        updated_data = {
            "task_name": "updated_task",
            "task_description": "updated_description",
            "task_due_date": "2023-12-31",
            "task_assignee": [self.member_user_id],
            "priority": 2,
            "completed": True,
        }
        updated_data = json.dumps(updated_data)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.manager_token.key)
        response = self.client.patch(f"{self.url}{created_task_id}/", updated_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify that the task has been updated
        self.assertEqual(response.json()['data']['updated_task']['task_name'], "updated_task")
        self.assertEqual(response.json()['data']['updated_task']['task_description'], "updated_description")
        self.assertEqual(response.json()['data']['updated_task']['task_due_date'], "2023-12-31")
        self.assertEqual(response.json()['data']['updated_task']['task_assignee'], [self.member_user_id])
        self.assertEqual(response.json()['data']['updated_task']['priority'], 2)
        self.assertEqual(response.json()['data']['updated_task']['completed'], True)
        
    def test_update_task_with_invalid_data(self):
        """
        Error: Test updating a task with invalid data
        """

        # Create a task
        data = json.dumps(self.valid_task_data)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.manager_token.key)
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get the task ID
        created_task_id = response.json()['data']['created_task']['task_id']

        # Update the task with invalid data
        invalid_data = {
            "task_name": "",
            "task_description": "updated_description",
            "task_due_date": "2023-12-31",
            "task_assignee": [self.member_user_id],
            "priority": 2,
            "completed": "True",
        }
        invalid_data = json.dumps(invalid_data)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.manager_token.key)
        response = self.client.patch(f"{self.url}{created_task_id}/", invalid_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Update the task with another invalid data
        invalid_data = {
            "task_name": "",
            "task_description": "updated_description",
            "task_due_date": "2023-12-31",
            "task_assignee": [100],
            "priority": 2,
            "completed": "True",
        }
        invalid_data = json.dumps(invalid_data)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.manager_token.key)
        response = self.client.patch(f"{self.url}{created_task_id}/", invalid_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_task(self):
        """
        Success: Test successful deletion of a task
        """

        # Create a task
        data = json.dumps(self.valid_task_data)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.manager_token.key)
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Get the ID of the created task
        created_task_id = response.json()['data']['created_task']['task_id']

        # Delete the task
        delete_url = f"{self.url}{created_task_id}/"
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.manager_token.key)
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check deletion by getting by id
        response = self.client.get(self.url+f'{created_task_id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_task_due_date_not_invalid(self):
        """
        Edge: Test that task due date is not set before the creation date
        """
        self.valid_task_data['task_due_date'] = str((timezone.now() - timedelta(days=1)).date())
        data = json.dumps(self.valid_task_data)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.manager_token.key)
        response = self.client.post(self.url, data, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_task_name_max_length(self):
        """
        Edge: Test that task name field has a maximum character limit
        """

        # Create a task with a name that exceeds the maximum character limit
        self.valid_task_data['task_name'] = 'A' * 201
        data = json.dumps(self.valid_task_data)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.manager_token.key)
        response = self.client.post(self.url, data, content_type='application/json')

        # Verify that the response returns a validation error
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TaskCommentTestCase(APITestCase):
    """
    Test suite for Task Comment Api
    """
    def setUp(self):
        self.client = APIClient()
        self.url = "/task-comments/"

        # admin user creation
        admin_user = UserProfile.objects.create_user(username='admin_1', email = "admin_1@wow.com", password='admin_password', role="admin")
        admin_user.save()
        self.admin_user_id = admin_user.id
        self.admin_token = Token.objects.get(user=admin_user)

        # manager user creation
        manager_user = UserProfile.objects.create_user(username='manager_1', email = "manager@wow.com", password='manager_password', role="manager")
        manager_user.save()
        self.manager_user_id = manager_user.id
        self.manager_token = Token.objects.get(user=manager_user)

        # normal user creation
        member_user = UserProfile.objects.create_user(username='member_1', email = "member_1@wow.com", password='member_password', role="team_member")
        member_user.save()
        self.member_user_id = member_user.id
        self.member_token = Token.objects.get(user=member_user)

        # create a task
        test_task = Task.objects.create(task_name='test_task_1', task_description = "test_description",
                                        task_creator = manager_user, task_due_date='2025-12-12', priority=1, completed=False)
        test_task.task_assignee.set([self.manager_user_id, self.member_user_id])
        test_task.save()
        self.test_task_id = test_task.task_id

        # valid comment data
        self.valid_task_comment_data = {
            "task_id": test_task.task_id,
            "comment": "test comment"
            }
        
    def test_create_task_comment(self):
        '''
        Success: Test successful creation of a task by manager
        '''
        data = json.dumps(self.valid_task_comment_data)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.member_token.key)
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TaskComment.objects.count(), 1)
        self.assertEqual(TaskComment.objects.get().comment, "test comment")

    def test_update_task_comment(self):
        """
        Success: Test successful update of a task comment by the comment creator
        """
        # Create a task comment
        data = json.dumps(self.valid_task_comment_data)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.member_token.key)
        response = self.client.post(self.url, data, content_type='application/json')
        created_comment_id = response.json()['data']['created_task_comment']['comment_id']
        
        # Update the task comment
        updated_data = {
            "comment": "updated comment"
        }
        url = f"{self.url}{created_comment_id}/"
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.member_token.key)
        response = self.client.patch(url, data=json.dumps(updated_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['data']['attributes']['comment'], "updated comment")
    
    def test_delete_task_comment(self):
        """
        Success: Test successful deletion of a task comment by the comment creator
        """
        # Create a task comment
        data = json.dumps(self.valid_task_comment_data)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.member_token.key)
        response = self.client.post(self.url, data, content_type='application/json')
        created_comment_id = response.json()['data']['created_task_comment']['comment_id']
        
        # Delete the task comment
        url = f"{self.url}{created_comment_id}/"
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.member_token.key)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(TaskComment.objects.count(), 0)

    def test_delete_task_comment_by_invalid_user(self):
        """
        Error: Test deletion of a task comment by not the original comment creator
        """
        # Create a task comment by a  member
        data = json.dumps(self.valid_task_comment_data)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.member_token.key)
        response = self.client.post(self.url, data, content_type='application/json')
        created_comment_id = response.json()['data']['created_task_comment']['comment_id']
        
        # Delete the task comment by a manager 
        url = f"{self.url}{created_comment_id}/"
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.manager_token.key)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_task_comment_for_non_existing_task(self):
        '''
        Error: Test creation of a task comment for a task that is non-existent
        '''
        invalid_data = self.valid_task_comment_data
        invalid_data["task_id"] = 1000
        data = json.dumps(invalid_data)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.member_token.key)
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_task_comment_with_id(self):
        """
        Success: Test successful retrieval of the task_comment by its id
        """
        # Create a task comment
        data = json.dumps(self.valid_task_comment_data)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.member_token.key)
        response = self.client.post(self.url, data, content_type='application/json')
        created_comment_id = response.json()['data']['created_task_comment']['comment_id']

        # get task by id
        response = self.client.get(self.url+f'{created_comment_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['data']['attributes']['comment_id'], created_comment_id)

    def test_get_all_task_comments(self):
        """
        Success: Test successful retrieval of the all the task_comments by admin
        """

        # create 5 task comments
        for i in range(5):
            data = json.dumps(self.valid_task_comment_data)
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.manager_token.key)
            response = self.client.post(self.url, data, content_type='application/json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # get all the tasks, passing admin token, the creator manager would also work
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['data']), 5)

    def test_create_task_comment_with_blank_comment(self):
        '''
        Edge: Test creation of a task comment when comment is blank
        '''
        self.valid_task_comment_data["comment"] = ""
        data = json.dumps(self.valid_task_comment_data)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.member_token.key)
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

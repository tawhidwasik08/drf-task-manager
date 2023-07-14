from . models import UserProfile
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status
import json
from rest_framework.authtoken.models import Token

class UserTestCase(APITestCase):
    """
    Test suite for User Registration
    """
    def setUp(self):
        self.client = APIClient()
        self.data = {
            "username": "test_member1",
            "email": "test_member1@demo.com",
            "role": "team_member",
            "password": "12345"
            }
        self.url = "/users/"

    def test_create_user(self):
        '''
        Success: Test successful creation of a user
        '''
        data = json.dumps(self.data)
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserProfile.objects.count(), 1)
        self.assertEqual(UserProfile.objects.get().username, "test_member1")
    
    def test_create_user_with_different_roles(self):
        '''
        Success: Test successful creation of a user with different roles
        '''
        allowed_roles = ["admin", "manager", "team_member"]
        for role in allowed_roles:
            self.data['role'] = role 
            data = json.dumps(self.data)
            response = self.client.post(self.url, data, content_type='application/json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            user_id = response.json()['data']['created_user']['user_id']
            UserProfile.objects.filter(id=user_id).delete()
    
    def test_create_user_without_required_fields(self):
        '''
        Error: Test create method when username is not in data
        '''
        field_list = ["username", "email", "password", "role"]
        for field in field_list:
            self.data.pop(field)
            data = json.dumps(self.data)
            response = self.client.post(self.url, data, content_type='application/json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_when_email_is_non_email(self):
        '''
        Error: Test create method when email is not email like
        '''
        self.data["email"]="something@wow"
        data = json.dumps(self.data)
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_user_when_required_field_equals_blank(self):
        '''
        Edge: Test create method when username is blank
        '''
        field_list = ["username", "email", "password", "role"]
        for field in field_list:
            self.data[field]=""
            data = json.dumps(self.data)
            response = self.client.post(self.url, data, content_type='application/json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_invalid_data_types(self):
        '''
        Edge: Test create method when data type is invalid
        '''
        self.data["password"] = ["password"]
        data = json.dumps(self.data)
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.data["email"] = True
        data = json.dumps(self.data)
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.data["role"] = 3.14
        data = json.dumps(self.data)
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_users_list(self):
        """
        Success: Test successful retrieval of the list of users (without task information)
        """
        # Create admin user who have permission for viewing all users info
        user = UserProfile.objects.create_user(username='admin_1', email = "admin_1@wow.com", password='admin_password', role="admin")
        user.save()

        # Generate token for the admin
        token = Token.objects.get(user=user)

        # Set the Authorization header with the token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # Create some users
        user1 = UserProfile.objects.create(username="user1", email="user1@example.com", role="team_member")
        user2 = UserProfile.objects.create(username="user2", email="user2@example.com", role="team_member")

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['data']), 3)    
        self.assertEqual(response.json()['data'][1]['attributes']['username'], user1.username)
        self.assertEqual(response.json()['data'][2]['attributes']['username'], user2.username)
    
    def test_get_user_info_by_id(self):
        """
        Success: Test successful retrieval of single user's information by id (without task information)
        """
        # Create admin user who have permission for viewing all users info
        user = UserProfile.objects.create_user(username='admin_1', email = "admin_1@wow.com", password='admin_password', role="admin")
        user.save()

        # Generate token for the admin
        token = Token.objects.get(user=user)

        # Set the Authorization header with the token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # Create some users
        user1 = UserProfile.objects.create(username="user1", email="user1@example.com", role="team_member")
        user2 = UserProfile.objects.create(username="user2", email="user2@example.com", role="team_member")

        response = self.client.get(self.url+f'?id={3}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['data']['attributes']['username'], user2.username)

    def test_permission_error(self):
        """
        Error: Test retrieval of the users information from users without permission (without task information)
        """
        # Create a team_member user
        user = UserProfile.objects.create_user(username='team_member_1', email = "member_1@wow.com", password='password', role="team_member")
        user.save()

        # Generate token for the team_member
        token = Token.objects.get(user=user)

        # Set the Authorization header with the token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # Create some team_member users
        user1 = UserProfile.objects.create(username="user1", email="user1@example.com", role="team_member")
        user2 = UserProfile.objects.create(username="user2", email="user2@example.com", role="team_member")

        response = self.client.get(self.url+f'?id={3}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_found_user_error(self):
        """
        Error: Test retrieval of the non-existent users information(without task information)
        """
        # Create an admin or manager user
        user = UserProfile.objects.create_user(username='admin_1', email = "admin_1@wow.com", password='admin_password', role="admin")
        user.save()

        # Generate token for the user
        token = Token.objects.get(user=user)

        # Set the Authorization header with the token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # Create some users
        user1 = UserProfile.objects.create(username="user1", email="user1@example.com", role="team_member")
        user2 = UserProfile.objects.create(username="user2", email="user2@example.com", role="team_member")

        response = self.client.get(self.url+f'?id={5}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

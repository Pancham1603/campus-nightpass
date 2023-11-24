from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from .models import Student, CustomUser
from .google_config import config
import json
import requests
from urllib.parse import urlencode


def gauth(request):
    # Load configuration from JSON file

    params = {
        'scope': 'profile',
        'access_type': 'offline',
        'prompt': 'consent',
        'include_granted_scopes': 'true',
        'response_type': 'code',
        'state': 'state_parameter_passthrough_value',
        'redirect_uri': config['web']['redirect_uris'][0],
        'client_id': config['web']['client_id'],
    }

    auth_uri = config['web']['auth_uri']
    redirect_url = f"{auth_uri}?{urlencode(params)}"

    # Redirect to the constructed URL
    return HttpResponseRedirect(redirect_url)

def get_google_user_info(access_token):
    # Google userinfo endpoint URL
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"

    # Set up the request headers
    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    # Make a GET request to the userinfo endpoint
    response = requests.get(userinfo_url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse and return the user information
        user_info = response.json()
        return user_info
    else:
        # Print the error message if the request fails
        print(f"Failed to fetch user information. Status code: {response.status_code}")
        return None


def oauth_callback(request):
    # Load configuration from JSON file
    # Check if the 'code' parameter is present in the GET request
    if 'code' in request.GET:
        # Read the code from the GET parameters
        code = request.GET['code']
        # Google OAuth2 token endpoint URL
        token_endpoint = config['web']['token_uri']
        # Your client credentials
        client_id = config['web']['client_id']
        client_secret = config['web']['client_secret']
        redirect_uri = config['web']['redirect_uris'][0]

        # Build the POST data
        post_data = {
            'code': code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code',
        }

        # Make a POST request to the token endpoint
        response = requests.post(token_endpoint, data=post_data)

        # Check if the request was successful
        if response.ok:
            # Save the response to a JSON file
            user_info = get_google_user_info(response.json()['access_token'])
            user_email = user_info['email']
            login(request, user=CustomUser.objects.filter(email=user_email).first())
            return HttpResponseRedirect('/')
        else:
            # Handle the case when the token request fails
            return HttpResponse(f"Error: {response.text}")
    else:
        # Handle the case when 'code' parameter is not present
        return HttpResponse('Error: Authorization code not found in GET parameters.')



@csrf_exempt
def login_user(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            return gauth(request)
        else:
            return render(request=request, template_name='login.html')
    else:
        return redirect('/')


def logout_user(request):
    logout(request)
    return redirect('/login')



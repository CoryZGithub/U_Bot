# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # ...
    path('get_chatgpt_response/', views.get_chatgpt_response, name='get-chatgpt-response'),
    path('end_session/', views.end_session, name='end_session'),
    path('set_initial_prompt/', views.set_initial_prompt, name='set-initial-prompt'),
    path('update-variable/', views.update_variable, name='update_variable')
]

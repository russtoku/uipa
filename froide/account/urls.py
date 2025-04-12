from django.urls import path
from django.urls import re_path

from .views import (
    MyRequestsView,
    FollowingRequestsView,
    CustomPasswordResetConfirmView,
    account_settings,
    new_terms,
    logout,
    login,
    signup,
    confirm,
    send_reset_password_link,
    change_password,
    ##password_reset_confirm,
    change_user,
    change_email,
    go,
    delete_account,
)

urlpatterns = [
    path('', MyRequestsView.as_view(), name='account-show'),
    path('following/', FollowingRequestsView.as_view(), name='account-following'),
    path('settings/', account_settings, name='account-settings'),
    path('terms/', new_terms, name='account-new_terms'),
    path('logout/', logout, name='account-logout'),
    path('login/', login, name='account-login'),
    path('signup/', signup, name='account-signup'),
    path('reset/', send_reset_password_link, name='account-send_reset_password_link'),
    path('change_password/', change_password, name='account-change_password'),
    path('change_user/', change_user, name='account-change_user'),
    path('change-email/', change_email, name='account-change_email'),
    path('delete-account/', delete_account, name='account-delete_account'),
    re_path(r'^confirm/(?P<user_id>\d+)/(?P<secret>\w{32})/$', confirm, name='account-confirm'),
    re_path(r'^confirm/(?P<user_id>\d+)/(?P<request_id>\d+)/(?P<secret>\w{32})/$',
        confirm, name='account-confirm'),
    #url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #    password_reset_confirm, name='account-password_reset_confirm'),
    path(
        "reset/<uidb64>/<token>/",
        CustomPasswordResetConfirmView.as_view(),
        name="account-password_reset_confirm",
    ),
    re_path(r'^go/(?P<user_id>\d+)/(?P<secret>\w{32})(?P<url>/.*)$', go,
        name='account-go'),
]

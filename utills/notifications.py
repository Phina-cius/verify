from django.contrib import messages

class NotificationManager:
    @staticmethod
    def success(request, message_key, **kwargs):
        message_map = {
            'logout_success': 'You have been signed out successfully.',
            'login_success': 'Welcome back! You are now signed in.',
            'profile_updated': 'Your profile has been updated successfully.',
            'password_changed': 'Your password has been changed successfully.',
            'item_created': 'Your item has been created successfully.',
            'item_updated': 'Your item has been updated successfully.',
            'item_deleted': 'Your item has been deleted successfully.',
        }
        messages.success(request, message_map.get(message_key, 'Operation completed successfully.'))

    @staticmethod
    def error(request, message_key, **kwargs):
        message_map = {
            'login_failed': 'Invalid username or password.',
            'permission_denied': 'You do not have permission to perform this action.',
            'form_errors': 'Please correct the errors below.',
        }
        messages.error(request, message_map.get(message_key, 'An error occurred.'))
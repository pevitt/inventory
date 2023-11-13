from django.contrib.auth import get_user_model

class EmailPasswordAuthBackend():
    """
    Authentication using auth user model by email
    """
    def authenticate(
            self,
            email=None,
            password=None
    ):
        UserModel = get_user_model()
        try:
            # UserModel.objects.get(email=email)
            user = UserModel._default_manager.get(email=email)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None

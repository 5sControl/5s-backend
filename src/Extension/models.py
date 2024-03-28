from django.db import models


class ExtensionReport(models.Model):
    text_post = models.TextField()
    text_comment = models.TextField()
    link_author_comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # UserInfo
    about_user = models.TextField()
    about_author = models.TextField()
    user_company = models.CharField(max_length=255, default=None, null=True)
    user_experience = models.CharField(max_length=255)
    user_link = models.TextField(null=True, blank=True)
    user_name = models.CharField(max_length=255)
    user_position = models.CharField(max_length=255)

    # extension user
    extension_user = models.CharField(max_length=255)

    # AI comments
    ai_comments = models.TextField()

    # Projects ID
    project_id = models.CharField(max_length=50)

    def __str__(self):
        return self.project_id

from django.db import models


class SocialPost(models.Model):
    text_post = models.TextField()
    text_comment = models.TextField()
    link_author_comment = models.URLField()

    # UserInfo
    about = models.TextField()
    about_author = models.TextField()
    company = models.CharField(max_length=255)
    experience = models.CharField(max_length=255)
    link = models.URLField()
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)

    # extension user
    extension_user = models.CharField(max_length=255)

    # AI comments
    ai_comments = models.TextField()

    # Projects ID
    project_id = models.CharField(max_length=50)

    def __str__(self):
        return self.project_id

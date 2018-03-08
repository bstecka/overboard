from django.contrib import admin
from .models import Question, Answer, Vote, Tag, QuestionsTag, Notification, User

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Vote)
admin.site.register(Tag)
admin.site.register(QuestionsTag)
admin.site.register(User)
admin.site.register(Notification)

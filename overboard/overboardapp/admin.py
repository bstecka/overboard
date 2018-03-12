from django.contrib import admin
from .models import Question, Answer, Vote, Tag, Notification, UserExtended

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Vote)
admin.site.register(Tag)
admin.site.register(Notification)
admin.site.register(UserExtended)

from django.contrib import admin
from posts.models import Question, Answer, Vote
from users.models import UserExtended
from tags.models import Tag

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Vote)
admin.site.register(Tag)
admin.site.register(UserExtended)

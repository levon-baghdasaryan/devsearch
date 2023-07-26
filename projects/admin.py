from django.contrib import admin

from .models import Project, Review, Tag

# class ProjectAdmin(admin.ModelAdmin):
#     readonly_fields = ('vote_total', 'vote_ratio')

admin.site.register(Project)
admin.site.register(Review)
admin.site.register(Tag)

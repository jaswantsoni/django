from django.contrib import admin
from .models import Genre, Movie, Review

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ('author', 'average_score')
    fields = ('author', 'storyline_score', 'visual_score', 'soundtrack_score', 'average_score', 'is_approved')

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'created_at')
    list_filter = ('genre', 'created_at')
    search_fields = ('title',)
    inlines = [ReviewInline]

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('movie', 'author', 'storyline_score', 'visual_score', 'soundtrack_score', 'average_score', 'is_approved')
    list_editable = ('is_approved',)
    list_filter = ('is_approved', 'movie__genre')

class GenreAdmin(admin.ModelAdmin):
    search_fields = ('name',)

admin.site.register(Genre, GenreAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Review, ReviewAdmin)
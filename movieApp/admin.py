from django.contrib import admin
from .models import Movie, Review, Genre

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'review_count', 'avg_storyline', 'avg_visual', 'avg_soundtrack')
    inlines = [ReviewInline]
    
    def review_count(self, obj):
        return obj.reviews.count()
    
    def avg_storyline(self, obj):
        return obj.average_storyline()
    
    def avg_visual(self, obj):
        return obj.average_visual()
    
    def avg_soundtrack(self, obj):
        return obj.average_soundtrack()

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('movie', 'author', 'average_score', 'is_approved')
    list_editable = ('is_approved',)
    list_filter = ('is_approved', 'movie__genre')

admin.site.register(Movie, MovieAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Genre)
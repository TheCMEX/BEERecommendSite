from django.contrib import admin

from main.models import Beer, Recommendation


class AdminSort (admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    list_filter = ['name', 'id']
    search_fields = ['name', 'id', 'description']

    class Meta:
        model = Beer


admin.site.register(Beer, AdminSort)


class AdminSortMarks(admin.ModelAdmin):
    list_display = ['beer_id', 'mark', 'user_id']
    list_filter = ['mark', 'beer_id']
    search_fields = ['mark', 'beer_id', 'user_id']


admin.site.register(Recommendation, AdminSortMarks)
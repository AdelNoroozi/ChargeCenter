from django.contrib.admin import ModelAdmin


class BaseModelAdmin(ModelAdmin):
    list_display = ["position", "is_active", "created_at", "updated_at"]
    list_editable = ["is_active"]
    list_filter = ["is_active", "created_at", "updated_at"]
    date_hierarchy = "created_at"
    ordering = ["created_at", "updated_at", "position"]

    class Meta:
        abstract = True

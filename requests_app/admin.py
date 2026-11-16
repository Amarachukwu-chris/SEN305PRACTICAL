from django.contrib import admin
from .models import Category, ServiceRequest, WorkOrder, Comment
from django.utils import timezone


class OverdueFilter(admin.SimpleListFilter):
    title = "due status"
    parameter_name = "due_status"

    def lookups(self, request, model_admin):
        return (
            ("overdue", "Overdue"),
            ("not_overdue", "Not overdue"),
        )

    def queryset(self, request, queryset):
        now = timezone.now()

        if self.value() == "overdue":
            return queryset.filter(
                due_at__lt=now,
                status__in=[
                    ServiceRequest.Status.OPEN,
                    ServiceRequest.Status.ASSIGNED,
                    ServiceRequest.Status.IN_PROGRESS,
                ],
            )

        if self.value() == "not_overdue":
            return queryset.filter(due_at__gte=now)

        return queryset

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "requester",
        "category",
        "priority",
        "status",
        "due_at",
        "resolution_summary",
        "created_at",
    )

    list_filter = (
        "status",
        "priority",
        "category",
        OverdueFilter,
    )

    search_fields = (
        "title",
        "description",
        "location",
        "resolution_summary",
    )


@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ("service_request", "technician", "created_at")
    search_fields = ("service_request__title", "technician__username")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("service_request", "author", "is_internal", "created_at")
    list_filter = ("is_internal",)
    search_fields = ("body", "author__username")

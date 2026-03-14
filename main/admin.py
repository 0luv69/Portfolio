from django.contrib import admin
from main.models import Contact, IPAddressInfo
from .models import (
    Technology,
    Project,
    ProjectLink,
    ProjectMedia,
)
from django.utils.html import format_html
# Register your models here.

@admin.register(IPAddressInfo)
class IPAddressInfoAdmin(admin.ModelAdmin):
    list_display = ('contact','ip', 'city', 'country_name', 'created_at')
    search_fields = ('ip', 'city', 'country_name')
    list_filter = ('country_name', 'city')

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)










# -------------------------
# Technology Admin
# -------------------------

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ("logo_thumb", "name", "short_description", "order")
    search_fields = ("name",)
    ordering = ("-order", "name")

    def logo_thumb(self, obj):
        if obj.logo_image:
            return format_html(
                '<img src="{}" style="width:40px; height:40px; object-fit:contain;" />',
                obj.logo_image.url
            )
        return "-"
    logo_thumb.short_description = "Logo"

# -------------------------
# Inline: ProjectLink
# -------------------------

class ProjectLinkInline(admin.TabularInline):
    model = ProjectLink
    extra = 1
    fields = (
        "link_type",
        "label",
        "url",
        "sort_order",
    )
    ordering = ("sort_order",)


# -------------------------
# Inline: ProjectMedia
# -------------------------

class ProjectMediaInline(admin.TabularInline):
    model = ProjectMedia
    extra = 1
    fields = (
        "media_type",
        "image",
        "file",
        "external_url",
        "alt_text",
        "caption",
        "sort_order",
    )
    ordering = ("sort_order",)


# -------------------------
# Project Admin
# -------------------------

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "featured",
        "is_published",
        "sort_order",
        "created_at",
    )

    list_filter = (
        "featured",
        "is_published",
        "technologies",
        "created_at",
    )

    search_fields = (
        "title",
        "short_summary",
        "full_description",
        "slug",
    )

    readonly_fields = (
        "slug",
        "created_at",
        "updated_at",
    )

    ordering = (
        "sort_order",
        "-created_at",
    )

    filter_horizontal = (
        "technologies",
    )

    fieldsets = (

        ("Main Info", {
            "fields": (
                "title",
                "slug",
                "short_summary",
                "full_description",
            )
        }),

        ("Details", {
            "fields": (
                "role",
                "duration",
                "technologies",
            )
        }),

        ("Settings", {
            "fields": (
                "featured",
                "is_published",
                "sort_order",
            )
        }),

        ("Dates", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),

    )

    inlines = [
        ProjectLinkInline,
        ProjectMediaInline,
    ]


# -------------------------
# ProjectLink Admin (optional standalone)
# -------------------------

@admin.register(ProjectLink)
class ProjectLinkAdmin(admin.ModelAdmin):
    list_display = (
        "project",
        "link_type",
        "url",
        "sort_order",
    )

    list_filter = (
        "link_type",
    )

    search_fields = (
        "project__title",
        "url",
    )

    ordering = ("sort_order",)


# -------------------------
# ProjectMedia Admin (optional standalone)
# -------------------------

@admin.register(ProjectMedia)
class ProjectMediaAdmin(admin.ModelAdmin):

    list_display = (
        "project",
        "media_type",
        "sort_order",
    )

    list_filter = (
        "media_type",
    )

    search_fields = (
        "project__title",
        "caption",
    )

    ordering = ("sort_order",)
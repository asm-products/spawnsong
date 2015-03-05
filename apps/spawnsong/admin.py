from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin
from django.contrib import auth
from django.contrib.auth import admin as auth_admin
from django.db.models import Sum
from decimal import Decimal
from django.contrib.admin.filters import SimpleListFilter
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin

from avatar.models import Avatar
from avatar.signals import avatar_updated
from avatar.templatetags.avatar_tags import avatar

from sites.spawnsongsite import admin_site as site
from models import *


class NullFilterSpec(SimpleListFilter):
    title = u''

    parameter_name = u''

    value_label = "Has value"

    no_value_label = "None"

    def lookups(self, request, model_admin):
        return (
            ('1', self.value_label),
            ('0', self.no_value_label)
        )

    def queryset(self, request, queryset):
        kwargs = {
        '%s'%self.parameter_name : None,
        }
        if self.value() == '0':
            return queryset.filter(**kwargs)
        if self.value() == '1':
            return queryset.exclude(**kwargs)
        return queryset

class SnippetInline(admin.StackedInline):
    model = Snippet
    extra = 0
    readonly_fields = ("state",'processing_error')
    raw_id_fields = ("audio",)
    fieldsets = (
       (None, {
           'fields': ('title', 'message', 'state', 'created_at', 'image', 'visualisation_effect','processing_error'),
       }),
       ('Audio Data', {
           'classes': ('collapse',),
           'fields': ('audio',)
       }),
       # ('Echonest', {
       #     'classes': ('collapse',),
       #     'fields': ('echonest_track_profile', 'echonest_track_analysis')
       # }),
    )
    
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
        

class CompletedNullFilterSpec(NullFilterSpec):
    title = u'Completed'
    parameter_name = u'completed_at'
    value_label = "Completed"
    no_value_label = "Not Completed"
    
def retry_processing(modeladmin, request, queryset):
    for snippet in Snippet.objects.filter(state="processing_error", song__in=queryset.all()):
        snippet.process_uploaded_audio()
retry_processing.short_description = "Retry (failed) processing"

class SongAdmin(admin.ModelAdmin):
    inlines = [SnippetInline]
    list_display = ("title", "state", "artist", "completed")
    date_hierarchy = "created_at"
    search_fields = ("snippet__title", "snippet__state", "artist__user__username")
    list_filter = ("snippet__state", CompletedNullFilterSpec)
    actions = [retry_processing]
    raw_id_fields = ("complete_audio",)
    
    fieldsets = (
       (None, {
           'fields': ('artist', 'created_at')
       }),
       ('Completed Song', {
           'fields': ('completed_at', 'complete_audio')
       }),
    )

    def completed(self, obj):
        return obj.is_complete()
    completed.boolean = True
    
    def has_add_permission(self, request):
        return False

    def state(self, obj):
        snippet = obj.snippet_set.first()
        if not snippet: return None
        return snippet.state

class CommentAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
    search_fields = ("snippet__title", "user__username", "content", "ip_address")
    list_display = ("user", "snippet", "content", "created_at", "ip_address", "is_displayed")
    list_filter = ("is_displayed",)
    list_editable = ("is_displayed",)
    ordering = ("-created_at",)

def refund(modeladmin, request, queryset):
    for order in queryset.filter(refunded=False):
        order.refund()
refund.short_description = "Refund selected orders"
    
class OrderAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
    readonly_fields = ("delivered", "refunded","charged", "charge_failed", "charge_error")
    search_fields = ("song__snippet__title", "purchaser_email", "price")
    list_display = ("song", "purchaser_email", "created_at", "price", "refunded", "charged", "charge_failed", "delivered")
    list_filter = ("refunded", "delivered")
    ordering = ("-created_at",)
    actions = [refund]

    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    fieldsets = (
       (None, {
           'fields': ('song', 'price', 'created_at')
       }),
       ('Purchasher', {
           'fields': ('purchaser', 'purchaser_email')
       }),
       ('Order Status', {
           'fields': ('delivered', 'refunded','charged', 'charge_failed')
       }),
       ('Transaction', {
           'classes': ('collapse',),
           'fields': ('charge_error', 'stripe_transaction_id','stripe_customer_id',)
       }),
    )

class OrderInline(admin.StackedInline):
    model = Order
    extra = 0
    
    readonly_fields = ("delivered", "refunded")
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    fieldsets = (
       (None, {
           'fields': ('song', 'price', 'created_at')
       }),
       ('Purchasher', {
           'fields': ('purchaser', 'purchaser_email')
       }),
       ('Order Status', {
           'fields': ('delivered', 'refunded')
       }),
       ('Transaction', {
           'classes': ('collapse',),
           'fields': ('stripe_transaction_id',)
       }),
    )

class ArtistPaymentAdmin(admin.ModelAdmin):
    date_hierarchy = "created_at"
    search_fields = ("artist__user__username", "artist__user__email")
    list_display = ("artist", "created_at", "order_count", "total_amount", "paid", "paid_at")
    list_filter = ("paid",)
    list_editable = ("paid",)
    readonly_fields = ("paid_at",)
    ordering = ("-created_at",)
    inlines = [OrderInline]
    
    def order_count(self, obj):
        return obj.order_set.count()
    
    def total_amount(self, obj):
        return "$%0.2f" % ((obj.order_set.aggregate(Sum('price'))["price__sum"] or 0)/Decimal("100"))

    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False


class AvatarInline(admin.StackedInline):
    model = Avatar
    list_display = ('get_avatar', 'primary', "date_uploaded")
    extra = 0

    def get_avatar(self, avatar_in):
        return avatar(avatar_in.user, settings.AVATAR_SIZE)

    get_avatar.short_description = 'Avatar'
    get_avatar.allow_tags = True

    def save_model(self, request, obj, form, change):
        super(AvatarInline, self).save_model(request, obj, form, change)
        avatar_updated.send(sender=Avatar, user=request.user, avatar=obj)


class UserAdmin(auth_admin.UserAdmin):
    inlines = (AvatarInline,)

    def __init__(self, *args, **kwargs):
        super(UserAdmin, self).__init__(*args, **kwargs)
        self.list_filter += ('date_joined',)
        self.list_display += ('date_joined',)

for _site in [site]:
    _site.register(Song, SongAdmin)
    _site.register(Order, OrderAdmin)
    _site.register(ArtistPayment, ArtistPaymentAdmin)
    _site.register(Comment, CommentAdmin)
    
site.register(auth.models.User, UserAdmin)
site.register(FlatPage, FlatPageAdmin)

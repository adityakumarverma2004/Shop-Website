from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Category, Product, ProductImage, ContactMessage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'delete_button')
    prepopulated_fields = {'slug': ('name',)}

    def delete_button(self, obj):
        url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html(
            '<a class="button" style="background-color: #ba2121; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold; text-decoration: none;" href="{}">Delete</a>',
            url
        )
    delete_button.short_description = 'Action'
    delete_button.allow_tags = True

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    # This prevents the raw images model from cluttering the main index page
    # but still registers it with the admin so the "Delete" URL is valid.
    def get_model_perms(self, request):
        return {}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0 # Keeps it clean, showing only existing images
    can_delete = False # Removes the default delete checkbox
    readonly_fields = ('instant_delete',)

    def instant_delete(self, obj):
        if obj.pk:
            return format_html(
                '<button type="button" class="button instant-delete-btn" data-image-id="{}" style="background-color: #ba2121; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold; border: none; cursor: pointer;">Delete</button>',
                obj.id
            )
        return ""
    instant_delete.short_description = 'Delete'

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class ProductAdminForm(forms.ModelForm):
    # This field allows the user to select multiple files at once
    images_upload = MultipleFileField(
        required=False,
        help_text="Hold Ctrl (Windows) or Command (Mac) to select multiple images at once."
    )

    class Meta:
        model = Product
        fields = '__all__'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ('id', 'title', 'category', 'price', 'carat', 'weight_grams', 'is_featured', 'created_at', 'delete_button')
    list_editable = ('is_featured',)
    list_filter = ('category', 'is_featured')
    search_fields = ('id', 'title', 'description', 'carat')
    inlines = [ProductImageInline]

    class Media:
        js = ('admin/js/instant_delete.js',)

    def save_model(self, request, obj, form, change):
        # Save the Product model first
        super().save_model(request, obj, form, change)
        
        # Then, grab all the files uploaded to our custom 'images_upload' field
        for image_file in request.FILES.getlist('images_upload'):
            # Create a ProductImage for each file
            ProductImage.objects.create(product=obj, image=image_file)

    def delete_button(self, obj):
        url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html(
            '<a class="button" style="background-color: #ba2121; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold; text-decoration: none;" href="{}">Delete</a>',
            url
        )
    delete_button.short_description = 'Action'
    delete_button.allow_tags = True

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'created_at', 'delete_button')
    search_fields = ('name', 'phone', 'message')
    readonly_fields = ('name', 'phone', 'message', 'created_at')
    ordering = ('-created_at',)

    def delete_button(self, obj):
        url = reverse('admin:%s_%s_delete' % (obj._meta.app_label, obj._meta.model_name), args=[obj.id])
        return format_html(
            '<a class="button" style="background-color: #ba2121; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold; text-decoration: none;" href="{}">Delete</a>',
            url
        )
    delete_button.short_description = 'Action'
    delete_button.allow_tags = True

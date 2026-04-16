import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_project.settings')
django.setup()

from admin_interface.models import Theme

def configure_admin_theme():
    # Only create if it doesn't exist, or update the first one
    theme, created = Theme.objects.get_or_create(name='Seth Sanwara Luxury Theme')
    
    # Custom colors to match the storefront
    theme.css_header_background_color = '#111111'
    theme.css_header_link_color = '#e2a77f' # Rose gold
    theme.css_header_link_hover_color = '#ffffff'
    
    theme.css_module_background_color = '#1a1a1a'
    theme.css_module_text_color = '#e2a77f'
    theme.css_module_link_color = '#ffffff'
    theme.css_module_link_hover_color = '#e2a77f'
    
    theme.css_generic_link_color = '#d4af37' # Gold
    theme.css_generic_link_hover_color = '#b08d20'
    
    theme.css_save_button_background_color = '#d4af37'
    theme.css_save_button_background_hover_color = '#b08d20'
    theme.css_save_button_text_color = '#ffffff'
    
    theme.css_delete_button_background_color = '#a00000'
    
    # Typography
    theme.title = "Seth Sanwara Jewellers"
    theme.title_visible = True
    theme.logo_visible = False
    
    # General tweaks
    theme.list_filter_dropdown = True
    theme.recent_actions_visible = True
    
    theme.active = True
    theme.save()
    
    print("Luxury Admin Theme configured successfully!")

if __name__ == '__main__':
    configure_admin_theme()

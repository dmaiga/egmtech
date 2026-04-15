from catalog.models import Category

def categories_processor(request):
    return {
        'nav_categories': Category.objects.filter(is_active=True)
    }
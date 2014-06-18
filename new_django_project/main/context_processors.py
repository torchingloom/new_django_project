
from new_django_project._lib.template_layer_registry import Registry


def registry(request):
    return {
        'registry': Registry(request)
    }

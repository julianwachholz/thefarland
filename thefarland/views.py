from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'

index = IndexView.as_view()


class ContactView(TemplateView):
    template_name = 'contact.html'

contact = ContactView.as_view()

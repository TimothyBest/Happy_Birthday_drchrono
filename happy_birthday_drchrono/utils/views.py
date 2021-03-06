from django.db import connection
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import FormView


def load_template(request, template_name, extra_context=None):
    if not extra_context: extra_context = dict()
    return render(request, template_name, extra_context)

# Mixin to handle multiple form classses
class MultipleFormsView(FormView):
    form_classes = {}
    template_name = None
    success_url = 'home'

    def are_forms_valid(self, forms):
        for key, form in forms.iteritems():
            if not form.is_valid():
                return False
        return True

    def forms_valid(self, forms):
        for key, form in forms.iteritems():
            form.save()
        return self.get_success_url()

    def forms_invalid(self, forms):
        context = self.get_context_data()
        context['next'] = self.request.POST.get('next')
        context.update(forms)
        return render(self.request, self.template_name, context)

    def get(self, request, username=None, **kwargs):
        context = self.get_context_data()
        context.update(self.get_forms())
        # TODO: append next url to response
        return render(request, self.template_name, context=context)

    def get_context_data(self, **kwargs):
        context = super(MultipleFormsView, self).get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next')
        context['request'] = self.request
        return context

    def get_forms(self):
        forms = {}
        initial = self.get_initial_data()
        form_kwargs = self.get_form_kwargs()
        for key, form_class in self.form_classes.iteritems():
            forms[key] = form_class(initial=initial[key], **form_kwargs)
        return forms

    def get_form_kwargs(self):
        kwargs = {}
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_initial_data(self):
        initial = {}
        for key, form_class in self.form_classes.iteritems():
            initial[key] = {}
        return initial

    def get_success_url(self):
        success_url = self.request.POST.get('next', "")
        if success_url and success_url != "None":
            return HttpResponseRedirect(self.request.POST['next'])
        else:
            return redirect(self.success_url)

    def post(self, request, **kwargs):
        forms = self.get_forms()
        if self.are_forms_valid(forms):
            return self.forms_valid(forms)
        else:
            return self.forms_invalid(forms)

class MultipleModelFormsView(MultipleFormsView):
    """ The object coresponding to the form must use the sam key """

    def get_objects(self):
        objects = {}
        for key, form_class in self.form_classes.iteritems():
            objects[key] = None
        return objects

    def get_forms(self):
        forms = {}
        objects = self.get_objects()
        initial = self.get_initial_data()
        form_kwargs = self.get_form_kwargs()
        for key, form_class in self.form_classes.iteritems():
            forms[key] = form_class(instance=objects[key], initial=initial[key], **form_kwargs)
        return forms

def reset():
     cursor = connection.cursor()
     cursor.execute("SELECT setval('location_id_key', (SELECT MAX(id) FROM contact_location)+1)")
     print "success"

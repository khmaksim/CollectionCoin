from django.shortcuts import render, HttpResponse
from django.views.generic import View
from django.template import RequestContext
from django.core.mail import mail_admins, send_mail, BadHeaderError
from .forms import MessageForm


class Messsage(View):
    form_class = MessageForm
    template_name = 'feedback.html'
    user = {}

    def get(self, request):
        message_form = self.form_class(label_suffix='', initial=self.get_user_info(request))
        return render(request, self.template_name, context={'form': message_form})

    def post(self, request):
        sent = False
        message_form = self.form_class(request.POST, label_suffix='')
        if message_form.is_bound and message_form.is_valid():
            message = message_form.save(commit=False)
            message.user = request.user
            message.save()

            message = message_form.cleaned_data['content']
            from_email = message_form.cleaned_data['email']
            try:
                mail_admins('Feedback', message)
                send_mail('Feedback', message, from_email, ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            sent = True
            message_form = self.form_class(label_suffix='', initial=self.get_user_info(request))
        return render(request, self.template_name, context={'form': message_form, 'sent': sent})

    def get_user_info(self, request):
        if request.user.is_authenticated():
            self.user = {'email': request.user.email, 'name_sender': request.user.first_name}
        return self.user

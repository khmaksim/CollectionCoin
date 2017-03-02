from django.shortcuts import render, HttpResponse
from django.template import RequestContext
from feedback.forms import FeedbackForm
from django.utils import timezone
from django.core.mail import mail_admins, send_mail, send_mass_mail, BadHeaderError


def feedback(request):
    sent = False
    if request.method == 'POST':
        feedback_form = FeedbackForm(request.POST, label_suffix='')
        if feedback_form.is_bound and feedback_form.is_valid():
            feedback = feedback_form.save(commit=False)
            feedback.datetime = timezone.now()
            feedback.user = request.user
            feedback.save()

            message = request.POST.get('message', '')
            from_email = request.POST.get('email', '')
            try:
                mail_admins('Feedback', message)
                send_mail('Feedback', message, from_email, ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            sent = True
    else:
        if request.user.is_authenticated():
            user = {'email': request.user.email, 'name_sender': request.user.first_name}
        else:
            user = {}
        feedback_form = FeedbackForm(label_suffix='', initial=user)

    return render(request, 'feedback.html', context={'form': feedback_form, 'sent': sent})

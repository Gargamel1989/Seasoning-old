from django.template.response import TemplateResponse
from django.contrib.sites.models import RequestSite
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, render_to_response
from django.template.context import RequestContext
from authentication.forms import ResendActivationEmailForm, AccountSettingsForm
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _


def register(request, backend, success_url=None, form_class=None,
             disallowed_url='registration_disallowed',
             template_name='authentication/registration_form.html',
             extra_context=None):
    """
    Allow a new user to register an account.

    The actual registration of the account will be delegated to the
    backend specified by the ``backend`` keyword argument (see below);
    it will be used as follows:

    1. The backend's ``registration_allowed()`` method will be called,
       passing the ``HttpRequest``, to determine whether registration
       of an account is to be allowed; if not, a redirect is issued to
       the view corresponding to the named URL pattern
       ``registration_disallowed``. To override this, see the list of
       optional arguments for this view (below).

    2. The form to use for account registration will be obtained by
       calling the backend's ``get_form_class()`` method, passing the
       ``HttpRequest``. To override this, see the list of optional
       arguments for this view (below).

    3. If valid, the form's ``cleaned_data`` will be passed (as
       keyword arguments, and along with the ``HttpRequest``) to the
       backend's ``register()`` method, which should return the new
       ``User`` object.

    4. Upon successful registration, the backend's
       ``post_registration_redirect()`` method will be called, passing
       the ``HttpRequest`` and the new ``User``, to determine the URL
       to redirect the user to. To override this, see the list of
       optional arguments for this view (below).
    
    **Required arguments**
    
    None.
    
    **Optional arguments**

    ``backend``
        The backend class to use.

    ``disallowed_url``
        URL to redirect to if registration is not permitted for the
        current ``HttpRequest``. Must be a value which can legally be
        passed to ``django.shortcuts.redirect``. If not supplied, this
        will be whatever URL corresponds to the named URL pattern
        ``registration_disallowed``.
    
    ``form_class``
        The form class to use for registration. If not supplied, this
        will be retrieved from the registration backend.
    
    ``extra_context``
        A dictionary of variables to add to the template context. Any
        callable object in this dictionary will be called to produce
        the end result which appears in the context.

    ``success_url``
        URL to redirect to after successful registration. Must be a
        value which can legally be passed to
        ``django.shortcuts.redirect``. If not supplied, this will be
        retrieved from the registration backend.
    
    ``template_name``
        A custom template to use. If not supplied, this will default
        to ``authentication/registration_form.html``.
    
    **Context:**
    
    ``form``
        The registration form.
    
    Any extra variables supplied in the ``extra_context`` argument
    (see above).
    
    **Template:**
    
    authentication/registration_form.html or ``template_name`` keyword
    argument.
    
    """
    backend = backend()
    if not backend.registration_allowed(request):
        return redirect(disallowed_url)
    if form_class is None:
        form_class = backend.get_form_class(request)
    
    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_user = backend.register(request, **form.cleaned_data)
            if success_url is None:
                to, args, kwargs = backend.post_registration_redirect(request, new_user)
                return redirect(to, *args, **kwargs)
            else:
                return redirect(success_url)
    else:
        form = form_class()
        
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    
    return render_to_response(template_name,
                              {'form': form},
                              context_instance=context)

def registration_closed(request):
    return render(request, 'authentication/registration_closed.html')
    
def registration_complete(request):
    return render(request, 'authentication/registration_complete.html')
    

def resend_activation_email(request):
    
    errormessage = None
    
    if request.method == "POST":
        
        form = ResendActivationEmailForm(data=request.POST)
        
        if form.is_valid():            
            site = RequestSite(request)
                    
            form.cleaned_data['email'].send_activation_email(site)
                    
            context = {'done': True}
            
            return TemplateResponse(request, 'authentication/resend_activation_email.html', context)
        
    else:
        form = ResendActivationEmailForm()
        
    context = {
        'done': False,
        'form': form,
        'error': errormessage
    }
        
    return TemplateResponse(request, 'authentication/resend_activation_email.html', context)


def activate(request, backend,
             template_name='authentication/activate.html',
             success_url=None, extra_context=None, **kwargs):
    """
    Activate a user's account.

    The actual activation of the account will be delegated to the
    backend specified by the ``backend`` keyword argument (see below);
    the backend's ``activate()`` method will be called, passing any
    keyword arguments captured from the URL, and will be assumed to
    return a ``User`` if activation was successful, or a value which
    evaluates to ``False`` in boolean context if not.

    Upon successful activation, the backend's
    ``post_activation_redirect()`` method will be called, passing the
    ``HttpRequest`` and the activated ``User`` to determine the URL to
    redirect the user to. To override this, pass the argument
    ``success_url`` (see below).

    On unsuccessful activation, will render the template
    ``authentication/activate.html`` to display an error message; to
    override thise, pass the argument ``template_name`` (see below).

    **Arguments**

    ``backend``
        The backend class to use. Required.

    ``extra_context``
        A dictionary of variables to add to the template context. Any
        callable object in this dictionary will be called to produce
        the end result which appears in the context. Optional.

    ``success_url``
        The name of a URL pattern to redirect to on successful
        acivation. This is optional; if not specified, this will be
        obtained by calling the backend's
        ``post_activation_redirect()`` method.
    
    ``template_name``
        A custom template to use. This is optional; if not specified,
        this will default to ``authentication/activate.html``.

    ``\*\*kwargs``
        Any keyword arguments captured from the URL, such as an
        activation key, which will be passed to the backend's
        ``activate()`` method.
    
    **Context:**
    
    The context will be populated from the keyword arguments captured
    in the URL, and any extra variables supplied in the
    ``extra_context`` argument (see above).
    
    **Template:**
    
    authentication/activate.html or ``template_name`` keyword argument.
    
    """
    backend = backend()
    account = backend.activate(request, **kwargs)

    if account:
        if success_url is None:
            to, args, kwargs = backend.post_activation_redirect(request, account)
            return redirect(to, *args, **kwargs)
        else:
            return redirect(success_url)

    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value

    return render_to_response(template_name,
                              kwargs,
                              context_instance=context)

def activation_complete(request):
    return render(request, 'authentication/activation_complete.html')
    

@login_required
def account_settings(request):
    if request.method == "POST":
        form = AccountSettingsForm(request.POST, request.FILES, instance=request.user)
        
        if form.is_valid():
            context = {}
            old_email = get_user_model().objects.get(id=request.user.id).email
            if not form.cleaned_data['email'] == old_email:
                # TODO: mail users new email adres
                context['email_message'] = _('An email has been sent to the new email address provided by you. Please follow the instructions \
                                              in this email to complete the changing of your email address.')
            form.save()
            return render(request, 'authentication/account_change_done.html', context)
    else:
        form = AccountSettingsForm(instance=request.user)
    
    return render(request, 'authentication/account_settings.html', {'form': form})

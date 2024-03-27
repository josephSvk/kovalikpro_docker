from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView

from kovalikpro.users.models import User

from .models import QuoteSubscription


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "id"
    slug_url_kwarg = "id"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        # for mypy to know that the user is authenticated
        assert self.request.user.is_authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})


user_redirect_view = UserRedirectView.as_view()


def toggle_quote_subscription(request):
    if not request.user.is_authenticated:
        messages.error(request, "Pre zmenu odberu musíte byť prihlásený.")
        return redirect("login")

    # Rozpakovanie vrátenej dvojice z get_or_create do dvoch premenných
    subscription, created = QuoteSubscription.objects.get_or_create(user=request.user)

    # Tu je potrebné opraviť logiku. Ak už objekt existuje, 'created' bude False.
    if not created:
        subscription.subscribed = not subscription.subscribed
        if subscription.subscribed:
            messages.success(request, "Úspešne ste sa prihlásili na odber citátov!")
        else:
            messages.success(request, "Váš odber citátov bol zrušený.")
    else:
        # Ak je objekt práve vytvorený,
        # predpokladáme, že sa používateľ prihlásil na odber
        messages.success(request, "Úspešne ste sa prihlásili na odber citátov!")

    subscription.save()
    return redirect(request.headers.get("referer", "home"))

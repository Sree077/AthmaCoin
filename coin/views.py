import random

from django.shortcuts import redirect, render
from django.views import View, generic
from django.urls import reverse_lazy
from braces.views import LoginRequiredMixin, SuperuserRequiredMixin
from django.views.generic.edit import FormMixin
from django.contrib.auth import get_user_model
from django.conf import settings
from . import models, forms


class GenerateCouponCodes(LoginRequiredMixin, SuperuserRequiredMixin, View):
    model = models.Coupon
    queryset = models.Shop.objects.all()
    code_per_shop = settings.NUMBER_OF_COUPONS_PER_SHOP
    success_url = reverse_lazy("generate_success")

    def get_coupon_code(self):
        return random.randint(100000, 999999)

    def get_shop_queryset(self):
        return models.Shop.objects.all()

    def check_coupon_codes_exists(self, shop):
        return models.Coupon.objects.filter(shop=shop).exists()

    def set_coupon_codes(self, shop):
        if not self.check_coupon_codes_exists(shop):
            for _ in range(0, self.code_per_shop):
                coupon = self.model(shop=shop, code=self.get_coupon_code(), status=self.model.UNCLAIMED)
                coupon.save()

    def get(self, request, **kwargs):
        shops = self.get_shop_queryset()
        print("generating coupon codes...")
        for shop in shops:
            print(f"for - {shop.name}")
            self.set_coupon_codes(shop)
            print("done")
        print("done generating coupon codes")
        return redirect(self.success_url)


class GenerateSuccess(LoginRequiredMixin, SuperuserRequiredMixin, generic.TemplateView):
    template_name = "coupon_generated.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "shops": models.Shop.objects.all(),
            "coupons": models.Coupon.objects.all(),
        })
        return context


class ValidateCouponCodes(LoginRequiredMixin, FormMixin, View):
    template_name = "home.html"
    model = models.Coupon
    coins_per_code = settings.COINS_PER_COUPON_CODE
    form_class = forms.CodeForm
    success_url = reverse_lazy("profile")

    def render_to_response(self, context):
        context.update({"leaderboard": get_user_model().objects.all().order_by("-AthmaCoin")})
        return render(self.request, self.template_name, context)

    def change_coupon_status(self, coupon):
        coupon.status = self.model.CLAIMED
        coupon.save()

    def add_points(self):
        user = get_user_model().objects.get(id=self.request.user.id)
        user.AthmaCoin += self.coins_per_code
        user.save()

    def form_valid(self, form):
        code = form.cleaned_data["code"]
        coupon = models.Coupon.objects.get(code=code)
        if coupon.is_claimed():
            print("coupon already claimed")
            form.add_error("code", f"Coupon code is already claimed")
            return self.render_to_response(self.get_context_data(form=form))
        if models.UserShop.objects.filter(user=self.request.user, shop=coupon.shop).exists():
            print("shop already claimed")
            form.add_error("code", f"You have already claimed coupon code from this shop {coupon.shop.name}")
            return self.render_to_response(self.get_context_data(form=form))
        self.change_coupon_status(coupon)
        self.add_points()
        user_shop = models.UserShop(user=self.request.user, shop=coupon.shop)
        user_shop.save()
        return redirect(self.get_success_url())

    def post(self, request, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

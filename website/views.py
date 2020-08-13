import datetime 
from collections import OrderedDict
import json
from monthdelta import monthdelta

from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic import View, ListView
from django.views.generic.edit import FormView
from django.views.defaults import page_not_found, server_error
from django.http import JsonResponse
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import login, update_session_auth_hash
from django.db.models import Q, Sum, Count, F, Window, Value, FloatField
from django.db.models.functions import ExtractMonth, ExtractYear, Replace
from django.core import serializers
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.forms import SetPasswordForm
from django.urls import reverse

from website.models import CtaCte
from website.models import Deliveries
from website.models import Sales
from website.models import SpeciesHarvest
from website.models import Applied
from website.models import UserInfo
from website.models import Notifications
from website.models import ViewedNotifications
from website.models import Currencies
from website.models import Board
from website.models import TicketsAnalysis
from website.models import City
from website.models import Rain
from website.models import RainDetail

from website.forms import ExtranetClientSelectionForm

from website.tokens import account_activation_token

from bh import settings


# def cp(request):
#     pass
# def downloadexcel(request):
#     pass
# def downloadPDFExtranet(request):
#     pass
# def downloadRainExcel(request):
#     pass
# def sales(request):
#     pass


def handler404(request, exception):
    return page_not_found(request, exception, template_name='404.html')


def handler500(request):
    return server_error(request, template_name='500.html')


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['currency'] = Currencies.objects.order_by('-date')[:1]
        context['board'] = Board.objects.order_by('-date')[:1]
        rain = Rain.objects.order_by('-date')[:1]
        context['rain'] = RainDetail.objects.filter(rain=rain).order_by('city__city')
        return context


class CurrencyView(ListView):
    http_method_names = ['post',]
    model = Currencies

    def post(self, request, *args, **kwargs):
        data = None
        get_date = request.POST.get('cDate')
        currency = Currencies.objects.filter(date=get_date)
        if currency:
            data = serializers.serialize('json',currency)
        return JsonResponse({'data': data})


class BoardView(ListView):
    http_method_names = ['post',]
    model = Board

    def post(self, request, *args, **kwargs):
        data = None
        get_date = request.POST.get('bDate')
        board = Board.objects.filter(date=get_date)
        if board:
            data = serializers.serialize('json',board)
        return JsonResponse({'data': data})


class RainView(ListView):
    http_method_names = ['post',]
    model = RainDetail

    def post(self, request, *args, **kwargs):
        data = None
        get_date = request.POST.get('rDate')
        rain = RainDetail.objects.filter(rain=get_date).values('rain', 'city__city', 'mm').order_by('city__city')
        if rain:
            rain_data = []
            for r in rain:
                temp = {}
                temp['date'] = str(r['rain'])
                temp['city'] = r['city__city']
                temp['mm'] = r['mm']
                rain_data.append(temp)
            data = json.dumps(rain_data)
        return JsonResponse({'data': data})


class HistoricRainView(TemplateView):
    template_name = 'historic_rain.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        # Filter City = 1 only por Arrecifes
        rain = RainDetail.objects.filter(city=1).annotate(month=ExtractMonth('rain'), year=ExtractYear('rain')).values('month', 'year').annotate(mmsum=Sum('mm')).order_by('-year', 'month')
        history = OrderedDict()
        month_avg = OrderedDict()
        prev_year = 0
        prev_month = 0

        for r in rain:
            year = r['year']
            month = r['month']
            if history.get(year, None) is None:
                history[year] = OrderedDict()
                history[year]['rain'] = OrderedDict()
                history[year]['total'] = 0
            if month_avg.get(month, None) is None:
                month_avg[month] = OrderedDict()
                month_avg[month]['sum'] = 0
                month_avg[month]['count'] = 0
            if year == prev_year or prev_year == 0:
                if prev_month + 1 == month or prev_month == 0:
                    # history[year]['rain'][month] = r['mmsum']
                    history[year]['rain'][month] = OrderedDict()
                    history[year]['rain'][month]['name'] = months[month-1]
                    history[year]['rain'][month]['mm'] = r['mmsum']
                    history[year]['total'] += r['mmsum']
                    month_avg[month]['sum'] += r['mmsum']
                    month_avg[month]['count'] += 1
                else:
                    for i in range(prev_month+1, month):
                        # history[year]['rain'][datetime.datetime(year,i,1).date().month] = 0
                        history[year]['rain'][datetime.datetime(year,i,1).date().month] = OrderedDict()
                        history[year]['rain'][datetime.datetime(year,i,1).date().month]['name'] = months[datetime.datetime(year,i,1).date().month - 1]
                        history[year]['rain'][datetime.datetime(year,i,1).date().month]['mm'] = 0
                        if month_avg.get(datetime.datetime(year,i,1).date().month, None) is None:
                            month_avg[datetime.datetime(year,i,1).date().month] = OrderedDict()
                            month_avg[datetime.datetime(year,i,1).date().month]['sum'] = 0
                            month_avg[datetime.datetime(year,i,1).date().month]['count'] = 0
                        month_avg[datetime.datetime(year,i,1).date().month]['count'] += 1
                    # history[year]['rain'][month] = r['mmsum']
                    history[year]['rain'][month] = OrderedDict()
                    history[year]['rain'][month]['name'] = months[month-1]
                    history[year]['rain'][month]['mm'] = r['mmsum']
                    history[year]['total'] += r['mmsum']
                    month_avg[month]['sum'] += r['mmsum']
                    month_avg[month]['count'] += 1
            else:
                # history[year]['rain'][month] = r['mmsum']
                history[year]['rain'][month] = OrderedDict()
                history[year]['rain'][month]['name'] = months[month-1]
                history[year]['rain'][month]['mm'] = r['mmsum']
                history[year]['total'] += r['mmsum']
                month_avg[month]['sum'] += r['mmsum']
                month_avg[month]['count'] += 1

            prev_year = year
            prev_month = month
        
        context['history'] = history
        context['month_avg'] = month_avg
        context['months'] = months
        return context


class AccountActivationView(View):
    def get(self, request, *args, **kwargs):
        try:
            uidb64 = kwargs['uidb64']
            token = kwargs['token']
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        
        # Check token, mark account as active and confirm account
        if user is not None and account_activation_token.check_token(user, token):
            user.userinfo.account_confirmed = True
            user.userinfo.save()
            user.is_active = True
            user.save()
            # Set backend for user instead authenticate() function
            user.backend = 'django.contrib.auth.backends.AllowAllUsersModelBackend'
            login(request, user)
            request.session['algoritmo_code'] = user.userinfo.algoritmo_code

            return render(request, 'change_password.html', {'account_confirmed': True})
        else:
            return render(request, 'change_password.html', {'account_confirmed_error': True})


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    form_class = SetPasswordForm
    template_name = 'change_password.html'

    def form_valid(self, form):
        form.save()
        if self.request.user.userinfo.random_password == True:
            self.request.user.userinfo.random_password = False
            self.request.user.userinfo.save()
        if not self.request.user.userinfo.is_commercial:
            self.request.session['algoritmo_code'] = self.request.user.userinfo.algoritmo_code
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)


class ExtranetView(LoginRequiredMixin, FormView):
    template_name = 'extranet.html'
    form_class = ExtranetClientSelectionForm
    success_url = '/extranet/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        client = form.cleaned_data['client']
        self.request.session['algoritmo_code'] = client.algoritmo_code
        self.request.session['company_name'] = client.company_name
        return super(ExtranetView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notifications = Notifications.objects.filter(active=True, date_to__gte=datetime.date.today())
        notifications_list = []
        notifications_id = []
        for n in notifications:
            if ViewedNotifications.objects.filter(notification=n.id, user=self.request.user).exists():
                pass
            else:
                notifications_list.append(n)
                notifications_id.append(n.id)
        context['notifications'] = notifications_list
        if len(notifications_id) > 0:
            self.request.session['notifications'] = notifications_id
        return context


class NotificationsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if 'notifications' in request.session:
            notifications = request.session['notifications']
            for n in notifications:
                not_obj = Notifications.objects.get(id=n)
                ViewedNotifications.objects.create(notification=not_obj, user=request.user, viewed=True)
            del request.session['notifications']
            return redirect(reverse('extranet'))
        else:
            return redirect('/')


class DateFilterBaseView(ListView):
    http_method_names = ['get',]
    allow_empty = True
    date_field = None
    since_date = None
    until_date = None
    date_format = '%Y-%m-%d'

    def get_since_date(self):
        since_date = self.since_date
        if since_date is None:
            try:
                since_date = self.kwargs['from']
            except KeyError:
                try:
                    since_date = self.request.GET['from']
                except KeyError:
                    return None
        format = self.date_format
        return datetime.datetime.strptime(since_date, format).date()

    def get_until_date(self):
        until_date = self.until_date
        if until_date is None:
            try:
                until_date = self.kwargs['to']
            except KeyError:
                try:
                    until_date = self.request.GET['to']
                except KeyError:
                    return None
        format = self.date_format
        return datetime.datetime.strptime(until_date, format).date()
    
    def get_context_data(self, **kwargs):
        context = {'from_date': self.get_since_date(),
                   'to_date': self.get_until_date()}
        context.update(kwargs)
        return super(DateFilterBaseView, self).get_context_data(**context)


class CtaCteView(LoginRequiredMixin, DateFilterBaseView):
    template_name = 'ctacte.html'

    def get(self, request, *args, **kwargs):
        ctacte_type = kwargs['ctacte_type']
        if ctacte_type != 'vencimiento' and ctacte_type != 'emision':
            raise Http404('Tipo de cuenta corriente iválido')
        if ctacte_type == 'emision':
            self.date_field = 'date_2'
        else:
            self.date_field = 'date_1'
        if self.get_since_date() is None:
            self.since_date = (datetime.datetime.today() - monthdelta(1)).strftime(self.date_format)
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_queryset(self):
        ctacte_type = self.kwargs['ctacte_type']
        algoritmo_code = self.request.session['algoritmo_code']

        date_field = self.date_field
        since = self.get_since_date()
        until = self.get_until_date()
        lookup_ib = {
            '%s__lt' % date_field: since
        }
        if until:
            lookup_kwargs = {
                '%s__gte' % date_field: since,
                '%s__lt' % date_field: until,
            }
        else:
            lookup_kwargs = {
                '%s__gte' % date_field: since
            }
        initial_balance = CtaCte.objects.filter(algoritmo_code=algoritmo_code).filter(**lookup_ib).aggregate(ib=Sum('amount_sign'))
        queryset = CtaCte.objects\
            .filter(algoritmo_code=algoritmo_code)\
            .filter(**lookup_kwargs)\
            .annotate(ib=Value(initial_balance['ib'] or 0, output_field=FloatField()))\
            .annotate(row_balance=Window(Sum('amount_sign'), order_by=[F('%s' % date_field).asc(), F('voucher').asc(), F('amount_sign').asc()]) + F('initial_balance_countable') + F('ib'))\
            .values('date_1', 'date_2', 'voucher', 'concept', 'movement_type', 'amount_sign', 'initial_balance_countable', 'ib', 'row_balance').order_by('%s' % date_field, 'voucher', 'amount_sign')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ctacte_type'] = self.kwargs['ctacte_type']
        return context


class AppliedView(LoginRequiredMixin, DateFilterBaseView):
    template_name = 'applied.html'
    date_field = 'expiration_date'

    def get_queryset(self):
        algoritmo_code = self.request.session['algoritmo_code']

        date_field = self.date_field
        since = self.get_since_date()
        until = self.get_until_date()
        if since:
            lookup_ib = {
                '%s__lt' % date_field: since
            }
            initial_balance = Applied.objects.filter(algoritmo_code=algoritmo_code).filter(**lookup_ib).aggregate(ib=Sum('amount_sign'))
            if until:
                lookup_kwargs = {
                    '%s__gte' % date_field: since,
                    '%s__lt' % date_field: until,
                }
            else:
                lookup_kwargs = {
                    '%s__gte' % date_field: since
                }
            queryset = Applied.objects\
                .filter(algoritmo_code=algoritmo_code)\
                .filter(**lookup_kwargs)\
                .annotate(ib=Value(initial_balance['ib'] or 0, output_field=FloatField()))\
                .annotate(row_balance=Window(Sum('amount_sign'), order_by=[F('%s' % date_field).asc(), F('voucher').asc(), F('amount_sign').asc()]) + F('ib'))\
                .values('expiration_date', 'issue_date', 'voucher', 'concept', 'movement_type', 'amount_sign', 'ib', 'row_balance').order_by('%s' % date_field, 'voucher', 'amount_sign')
        else:
            queryset = Applied.objects\
                .filter(algoritmo_code=algoritmo_code)\
                .annotate(row_balance=Window(Sum('amount_sign'), order_by=[F('%s' % date_field).asc(), F('voucher').asc(), F('amount_sign').asc()]))\
                .values('expiration_date', 'issue_date', 'voucher', 'concept', 'movement_type', 'amount_sign', 'row_balance').order_by('%s' % date_field, 'voucher', 'amount_sign')
        return queryset


class DeliveriesView(LoginRequiredMixin, ListView):
    template_name = 'deliveries.html'
    current_species = None

    def set_current_species(self, checks):
        speciesharvest_filter = Q()
        for item in checks:
            speciesharvest_filter = speciesharvest_filter | Q(speciesharvest=item)
        self.current_species = speciesharvest_filter

    def get(self, request, *args, **kwargs):
        try:
            request.session['current_species'] = kwargs['checks']
            self.set_current_species(kwargs['checks'])
        except KeyError:
            try:
                request.session['current_species'] = request.GET.getlist('checks')
                self.set_current_species(request.GET.getlist('checks'))
            except KeyError:
                pass
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_queryset(self):
        algoritmo_code = self.request.session['algoritmo_code']
        current_species = self.current_species
        queryset = Deliveries.objects\
            .filter(algoritmo_code=algoritmo_code)\
            .filter(current_species)\
            .annotate(species_title=Replace('species_description', Value('COSECHA '), Value('')))\
            .values('date', 'voucher', 'gross_kg', 'humidity_percentage', 'humidity_kg', 'shaking_reduction', 'shaking_kg', 'volatile_reduction', 'volatile_kg', 'net_weight', 'factor', 'grade', 'number_1116A', 'external_voucher_number', 'driver_name', 'field_description', 'species_title')\
            .order_by('-harvest', 'species', 'field_description', 'date')
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        algoritmo_code = self.request.session['algoritmo_code']
        current_species = self.current_species
        context['species'] = SpeciesHarvest.objects\
            .filter(algoritmo_code=algoritmo_code, movement_type='D')\
            .annotate(species_title=Replace('species_description', Value('COSECHA '), Value('')))\
            .values('species', 'harvest', 'speciesharvest', 'species_title', 'species_description')\
            .order_by('-harvest', 'speciesharvest')
        context['total'] = Deliveries.objects\
            .filter(algoritmo_code=algoritmo_code)\
            .filter(current_species)\
            .aggregate(Sum('net_weight'), Count('voucher'), Sum('humidity_kg'), Sum('shaking_kg'), Sum('volatile_kg'), Sum('gross_kg'))
        context['totals_by_field'] = list(
            Deliveries.objects\
                .filter(algoritmo_code=algoritmo_code)\
                .filter(current_species)\
                .annotate(species_title=Replace('species_description', Value('COSECHA '), Value('')))\
                .values('species_title', 'field_description')\
                .annotate(total_net=Sum('net_weight'), tickets_count=Count('voucher'), total_hum=Sum('humidity_kg'), total_sha=Sum('shaking_kg'), total_vol=Sum('volatile_kg'), total_gross=Sum('gross_kg'))\
                .order_by('-harvest', 'speciesharvest')
        )
        # Use list() to evaluate QuerySet only once, otherwise queryset will be evaluated every time a ticket is searched
        context['ticket_analysis'] = list(
            TicketsAnalysis.objects\
                .filter(algoritmo_code=algoritmo_code)\
                .filter(current_species)\
                .values('ticket', 'analysis_costs', 'gluten', 'analysis_item', 'percentage', 'bonus', 'reduction', 'item_descripcion')\
                .order_by('item_descripcion')
        )
        return context
import datetime 
from collections import OrderedDict
import json
import csv
import io
from monthdelta import monthdelta

from django.db.models.functions import Coalesce
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic.list import MultipleObjectMixin
from django.views.generic import View, ListView
from django.views.generic.edit import FormView
from django.views.defaults import page_not_found, server_error
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse, HttpResponseRedirect
from django.http import Http404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.contrib.auth import login, update_session_auth_hash
from django.db.models import Q, Sum, Count, F, Window, Value, FloatField
from django.db.models.functions import ExtractMonth, ExtractYear, Replace
from django.core import serializers
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.forms import SetPasswordForm
from django.urls import reverse
from django.template import loader

from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import requests
from requests.auth import HTTPBasicAuth

from website.forms import CP, ExtranetClientSelectionForm
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
from website.models import Careers
from website.tokens import account_activation_token
from website import import_tasks

from bh import settings

from django.http import FileResponse

def cp(request):

    def proccess_cp(file, form):

        #CONST
        species_dict = {
            '0000': '------',
            'ALGO': 'Algodón',
            'AVEN': 'Avena',
            'CART': 'Cártamo',
            'CEBA': 'Cebada',
            'CECE': 'Cebada Cervecera',
            'COLZ': 'Colza',
            'COL0': 'Colza Doble 00',
            'CUAR': 'Cuarta de Cebada',
            'GIRA': 'Girasol',
            'LINO': 'Lino',
            'MAIZ': 'Maíz',
            'MAMA': 'Maíz Mav',
            'MAPI': 'Maíz Pisingallo',
            'MANI': 'Maní',
            'SOJA': 'Soja',
            'SORG': 'Sorgo',
            'TRIG': 'Trigo',
            'TRIC': 'Trigo Candeal',
            'TRIP': 'Trigo Pan',
        }

        harvest_dict = {'0000': '------'}
        date = datetime.datetime.now().year
        for year in range(date-3,date+1):
            harvest_dict[str(year)[-2:] + str(year+1)[-2:]] = str(year)[-2:] + '/' + str(year+1)[-2:]

        # Init InMemory PDF file & canvas
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=A4)

        # Init fields through form data
        ownership_line = form.get('ownership_line', None)
        if ownership_line:
            ownership_height = 20
        else:
            ownership_height = 0

        destination_load = form.get('destination_load', None)
        species = species_dict.get(form['species'], None)
        harvest = harvest_dict.get(form['harvest'], None)

        fcarga_year = str(datetime.datetime.strptime(form['load_date'], "%Y-%m-%d").date().year)
        fcarga_month = ('0'+str(datetime.datetime.strptime(form['load_date'], "%Y-%m-%d").date().month))[-2:]
        fcarga_day = ('0'+str(datetime.datetime.strptime(form['load_date'], "%Y-%m-%d").date().day))[-2:]

        observations = can.beginText()
        observations.setTextOrigin(410, 430 - ownership_height)
        observations.textLines(form['observations'])

        # Write form fields to canvas
        can.setFont('Helvetica', 12)
        can.drawString(235, 747, form['ctg'])
        can.drawString(320, 747, form['renspa'])
        can.setFont('Helvetica', 10)
        can.drawString(506, 761, fcarga_day)
        can.drawString(524, 761, fcarga_month)
        can.drawString(541, 761, fcarga_year)
        can.drawString(183, 683 - ownership_height, form['intermediary'])
        can.drawString(183, 663 - ownership_height, form['sender'])
        can.drawString(183, 643 - ownership_height, form['broker'])
        can.drawString(183, 623 - ownership_height, form['mat'])
        can.drawString(183, 603 - ownership_height, form['broker_seller'])
        can.drawString(183, 583 - ownership_height, form['representative'])
        can.drawString(183, 563 - ownership_height, form['addressee'])
        can.drawString(183, 543 - ownership_height, form['destination'])
        can.drawString(183, 523 - ownership_height, form['freight_broker'])
        can.drawString(183, 504 - ownership_height, form['carrier'])
        can.drawString(183, 484 - ownership_height, form['driver'])
        can.drawString(471, 684 - ownership_height, form['intermediary_cuit'])
        can.drawString(471, 664 - ownership_height, form['sender_cuit'])
        can.drawString(471, 644 - ownership_height, form['broker_cuit'])
        can.drawString(471, 624 - ownership_height, form['mat_cuit'])
        can.drawString(471, 604 - ownership_height, form['broker_seller_cuit'])
        can.drawString(471, 584 - ownership_height, form['representative_cuit'])
        can.drawString(471, 564 - ownership_height, form['addressee_cuit'])
        can.drawString(471, 544 - ownership_height, form['destination_cuit'])
        can.drawString(471, 524 - ownership_height, form['freight_broker_cuit'])
        can.drawString(471, 505 - ownership_height, form['carrier_cuit'])
        can.drawString(471, 486 - ownership_height, form['driver_cuit'])
        can.drawString(370, 460 - ownership_height, harvest)
        can.drawString(130, 460 - ownership_height, species.upper())
        can.drawString(246, 460 - ownership_height, form['species_type'])
        can.drawString(500, 460 - ownership_height, form['contract'])
        if destination_load:
            can.drawString(133, 430 - ownership_height, 'X')
        can.drawString(125, 410 - ownership_height, form['estimated_kg'])
        if form['quality'] == 'DECLARACION':
            can.drawString(257, 445 - ownership_height, 'X')
        elif form['quality'] == 'CONFORME':
            can.drawString(257, 427 - ownership_height, 'X')
        else:
            can.drawString(257, 411 - ownership_height, 'X')
        can.drawString(353, 442 - ownership_height, form['gross_kg'])
        can.drawString(353, 425 - ownership_height, form['tare_kg'])
        can.drawString(353, 409 - ownership_height, form['net_kg'])
        can.drawText(observations)
        can.drawString(423, 395 - ownership_height, form['stablishment'])
        can.drawString(423, 381 - ownership_height, form['city'])
        can.drawString(423, 367 - ownership_height, form['state'])
        can.drawString(110, 375 - ownership_height, form['address'])
        can.drawString(360, 349 - ownership_height, form['destination_city'])
        can.drawString(360, 332 - ownership_height, form['destination_state'])
        can.drawString(80, 332 - ownership_height, form['destination_address'])
        can.drawString(345, 311 - ownership_height, form['freight_payer'])
        can.drawString(95, 294 - ownership_height, form['truck'])
        can.drawString(95, 277 - ownership_height, form['trailer'])
        can.drawString(95, 260 - ownership_height, form['km'])
        can.drawString(242, 277 - ownership_height, form['ref_rate'])
        can.drawString(242, 260 - ownership_height, form['rate'])
        can.setFont('Helvetica', 8)
        can.drawString(463, 18 - ownership_height, form['fumigant_dni'])
        can.drawString(293, 18 - ownership_height, form['fumigant_observation'])
        can.save()

        # Move to the beginning of the StringIO buffer
        packet.seek(0)
        new_pdf = PdfFileReader(packet)
        # Get the canvas content
        new_pdf_page = new_pdf.getPage(0)
        existing_pdf = PdfFileReader(file)
        output = PdfFileWriter()
        for numpage in range(0, existing_pdf.getNumPages()):
            page = existing_pdf.getPage(numpage)
            # Merge uploaded PDF page with canvas content
            page.mergePage(new_pdf_page)
            page.compressContentStreams()
            # Save pages to new PDF
            output.addPage(page)
        # Write final PDF to buffer
        output.write(packet)
        # Return buffer stream
        return packet.getvalue()

    if request.method == 'POST':
        form = CP(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['cp']
            cp = proccess_cp(file, request.POST)
            name = file.name
            response = HttpResponse(cp, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="%s"' % name
            return response
    else:
        form = CP()
    return render(request, 'cp.html', {'form': form})


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


class CareersView(TemplateView):
    template_name = 'cv.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['careers'] = Careers.objects.filter(active=True)
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
        context['months'] = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        # Filter City = 1 only por Arrecifes
        rain = RainDetail.objects.filter(city=1).annotate(month=ExtractMonth('rain'), year=ExtractYear('rain')).values('month', 'year').annotate(mmsum=Sum('mm')).order_by('-year', 'month')
        context['rain'] = rain
        return context


class CustomLoginView(LoginView):
    def form_valid(self, form):
        """Security check complete. Log the user in."""
        login(self.request, form.get_user())
        user = form.get_user()
        self.request.session['algoritmo_code'] = user.userinfo.algoritmo_code
        return HttpResponseRedirect(self.get_success_url())


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
    initial = False
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
        try:
            return datetime.datetime.strptime(since_date, format).date()
        except:
            return None

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
        try:
            return datetime.datetime.strptime(until_date, format).date()
        except:
            return None
    
    def get_context_data(self, **kwargs):
        context = {'from_date': self.get_since_date(),
                   'to_date': self.get_until_date(),
                   'initial': self.initial}
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
        if self.get_since_date() is None and self.get_until_date() is None:
            self.since_date = (datetime.datetime.today() - monthdelta(1)).strftime(self.date_format)
            self.initial = True
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_queryset(self):
        ctacte_type = self.kwargs['ctacte_type']
        algoritmo_code = self.request.session['algoritmo_code']

        date_field = self.date_field
        since = self.get_since_date()
        until = self.get_until_date()
        initial_balance = {}
        if since:
            lookup_ib = {
                '%s__lt' % date_field: since
            }
            initial_balance = CtaCte.objects.filter(algoritmo_code=algoritmo_code).filter(**lookup_ib).aggregate(ib=Coalesce(Sum('amount_sign'),0))
        if until and since:
            lookup_kwargs = {
                '%s__gte' % date_field: since,
                '%s__lt' % date_field: until,
            }
        elif until:
            lookup_kwargs = {
                '%s__lt' % date_field: until,
            }
        else:
            lookup_kwargs = {
                '%s__gte' % date_field: since
            }
        queryset = CtaCte.objects\
            .filter(algoritmo_code=algoritmo_code)\
            .filter(**lookup_kwargs)\
            .annotate(ib=Value(initial_balance.get('ib', 0), output_field=FloatField()))\
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
        lookup_kwargs = {}
        initial_balance = {}
        if since:
            lookup_ib = {
                '%s__lt' % date_field: since
            }
            initial_balance = Applied.objects.filter(algoritmo_code=algoritmo_code).filter(**lookup_ib).aggregate(ib=Coalesce(Sum('amount_sign'),0))
        if until and since:
            lookup_kwargs = {
                '%s__gte' % date_field: since,
                '%s__lt' % date_field: until,
            }
        elif until:
            lookup_kwargs = {
                '%s__lt' % date_field: until,
            }
        elif since:
            lookup_kwargs = {
                '%s__gte' % date_field: since,
            }
        queryset = Applied.objects\
            .filter(algoritmo_code=algoritmo_code)\
            .filter(**lookup_kwargs)\
            .annotate(ib=Value(initial_balance.get('ib', 0), output_field=FloatField()))\
            .annotate(row_balance=Window(Sum('amount_sign'), order_by=[F('%s' % date_field).asc(), F('voucher').asc(), F('amount_sign').asc()]) + F('ib'))\
            .values('expiration_date', 'issue_date', 'voucher', 'concept', 'movement_type', 'amount_sign', 'ib', 'row_balance').order_by('%s' % date_field, 'voucher', 'amount_sign')
        return queryset


class HarvestFilterBaseView(ListView):
    current_species = None

    def set_current_species(self, checks):
        speciesharvest_filter = Q()
        for item in checks:
            speciesharvest_filter = speciesharvest_filter | Q(speciesharvest=item)
        self.current_species = speciesharvest_filter
    
    def get_species_for(self, algoritmo_code, movement_type):
        return SpeciesHarvest.objects\
            .filter(algoritmo_code=algoritmo_code, movement_type=movement_type)\
            .annotate(species_title=Replace('species_description', Value('COSECHA '), Value('')))\
            .values('species', 'harvest', 'speciesharvest', 'species_title', 'species_description')\
            .order_by('-harvest', 'speciesharvest')
    
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        algoritmo_code = self.request.session['algoritmo_code']
        current_species = self.current_species
        return context


class DeliveriesView(LoginRequiredMixin, HarvestFilterBaseView):
    template_name = 'deliveries.html'

    def get_queryset(self):
        current_species = self.current_species
        if current_species:
            algoritmo_code = self.request.session['algoritmo_code']
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
        context['species'] = self.get_species_for(algoritmo_code, 'D')
        if current_species:
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


class SalesView(LoginRequiredMixin, HarvestFilterBaseView):
    template_name = 'sales.html'

    def get_queryset(self):
        current_species = self.current_species
        if current_species:
            algoritmo_code = self.request.session['algoritmo_code']
            queryset = Sales.objects\
                .filter(algoritmo_code=algoritmo_code)\
                .filter(current_species)\
                .annotate(species_title=Replace('species_description', Value('COSECHA '), Value('')))\
                .values('id', 'date', 'voucher', 'field_description', 'service_billing_date', 'to_date', 'gross_kg', 'service_billing_number', 'number_1116A', 'price_per_yard', 'grade', 'driver_name', 'observations', 'species_description', 'indicator', 'species_title')\
                .order_by('-harvest', 'speciesharvest', 'indicator', 'date')
            return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        algoritmo_code = self.request.session['algoritmo_code']
        current_species = self.current_species
        context['species'] = self.get_species_for(algoritmo_code, 'S')
        if current_species:
            context['totals_by_sale'] = list(
                Sales.objects\
                .filter(algoritmo_code=algoritmo_code)\
                .filter(current_species)\
                .annotate(species_title=Replace('species_description', Value('COSECHA '), Value('')))\
                .values('species_title', 'indicator')\
                .annotate(total_gross=Sum('gross_kg'), total_pending=Sum('service_billing_number'), total_liquid=Sum('number_1116A'), total_count=Count('voucher'), total_in=Sum('gross_kg', filter=Q(gross_kg__gt=0)), total_out=Sum('gross_kg', filter=Q(gross_kg__lt=0)))\
                .order_by('-harvest', 'speciesharvest')
            )
            context['total_sales'] = Sales.objects.filter(algoritmo_code=algoritmo_code, indicator='2').filter(current_species).aggregate(Sum('net_weight'))
            context['total_to_set'] = Sales.objects.filter(algoritmo_code=algoritmo_code, indicator='2B').filter(current_species).aggregate(Sum('net_weight'))
            context['total_other'] = Sales.objects.filter(algoritmo_code=algoritmo_code, indicator='3').filter(current_species).aggregate(Sum('net_weight'))
            context['total_settled'] = Sales.objects.filter(algoritmo_code=algoritmo_code).filter(current_species).aggregate(Sum('number_1116A'))
        return context


class DownloadCSVBaseClass(MultipleObjectMixin, View):
    filename = None
    fields = None
    headers = None
    template = None

    def get_csv_response(self):
        queryset = self.get_queryset()
        response = HttpResponse(content_type='text/csv')
        filename = self.filename
        if not filename.endswith('.csv'):
            filename += '.csv'
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
        c = {
            'data': queryset,
            'headers': self.headers
        }
        t = loader.get_template(self.template)
        response.write(t.render(c))
        return response


class DownloadRainView(DownloadCSVBaseClass):
    filename = 'Historico Lluvias'
    headers = ('Mes', 'Año', 'Milimetros')
    template = 'csv_rain_template.txt'

    def get_queryset(self):
        queryset = RainDetail.objects.filter(city=1).annotate(month=ExtractMonth('rain'), year=ExtractYear('rain')).values('month', 'year').annotate(mmsum=Sum('mm')).order_by('-year', 'month')
        return queryset

    def get(self, request, *args, **kwargs):
        response = self.get_csv_response()
        return response


class DownloadCtaCteCSVView(CtaCteView, DownloadCSVBaseClass):
    filename = 'Cuenta Corriente'
    headers = ('Fecha Vencimiento', 'Fecha Emisión', 'Comprobante', 'Concepto', 'Tipo de Movimiento', 'Importe', 'Saldo')
    template = 'csv_ctacte_template.txt'

    def get(self, request, *args, **kwargs):
        super(DownloadCtaCteCSVView, self).get(request, *args, **kwargs)
        response = self.get_csv_response()
        return response


class DownloadAppliedCSVView(AppliedView, DownloadCSVBaseClass):
    filename = 'Cuenta Corriente Aplicada'
    headers = ('Fecha Vencimiento', 'Fecha Emisión', 'Comprobante', 'Concepto', 'Tipo de Movimiento', 'Importe', 'Saldo')
    template = 'csv_applied_template.txt'

    def get(self, request, *args, **kwargs):
        super(DownloadAppliedCSVView, self).get(request, *args, **kwargs)
        response = self.get_csv_response()
        return response


class DownloadDeliveriesCSVView(DeliveriesView, DownloadCSVBaseClass):
    filename = 'Entregas'
    headers = ('Fecha', 'Comprobante', 'Kilos Brutos', '% Hum.', 'Kg. Hum.', '% Zarandeo', 'Kg. Zarandeo', '% Volatil', 'Kg. Volatil', 'Kilos Netos', 'Factor', 'Grado', 'Certificado', 'Número Externo', 'Chofer', 'Campo', 'Especie y Cosecha')
    template = 'csv_deliveries_template.txt'

    def get(self, request, *args, **kwargs):
        super(DownloadDeliveriesCSVView, self).get(request, *args, **kwargs)
        response = self.get_csv_response()
        return response


class DownloadSalesCSVView(SalesView, DownloadCSVBaseClass):
    filename = 'Ventas'
    headers = ('Fecha', 'Comprobante', 'Destino', 'Fecha Entrega Desde', 'Fecha Entrega Hasta', 'Kilos', 'Pend. TC', 'Liquidado', 'Precio por Quintal', 'Moneda', 'Observaciones', 'Especie y Cosecha')
    template = 'csv_sales_template.txt'

    def get(self, request, *args, **kwargs):
        super(DownloadSalesCSVView, self).get(request, *args, **kwargs)
        response = self.get_csv_response()
        return response


class DownloadPDFView(LoginRequiredMixin, View):
    vouchers = {
        'LC': {'codigo': ['C',], 'separator': ' ', 'url':''},
        'IC': {'codigo': ['C',], 'separator': ' ', 'url':''},
        'LB': {'codigo': ['B',], 'separator': ' ', 'url':''},
        'IB': {'codigo': ['B',], 'separator': ' ', 'url':''},
        'ND': {'codigo': ['HNDCER','HNDE','NDE','NDECAJ','NDECER','NDEPER',], 'separator': '_', 'url':'ventas/'},
        'NC': {'codigo': ['HNCCER','HNCR','NCR','NCRCER','NCRDEV','NCSCER',], 'separator': '_', 'url':'ventas/'},
        'FC': {'codigo': ['FAC','FACCER','FACD','FACSER','FASCER','HFAC','HFACER',], 'separator': '_', 'url':'ventas/'},
        'PC': {'codigo': ['PC',], 'separator': '_', 'url':'tesoreria/'},
        'OP': {'codigo': ['OP',], 'separator': '_', 'url':'tesoreria/'},
        'RE': {'codigo': ['RE',], 'separator': '_', 'url':'tesoreria/'},
        'VT': {'codigo': ['VT',], 'separator': '_', 'url':'cnv/'},
        'VF': {'codigo': ['VF',], 'separator': '_', 'url':'cnv/'},
    }

    def append_pdf(self, input, output):
        [output.addPage(input.getPage(page_num)) for page_num in range(input.numPages)]

    def merge_pdf(self, file1, file2):
        # Create instance por Write new PDF
        output = PdfFileWriter()
        pdf1 = PdfFileReader(io.BytesIO(file1))
        pdf2 = PdfFileReader(io.BytesIO(file2))
        self.append_pdf(pdf1,output)
        self.append_pdf(pdf2,output)
        # Init InMemory PDF file
        new_file = io.BytesIO()

        # Write PDF to buffer
        output.write(new_file)
        return new_file.getvalue()

    def search_file(self, voucher, voucher_date):
        voucher = voucher.split(' ')
        if self.vouchers.get(voucher[0], None) is None:
            return None
        else:
            separator = self.vouchers[voucher[0]]['separator']
            url = self.vouchers[voucher[0]]['url']
            for c in self.vouchers[voucher[0]]['codigo']:
                file_name = '{0}{1}{2}{3}{4}.pdf'.format(c, separator, voucher[1], separator, voucher[2])
                if 'tesoreria' in url:
                    file_url = 'http://{0}:{1}/{2}{3}/C{4}{5}{6}'.format(settings.RS_HOST, settings.RS_PORT, url, voucher_date, str(self.request.session['algoritmo_code']), separator, file_name)
                else:
                    file_url = 'http://{0}:{1}/{2}{3}'.format(settings.RS_HOST, settings.RS_PORT, url, file_name)
                r = requests.get(file_url, auth=HTTPBasicAuth(settings.RS_USER, settings.RS_PASS))
                if r.status_code == 200:
                    ##### FASCER Tickets Detail
                    if c == 'FASCER':
                        tickets_file_url = 'http://{0}:{1}/DETTK{2}{3}{4}{5}.pdf'.format(settings.RS_HOST, settings.RS_PORT, separator, voucher[1], separator, voucher[2])
                        rtk = requests.get(tickets_file_url, auth=HTTPBasicAuth(settings.RS_USER, settings.RS_PASS))
                        if rtk.status_code == 200:
                            r = self.merge_pdf(r.content, rtk.content)
                            return {'file':r, 'filename':file_name}
                    # If voucher is not FASCER or there is no DETTK then return the response content (file)
                    return {'file':r.content, 'filename':file_name}

    def get(self, request, *args, **kwargs):
        algoritmo_code = request.session['algoritmo_code']
        try:
            f = kwargs['f']
            d = kwargs['d']
        except KeyError:
            try:
                f = request.GET['f']
                d = request.GET['d']
            except KeyError:
                pass
        file = self.search_file(f, d)
        if file:
            response = HttpResponse(file['file'], content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(file['filename'])
            return response
        else:
            raise Http404


@login_required
@staff_member_required
def importdata(request, datatype):
    if datatype == 'ctacte':
        import_tasks.importCtaCteP()
    elif datatype == 'kilos':
        import_tasks.importKilos()
    elif datatype == 'applied':
        import_tasks.importApplied()
    elif datatype == 'analysis':
        import_tasks.importTicketsAnalysis()
    elif datatype == 'all':
        import_tasks.importCtaCteP()
        import_tasks.importKilos()
        import_tasks.importApplied()
        import_tasks.importTicketsAnalysis()
    else:
        raise Http404()

    return render(request, 'update_extranet.html')

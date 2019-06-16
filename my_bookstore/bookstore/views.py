from django.shortcuts import render,redirect, get_object_or_404, HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Product, assistant, LoginTracker,Transaction
from .forms import ProductForm
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import datetime
from django.contrib.auth import logout
from django.urls import reverse
from django.db.models import Count,Sum
from django.db.models.query import QuerySet
from django.utils import timezone
from django.db.models.functions import TruncDay
# Create your views here.


def Assistant(request):
    templates = 'assistant.html'
    allAssistant = assistant.objects.all()
    context = {
        'allAssistant': allAssistant,

    }
    return render(request, templates, context)


@login_required(login_url='http://127.0.0.1:8000')
def Welcome(request):
    templates = 'welcome.html'
    templates1 = 'assistant.html'
    assistant_username = request.GET.get('username')
    request.session['username'] = request.GET['username']
    if assistant.objects.filter(username=assistant_username):
        # getting only the pk of the assistant
        assistant_logger = assistant.objects.filter(username=assistant_username).get().pk
        # getting information of the pk above
        logger = assistant.objects.get(pk=assistant_logger)
        # passing username of the pk above
        # login datetime by now.
        logintrack = LoginTracker(username=logger,log_in=datetime.datetime.now())
        logintrack.save()
        context = {
            'assistant_username': assistant_username,
        }
        return render(request,templates,context)
    else:
        messages.warning(request, "Username invalid")
        return render(request,templates1)
    
        
@login_required(login_url='http://127.0.0.1:8000',redirect_field_name='Assistant')
def inventory(request):
    templates = 'inventory.html'
    Allproduct = Product.objects.all().order_by('category')
    paginator = Paginator(Allproduct, 5)
    page = request.GET.get('page')
    ProductAll = paginator.get_page(page)
    context = {
        'ProductAll': ProductAll,
        'AllProduct': Allproduct,
    }
    if request.method == 'POST':
        prod_name = request.POST.get('prod_name')
        if Product.objects.filter(product_name=prod_name):
            # session the query
            get_username = request.session.get('username')
            # getting the primary key of the query
            get_assistant_pk = assistant.objects.filter(username=get_username).get().pk
            # info of the primary key
            get_assistant_info = assistant.objects.get(pk=get_assistant_pk)

            get_pk = Product.objects.filter(product_name=prod_name).get().pk
            product = Product.objects.get(pk=get_pk)
            quantity = request.POST.get('quantity')
            transaction = Transaction(quantity=quantity, item=product,assistant_username=get_assistant_info,total=int(quantity)*product.price)
            product.quantity=product.quantity - int(quantity)
            transaction.save()
            product.save()
            context = {
                'transaction':transaction,
                'quantity':quantity,
                'product':product,
                'get_username':get_username
            }
            return redirect('/inventory/')
            
        seldels = request.POST.getlist('check[]')  # getting the list of the data that is being check
        if len(seldels) > 0:  # length of the list
            Product.objects.filter(id__in=seldels).delete()
            return redirect('/inventory/')
    return render(request, templates, context)


@login_required(login_url='http://127.0.0.1:8000',redirect_field_name='Assistant')
def add_product(request):
    templates = 'detail.html'
    title = "Add Products"
    cancel = "Cancel"
    products = ProductForm(request.POST or None)
    if products.is_valid():
        category = products.cleaned_data.get('category')
        product_name = products.cleaned_data.get('product_name')
        quantity = products.cleaned_data.get('quantity')
        price = products.cleaned_data.get('price')
        products.save()
        return redirect('/inventory/')
    return render(request,templates, {"products": products, "title": title, "cancel": cancel})


@login_required(login_url='http://127.0.0.1:8000',redirect_field_name='Assistant')
def edit_product(request,pk):
    templates = 'detail.html'
    product = get_object_or_404(Product, pk=pk)
    form_pro = ProductForm
    products = form_pro(request.POST or None, instance=product)

    #requesting to post data
    if request.method == 'POST':
         try:
             if products.is_valid():
                 products.save()
                 messages.success(request, 
                            mark_safe(
                                'Your Product was Successfully Updated'
                 ))
         except Exception as e:
            mesasges.warning(request, 'Your Product Not Saved Due To An Error: {}'.format(e))
    else:
        form_pro = ProductForm(instance=product)
    return render(request, templates, {'products':products, 'product':product})


@login_required(login_url='http://127.0.0.1:8000',redirect_field_name='Assistant')
def search(request):
    templates = 'inventory.html'
    query = request.GET.get('q')
    if query:
        results = Product.objects.filter(Q(category__icontains=query) | Q(product_name__icontains=query))
    else:
        results = Product.objects.all()

    paginator = Paginator(results, 5)
    page = request.GET.get('page')
    ProductAll = paginator.get_page(page)
    context = {
        'ProductAll':ProductAll,
        'query':query,
    }
    return render(request, templates, context)


@login_required(login_url='http://127.0.0.1:8000',redirect_field_name='Assistant')
def TransactionList(request):
    templates = 'transaction/transaction.html'
    transac = mark_safe('Transaction')
    transaction_list = Transaction.objects.all()
    paginator = Paginator(transaction_list, 5)
    page = request.GET.get('page')
    List_transaction = paginator.get_page(page)
    
    context = {
        'transaction_list':transaction_list,
        'List_transaction':List_transaction,
        'transac':transac,
       
    }
    return render(request, templates, context)


@login_required(login_url='http://127.0.0.1:8000',redirect_field_name='Assistant')
def transac_search(request):
    templates = 'transaction/transaction.html'
    query = request.GET.get('q')
    if query:
        results = Transaction.objects.filter(Q(item__category__icontains=query) | Q(item__product_name__icontains=query))
    else:
        results = Transaction.objects.all()

    paginator = Paginator(results, 5)
    page = request.GET.get('page')
    List_transaction = paginator.get_page(page)
    context = {
        'List_transaction':List_transaction,
        'query':query,
    }
    return render(request, templates, context)


@login_required(login_url='http://127.0.0.1:8000',redirect_field_name='Assistant')
def charts(request):
    templates ='charts/charts.html'
    post_cat = request.POST.get('dropdown')
    print(post_cat)
    value = Transaction.objects.all()
    values = Transaction.objects.values('item__category','item__product_name','quantity','date')
    # daily and sum-up all the quantity
    count_day = Transaction.objects.annotate(day=TruncDay('date'))\
                                    .values('day')\
                                    .annotate(c=Sum('quantity'))\
                                    .values('item__category','item__product_name','day','c')\
                                    .all().order_by('day')
    # getting the distinct value of the item__category
    ob_cat = Transaction.objects.all().values('item__category').order_by('item__category').distinct()
    # sum up of all the sales inside the category

    all_sumcat = Transaction.objects.values('item__category').annotate(c=Sum('quantity')).order_by('item__category')
    # getting all the transaction
    get_cat = Transaction.objects.filter(item__category=post_cat)\
                                    .annotate(day=TruncDay('date'))\
                                    .values('day')\
                                    .annotate(c=Sum('quantity'))\
                                    .values('item__category','item__product_name','day','c')\
                                    .all().order_by('day')
    print(get_cat)
    context = {
        'value':value,
        'values':values,
        'count_day':count_day,
        'ob_cat': ob_cat,
        'all_sumcat':all_sumcat,
        'get_cat':get_cat,
        'post_cat':post_cat,
    }
    if Transaction.objects.filter(item__category=post_cat):
        return render(request,templates,context)
    else:
         # sum up of all the sales inside the category
        all_sumcat = Transaction.objects.values('item__category').annotate(c=Sum('quantity')).order_by('item__category')
        return render(request,templates,context)
    if(len(values) > 0):
        return render(request,templates,context)
    else:
        messages.warning(request, "No Sales Data To Graph")
        return render(request,templates,context)



@login_required(login_url='http://127.0.0.1:8000',redirect_field_name='Assistant')
def charts_search(request):
    templates = 'charts/charts.html'
    cat = request.GET.get('category')
    prod_name = request.GET.get('product_name')
    a = mark_safe('<div class="alert alert-success"><strong>'
                  'Search Found!'
                  '</strong> <button type="button" class="btn btn-primary" '
                  'data-toggle="modal" '
                  'data-target="#basicExampleModal">'
                  'View Graph'
                  '</button></div>')
    value = Transaction.objects.all()
    values = Transaction.objects.values('item__category','item__product_name','quantity','date').order_by('date')
    if Transaction.objects.filter(Q(item__category__iexact=cat) & Q(item__product_name__iexact=prod_name)):
        key = Transaction.objects.filter(Q(item__category__iexact=cat) & Q(item__product_name__iexact=prod_name)).all().order_by('date')
        count_day = Transaction.objects.annotate(day=TruncDay('date'))\
                                       .values('day')\
                                       .annotate(c=Sum('quantity'))\
                                       .values('item__category','item__product_name','day','c')\
                                       .order_by('day')
        print(count_day)
        context = {
            'value':value,
            'values':values,
            'key':key,
            'a':a,
            'count_day':count_day
        }
        return  render(request,templates,context)
    else:
         context = {
            'value':value,
            'values':values,
        }
         messages.error(request, "Category Name: " + cat + " Product Name: " + prod_name + " Not found")
         return render(request, templates,context)


@login_required(login_url='http://127.0.0.1:8000')
def log_out(request):
    templates = 'logout.html'
    if request.method == 'POST':
        get_username = request.session.get('username')
        # getting the latest log-in based on latest function
        get_id = LoginTracker.objects.filter(username__username=get_username).latest('log_in')
        # getting the primary key and the information
        update_logger = LoginTracker.objects.get(pk=get_id.pk)
        # updating the tracker based on the primary key and information
        update_logger.log_out = datetime.datetime.now()
        # save
        update_logger.save()
        logout(request)
        return HttpResponseRedirect(reverse('login'))
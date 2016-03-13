__author__ = 'kolobok'

from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from collection.models import Section, Coin, Metal, Edge, Collection
from collection.form import CoinForm, AddToCollectionForm


def main(request):
    if not request.user.is_authenticated():
        return render(request, 'catalog.html')
    else:
        title = breadcrumbs = u'Каталог'
        section_list = Section.objects.all()
        return render(request, 'catalog.html', {'title': title, 'breadcrumbs': breadcrumbs, 'section_list': section_list})
    # return render(request, 'catalog.html')


def catalog(request):
    if not request.user.is_authenticated():
        return render(request, 'catalog.html')
    else:
        title = breadcrumbs = u'Каталог'
        section_list = Section.objects.all()
        return render(request, 'catalog.html',
                      {'title': title, 'breadcrumbs': breadcrumbs, 'section_list': section_list})


def section_catalog(request, id_section):
    coins = Coin.objects.filter(section=id_section)
    section = Section.objects.get(pk=id_section)
    return render_to_response('section.html', {'section': section, 'coins': coins},
                              context_instance=RequestContext(request))


def information_coin(request, id_coin):
    coin = Coin.objects.get(pk=id_coin)

    metal_list = []
    for metal in coin.metal.all():
        metal_list.append(metal.name)

    if coin.edge is not None:
        try:
            edge = Edge.objects.get(id__exact=coin.edge.id)
            edge_name = edge.name
        except ObjectDoesNotExist:
            edge_name = ""
    else:
        edge_name = ""

    coin_form = CoinForm(instance=coin, initial={'edge': edge_name, 'metal': ','.join(metal_list)}, label_suffix='')
    return render_to_response('coin.html', {'coin': coin, 'coin_form': coin_form},
                              context_instance=RequestContext(request))


def add_to_collection(request, id_coin):
    coin = Coin.objects.get(pk=id_coin)

    if request.method == 'POST':
        add_to_collection_form = AddToCollectionForm(request.POST, label_suffix='')
        if add_to_collection_form.is_bound and add_to_collection_form.is_valid():
            collection = add_to_collection_form.save(commit=False)
            collection.coin = coin
            collection.save()
            return redirect('coins_section', id_section=coin.section_id)
    else:
        add_to_collection_form = AddToCollectionForm(label_suffix='')

    return render(request, 'add_to_collection.html',
                              {'coin': coin, 'add_to_collection_form': add_to_collection_form})


def my_collection(request):
    title = breadcrumbs = u'Моя Коллекция'
    section_list = []

    section_list = Section.objects.filter(coin__collection__isnull=False).distinct()

    # for collection in Collection.objects.all():
    #     section_list.append(collection.coin.section)

    return render(request, 'collection.html', {'title': title, 'breadcrumbs': breadcrumbs, 'section_list': section_list})


def section_collection(request, id_section):
    coins = Coin.objects.filter(section=id_section)
    section = Section.objects.get(pk=id_section)
    return render_to_response('section.html', {'section': section, 'coins': coins},
                              context_instance=RequestContext(request))